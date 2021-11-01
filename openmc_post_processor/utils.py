from pathlib import Path
from typing import Tuple

import numpy as np
import openmc
import pint

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))


def process_spectra_tally(
    tally,
    required_units: str = "centimeters / simulated_particle",
    required_energy_units: str = 'eV',
    source_strength: float = None,
    volume: float = None,
) -> tuple:
    """Processes a spectra tally converting the tally with default units
    obtained during simulation into the user specified units.

    Args:
        tally: The openmc.Tally object which should be a spectra tally. With a
            score of flux or current and an EnergyFilter
        required_units: A tuple of the units to convert the energy and tally
            into
        source_strength: In some cases the source_strength will be required
            to convert the base units into the required units. This optional
            argument allows the user to specify the source_strength when needed
        volume: In some cases the volume will be required to convert the base
            units into the required units. In the case of a regular mesh the
            volume is automatically found. This optional argument allows the
            user to specify the volume when needed or overwrite the
            automatically calculated volume.

    Returns:
        Tuple of spectra energies and tally results
    """

    if not check_for_energy_filter(tally):
        raise ValueError('EnergyFilter was not found in spectra tally')

    if check_for_energy_function_filter(tally):
        raise ValueError('EnergyFunctionFilter was found in spectra tally')

    data_frame = tally.get_pandas_dataframe()

    # checks for user provided base units
    base_units = get_tally_units(tally)
    print(f"tally {tally.name} base units {base_units}")

    # numpy array is needed as a pandas series can't have units

    energy_base = np.array(data_frame["energy low [eV]"]) * ureg.electron_volt
    energy_in_required_units = energy_base.to(required_energy_units)

    tally_base = np.array(data_frame["mean"]) * base_units
    scaled_tally_result = scale_tally(
        tally,
        tally_base,
        base_units,
        ureg[required_units],
        source_strength,
        volume,
    )
    tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in data_frame.columns.to_list():
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        scaled_tally_std_dev = scale_tally(
            tally,
            tally_std_dev_base,
            base_units,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_std_dev_in_required_units = scaled_tally_std_dev.to(required_units)
    
        return energy_in_required_units, tally_in_required_units, tally_std_dev_in_required_units

    else:

        return energy_in_required_units, tally_in_required_units


def process_dose_tally(
    tally,
    required_units: str = 'picosievert cm **2 / simulated_particle',
    source_strength: float = None,
    volume: float = None,
):
    """Processes a dose tally converting the tally with default units
    obtained during simulation into the user specified units.

    Args:
        tally: The openmc.Tally object which should be a spectra tally. With a
            score of flux or current and an EnergyFunctionFilter
        required_units: The units to convert the energy and tally into
        source_strength: In some cases the source_strength will be required
            to convert the base units into the required units. This optional
            argument allows the user to specify the source_strength when needed
        volume: In some cases the volume will be required to convert the base
            units into the required units. In the case of a regular mesh the
            volume is automatically found. This optional argument allows the
            user to specify the volume when needed or overwrite the
            automatically calculated volume.

    Returns:
        The dose tally result in the required units
    """

    if not check_for_energy_function_filter(tally):
        raise ValueError('EnergyFunctionFilter was not found in dose tally')

    # checks for user provided base units
    base_units = get_tally_units(tally)
    base_units = ureg.picosievert * ureg.centimeter * base_units

    data_frame = tally.get_pandas_dataframe()

    print(f"tally {tally.name} base units {base_units}")

    tally_result = np.array(data_frame["mean"]) * base_units

    scaled_tally_result = scale_tally(
        tally,
        tally_result,
        base_units,
        ureg[required_units],
        source_strength,
        volume,
    )
    tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in data_frame.columns.to_list():
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        scaled_tally_std_dev = scale_tally(
            tally,
            tally_std_dev_base,
            base_units,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_std_dev_in_required_units = scaled_tally_std_dev.to(required_units)
        return tally_in_required_units, tally_std_dev_in_required_units
    else:
        return tally_in_required_units


def process_tally(
    tally,
    required_units: str,
    source_strength: float = None,
    volume: float = None,
):
    """Processes a tally converting the tally with default units obtained
     during simulation into the user specified units.

    Args:
        tally: The openmc.Tally object to convert the units of
        required_units: The units to convert the energy and tally into
        source_strength: In some cases the source_strength will be required
            to convert the base units into the required units. This optional
            argument allows the user to specify the source_strength when needed
        volume: In some cases the volume will be required to convert the base
            units into the required units. In the case of a regular mesh the
            volume is automatically found. This optional argument allows the
            user to specify the volume when needed or overwrite the
            automatically calculated volume.

    Returns:
        The dose tally result in the required units
    """

    if check_for_energy_function_filter(tally):
        msg = (
            "An EnergyFunctionFilter was found in the tally. This "
            "modifies the tally units and the base units of the"
            "EnergyFunctionFilter are not known to OpenMC. Therefore "
            "the units of this tally can not be found. If you have "
            "applied dose coefficients to an EnergyFunctionFilter "
            "the units of these are known and yo can use the "
            "get_tally_units_dose function instead of the "
            "get_tally_units"
        )
        raise ValueError(msg)

    data_frame = tally.get_pandas_dataframe()

    base_units = get_tally_units(tally)

    print(f"tally {tally.name} base units {base_units}")

    tally_result = np.array(data_frame["mean"]) * base_units

    scaled_tally_result = scale_tally(
        tally,
        tally_result,
        base_units,
        ureg[required_units],
        source_strength,
        volume,
    )
    tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in data_frame.columns.to_list():
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        scaled_tally_std_dev = scale_tally(
            tally,
            tally_std_dev_base,
            base_units,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_std_dev_in_required_units = scaled_tally_std_dev.to(required_units)

        return tally_in_required_units, tally_std_dev_in_required_units

    else:

        return tally_in_required_units


def scale_tally(
    tally,
    tally_result,
    base_units,
    required_units,
    source_strength: float,
    volume: float
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
            volume = volume * ureg["centimeter ** 3"]
        else:
            # volume required but not provided so it is found from the mesh
            volume = compute_volume_of_voxels(tally) * ureg["centimeter ** 3"]

        if length_diff == 3:
            print("dividing by volume")
            tally_result = tally_result / volume
        if length_diff == -3:
            print("multiplying by volume")
            tally_result = tally_result * volume

    return tally_result


def compute_volume_of_voxels(tally):
    tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
    if tally_filter:
        mesh = tally_filter.mesh
        x = abs(mesh.lower_left[0] - mesh.upper_right[0]) / mesh.dimension[0]
        y = abs(mesh.lower_left[1] - mesh.upper_right[1]) / mesh.dimension[1]
        z = abs(mesh.lower_left[2] - mesh.upper_right[2]) / mesh.dimension[2]
        volume = x * y * z
        return volume
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


# def get_tally_units_dose(tally):

#     # An EnergyFunctionFilter is exspeted in dose tallies
#     units = get_tally_units(tally)

#     units = [ureg.picosievert * ureg.centimeter * units[0]]

#     # check it is a dose tally by looking for a openmc.filter.EnergyFunctionFilter
#     for filter in tally.filters:
#         if isinstance(filter, openmc.filter.EnergyFunctionFilter):
#             print("filter is EnergyFunctionFilter")
#             # effective_dose
#             # dose coefficients have pico sievert cm **2
#             # flux has cm2 / simulated_particle units
#             # dose on a surface uses a current score (units of per simulated_particle) and is therefore * area to get pSv / source particle
#             # dose on a volume uses a flux score (units of cm2 per simulated particle) and therefore gives pSv cm**4 / simulated particle
            
#             return units

#     raise ValueError(
#         "units for dose tally can't be found, an EnergyFunctionFilter was not present"
#     )

def check_for_energy_filter(tally):

    # check it is a spectra tally by looking for a openmc.filter.EnergyFilter
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFilter):
            # spectra tally has units for the energy as well as the flux
            return True
    return False

    # raise ValueError(
    #     "units for spectra tally can't be found, an EnergyFilter was not present"
    # )


def check_for_energy_function_filter(tally):
    # check for EnergyFunctionFilter which modify the units of the tally
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFunctionFilter):
            return True
    return False


def get_tally_units(tally):
    """ """

    if tally.scores == ["current"]:
        units = get_particles_from_tally_filters(tally, ureg)
        units = units / (ureg.simulated_particle * ureg.centimeter ** 2)

    if tally.scores == ["flux"]:
        print("score is flux")
        # tally has units of particle-cm2 per simulated_particle
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        units = get_particles_from_tally_filters(tally, ureg)
        units = units * ureg.centimeter / ureg.simulated_particle

    elif tally.scores == ["heating"]:
        # heating units are eV / simulated_particle
        units = ureg.electron_volt / ureg.simulated_particle

    elif tally.scores == ["damage-energy"]:
        # damage-energy units are eV / simulated_particle
        units = ureg.electron_volt / ureg.simulated_particle

    else:
        msg = ("units for tally can't be found. Tallies that are supported "
               "by get_tally_units function are those with scores of current, "
               "flux, heating, damage-energy")
        raise ValueError(msg)

    return units


def check_for_dimentionality_difference(units_1, units_2, unit_to_compare):
    units_1_time_power = units_1.dimensionality.get(unit_to_compare)
    units_2_time_power = units_2.dimensionality.get(unit_to_compare)
    return units_1_time_power - units_2_time_power
