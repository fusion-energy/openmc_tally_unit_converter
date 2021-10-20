from pathlib import Path

import numpy as np
import openmc
import pint

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))

def process_spectra_tally(
    tally,
    required_units=None,
    source_strength=None,
    volume=None,
):
    """Processes a spectra tally converting the tally with default units obtained
    during simulation into the user specified units. In some cases
    additional user inputs will be required such as volume or source strength."""

    # user makes use of openmc.StatePoint.get_tally to find tally
    # passes the tally into this function along with the required units
    # the tally can be returned with base units or with converted units

    data_frame = tally.get_pandas_dataframe()

    # checks for user provided base units
    base_units = get_tally_units(tally)
    print(f"tally {tally.name} base units {base_units}")

    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFilter):
            energy_base = filter.values * base_units[0]
            # skip other filters and contine or error if not found?

    # numpy array is needed as a pandas series can't have units
    tally_base = np.array(data_frame["mean"]) * base_units[1]

    if required_units:
        scaled_tally_result = scale_tally(
            tally,
            tally_base,
            base_units[1],
            ureg[required_units[1]],
            source_strength,
            volume,
        )
        tally_results = convert_units(
            [energy_base, scaled_tally_result], required_units
        )
        return tally_results
    else:
        return [energy_base, tally_base]


def process_dose_tally(
    tally,
    required_units=None,
    source_strength=None,
    volume=None,
):
    """Processes the tally converting the tally with default units obtained
    during simulation into the user specified units. In some cases
    additional user inputs will be required. Units with"""

    # user makes use of StatePoint.get_tally to find tally
    # passes the tally into this function along with the required units
    # the tally can be returned with base units or with converted units

    data_frame = tally.get_pandas_dataframe()

    # checks for user provided base units
    base_units = get_tally_units(tally)
    print(f"tally {tally.name} base units {base_units}")

    if len(data_frame["mean"]) == 1:
        # just a single number in the tally result
        tally_result = data_frame["mean"].sum() * base_units[0]
    else:
        # more than one number, a mesh tally
        tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
        shape = tally_filter.mesh.dimension.tolist()
        if 1 in shape:
            # 2d mesh
            shape.remove(1)
        tally_result = np.array(data_frame["mean"]) * base_units[0]
        tally_result = tally_result.reshape(shape)

    if required_units:
        tally_result = scale_tally(
            tally,
            tally_result,
            base_units[0],
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_result = convert_units([tally_result], [required_units])[0]

    return tally_result


def process_tally(
    tally,
    required_units=None,
    source_strength=None,
    volume=None,
):
    """Processes the tally converting the tally with default units obtained
    during simulation into the user specified units. In some cases
    additional user inputs will be required. Units with"""

    # user makes use of StatePoint.get_tally to find tally
    # passes the tally into this function along with the required units
    # the tally can be returned with base units or with converted units

    data_frame = tally.get_pandas_dataframe()

    # checks for user provided base units
    base_units = get_tally_units(tally)
    print(f"tally {tally.name} base units {base_units}")

    # there might be more than one based unit entry if spectra has been tallied
    if len(base_units) == 1:
        if len(data_frame["mean"]) == 1:
            # just a single number in the tally result
            tally_result = data_frame["mean"].sum() * base_units[0]
        else:
            # more than one number, a mesh tally
            tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
            shape = tally_filter.mesh.dimension.tolist()
            if 1 in shape:
                # 2d mesh
                shape.remove(1)
            tally_result = np.array(data_frame["mean"]) * base_units[0]
            tally_result = tally_result.reshape(shape)

        if required_units:
            tally_result = scale_tally(
                tally,
                tally_result,
                base_units[0],
                ureg[required_units],
                source_strength,
                volume,
            )
            tally_result = convert_units([tally_result], [required_units])[0]

    return tally_result

def convert_units(value_to_convert, required_units):
    converted_units = []
    for value, required in zip(value_to_convert, required_units):
        converted_units.append(value.to(required))

    return converted_units

def scale_tally(
    tally, tally_result, base_units, required_units, source_strength, volume
):
    time_diff = check_for_dimentionality_difference(
        base_units, required_units, "[time]"
    )
    if time_diff != 0:
        print("time scaling needed (seconds)")
        if source_strength:
            source_strength = source_strength * ureg["1 / second"]
            if time_diff == -1:
                tally_result = tally_result / source_strength
            if time_diff == 1:
                tally_result = tally_result * source_strength
        else:
            raise ValueError(
                f"source_strength is required but currently set to {source_strength}"
            )

    time_diff = check_for_dimentionality_difference(
        base_units, required_units, "[pulse]"
    )
    if time_diff != 0:
        print("time scaling needed (pulse)")
        if source_strength:
            source_strength = source_strength * ureg["1 / pulse"]
            if time_diff == -1:
                tally_result = tally_result / source_strength
            if time_diff == 1:
                tally_result = tally_result * source_strength
        else:
            raise ValueError(
                f"source_strength is required but currently set to {source_strength}"
            )

    length_diff = check_for_dimentionality_difference(
        base_units, required_units, "[length]"
    )
    if length_diff != 0:
        print("length scaling needed")
        if volume:
            volume = volume * ureg["1 / centimeter ** 3"]
        else:
            # volume required but not provided so it is found from the mesh
            volume = compute_volume_of_voxels(tally, ureg)
        
        if length_diff == -3:
            tally_result = tally_result / volume
        if length_diff == 3:
            tally_result = tally_result * volume

    return tally_result


def compute_volume_of_voxels(tally, ureg):
    tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
    if tally_filter:
        mesh = tally_filter.mesh
        x = abs(mesh.lower_left[0] - mesh.upper_right[0])/mesh.dimension[0]
        y = abs(mesh.lower_left[1] - mesh.upper_right[1])/mesh.dimension[1]
        z = abs(mesh.lower_left[2] - mesh.upper_right[2])/mesh.dimension[2]
        volume = x*y*z
        return volume * ureg["1 / centimeter ** 3"]
    else:
        raise ValueError(f"volume could not be obtained from tally {tally}")

def find_fusion_energy_per_reaction(reactants: str) -> float:
    """Finds the average fusion energy produced per fusion reaction in joules
    from the fuel type.
    Args:
        reactants: the isotopes that are combined in the fusion even. Options
            are "DD" or "DT"
    Returns:
        The average energy of a fusion reaction in Joules
    """

    if reactants == "DT":
        fusion_energy_of_neutron_ev = 14.06 * 1e6
        fusion_energy_of_alpha_ev = 3.52 * 1e6
        fusion_energy_per_reaction_ev = (
            fusion_energy_of_neutron_ev + fusion_energy_of_alpha_ev
        )
    elif reactants == "DD":
        fusion_energy_of_trition_ev = 1.01 * 1e6
        fusion_energy_of_proton_ev = 3.02 * 1e6
        fusion_energy_of_he3_ev = 0.82 * 1e6
        fusion_energy_of_neutron_ev = 2.45 * 1e6
        fusion_energy_per_reaction_ev = (
            0.5 * (fusion_energy_of_trition_ev + fusion_energy_of_proton_ev)
        ) + (0.5 * (fusion_energy_of_he3_ev + fusion_energy_of_neutron_ev))
    else:
        raise ValueError("Only fuel types of DD and DT are currently supported")

    fusion_energy_per_reaction_j = fusion_energy_per_reaction_ev * 1.602176487e-19

    return fusion_energy_per_reaction_j


def find_source_strength(
    fusion_energy_per_second_or_per_pulse=None, reactants="DT"
) -> float:

    fusion_energy_per_reaction_j = find_fusion_energy_per_reaction(reactants)
    number_of_neutrons = (
        fusion_energy_per_second_or_per_pulse / fusion_energy_per_reaction_j
    )
    return number_of_neutrons


def get_particles_from_tally_filters(tally, ureg):
    particles = []
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.ParticleFilter):
            # assumes particle filters bin is a list of 1
            particles.append(filter.bins[0])
    if len(particles) == 0:
        particles = ["particle"]
    units_string = " * ".join(set(particles))
    return ureg(units_string)


def get_cell_ids_from_tally_filters(tally):
    cell_ids = []
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.CellFilter):
            cell_ids.append(filter.bins)
    return cell_ids


def get_tally_units(tally):
    """ """

    if tally.scores == ["flux"]:
        print('score is flux')
        # tally has units of particle-cm2 per simulated_particle
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        units = get_particles_from_tally_filters(tally, ureg)
        units = [units * ureg.centimeter / ureg.simulated_particle]
        for filter in tally.filters:
            if isinstance(filter, openmc.filter.EnergyFilter):
                # spectra tally has units for the energy as well as the flux
                units = [ureg.electron_volt, units[0]]
            if isinstance(filter, openmc.filter.EnergyFunctionFilter):
                print('filter is EnergyFunctionFilter')
                # effective_dose
                # dose coefficients have pico sievert cm **2
                # flux has cm2 / simulated_particle units
                # dose on a surface uses a current score (units of per simulated_particle) and is therefore * area to get pSv / source particle
                # dose on a volume uses a flux score (units of cm2 per simulated particle) and therefore gives pSv cm**4 / simulated particle
                units = [ureg.picosievert * ureg.centimeter * units[0]]

    elif tally.scores == ["heating"]:
        # heating units are eV / simulated_particle
        units = [ureg.electron_volt / ureg.simulated_particle]

    else:
        # return  [1 / ureg.simulated_particle]
        raise ValueError(
            "units for tally can't be found, supported tallies are currently limited"
        )

    return units


def check_for_dimentionality_difference(units_1, units_2, unit_to_compare):
    units_1_time_power = units_1.dimensionality.get(unit_to_compare)
    units_2_time_power = units_2.dimensionality.get(unit_to_compare)
    return units_1_time_power - units_2_time_power


# import pint
# ureg = pint.UnitRegistry()
# diff = check_for_dimentionality_difference_for_time(ureg['cm**2 / s'],ureg['m * s**2']
