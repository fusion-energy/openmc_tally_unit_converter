from pathlib import Path
from typing import Tuple

import numpy as np
import openmc
import pandas as pd
import pint

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))


def process_damage_energy_tally(
    tally,
    required_units: str = None,
    source_strength: float = None,
    volume: float = None,
    energy_per_displacement: float = None,
    recombination_fraction: float = 0,
    material: float = None,
):
    """Processes a damage-energy tally converting the tally with default units
    obtained during simulation into the user specified units. Can be processed
    to obtain damage per atom (DPA). Base units are  'eV / source_particle'

    Args:
        tally: The openmc.Tally object which should be a spectra tally. With a
            score of flux or current and an EnergyFunctionFilter
        required_units: The units to convert the energy and tally into.
        source_strength: In some cases the source_strength will be required
            to convert the base units into the required units. This optional
            argument allows the user to specify the source_strength when needed
        volume: In some cases the volume will be required to convert the base
            units into the required units. In the case of a regular mesh the
            volume is automatically found. This optional argument allows the
            user to specify the volume when needed or overwrite the
            automatically calculated volume. When finding DPA volume is needed
            along with the material to find number of atoms.
        energy_per_displacement: the energy required to displace an atom. The
            total damage-energy depositied is divided by this value to get
            number of atoms displaced. Assumed units are eV

    Returns:
        The dpa tally result in the required units
    """

    if check_for_energy_function_filter(tally):
        raise ValueError("EnergyFunctionFilter found in a damage-energy tally")

    # checks for user provided base units
    base_units = get_score_units(tally)

    data_frame = tally.get_pandas_dataframe()

    tally_result = np.array(data_frame["mean"])

    if recombination_fraction:
        if recombination_fraction < 0:
            raise ValueError(
                f"recombination_fraction can't be smaller than 1. recombination_fraction is {recombination_fraction}"
            )
        if recombination_fraction > 1:
            raise ValueError(
                f"recombination_fraction can't be larger than 1. recombination_fraction is {recombination_fraction}"
            )

        tally_result = tally_result * (1.0 - recombination_fraction)

    tally_result = tally_result * base_units

    if material:
        atomic_mass_in_g = material.average_molar_mass * 1.66054e-24
        density_in_g_per_cm3 = material.get_mass_density()
        number_of_atoms_per_cm3 = density_in_g_per_cm3 / atomic_mass_in_g
    else:
        number_of_atoms_per_cm3 = None

    if required_units is None:
        tally_in_required_units = tally_result
    else:
        scaled_tally_result = scale_tally(
            tally,
            tally_result,
            ureg[required_units],
            source_strength,
            volume,
            number_of_atoms_per_cm3,
            energy_per_displacement,
        )

        tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in get_data_frame_columns(data_frame):
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        if required_units is None:
            tally_std_dev_in_required_units = tally_std_dev_base
        else:
            scaled_tally_std_dev = scale_tally(
                tally,
                tally_std_dev_base,
                ureg[required_units],
                source_strength,
                volume,
                number_of_atoms_per_cm3,
                energy_per_displacement,
            )
            tally_std_dev_in_required_units = scaled_tally_std_dev.to(required_units)

        # TODO add recombination_fraction scaling
        # if recombination_fraction:
        #     scaled_tally_std_dev = scaled_tally_std_dev * recombination_fraction
        return tally_in_required_units, tally_std_dev_in_required_units
    else:
        return tally_in_required_units


def process_spectra_tally(
    tally,
    required_units: str = None,
    required_energy_units: str = "eV",
    source_strength: float = None,
    volume: float = None,
) -> tuple:
    """Processes a spectra tally converting the tally with default units
    obtained during simulation into the user specified units. Base units are
    'centimeters / source_particle'

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
        raise ValueError("EnergyFilter was not found in spectra tally")

    if check_for_energy_function_filter(tally):
        raise ValueError("EnergyFunctionFilter was found in spectra tally")

    data_frame = tally.get_pandas_dataframe()

    # checks for user provided base units
    base_units = get_score_units(tally)

    # numpy array is needed as a pandas series can't have units

    energy_base = np.array(data_frame["energy low [eV]"]) * ureg.electron_volt
    energy_in_required_units = energy_base.to(required_energy_units)

    tally_result = np.array(data_frame["mean"]) * base_units
    if required_units is None:
        tally_in_required_units = tally_result
    else:
        scaled_tally_result = scale_tally(
            tally,
            tally_result,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in get_data_frame_columns(data_frame):
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        if required_units is None:
            tally_std_dev_in_required_units = tally_std_dev_base
        else:
            scaled_tally_std_dev = scale_tally(
                tally,
                tally_std_dev_base,
                ureg[required_units],
                source_strength,
                volume,
            )
            tally_std_dev_in_required_units = scaled_tally_std_dev.to(required_units)

        return (
            energy_in_required_units,
            tally_in_required_units,
            tally_std_dev_in_required_units,
        )

    else:

        return energy_in_required_units, tally_in_required_units


def process_dose_tally(
    tally,
    required_units: str = None,
    source_strength: float = None,
    volume: float = None,
):
    """Processes a dose tally converting the tally with default units
    obtained during simulation into the user specified units. Base units are
    'picosievert / source_particle'

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
        raise ValueError("EnergyFunctionFilter was not found in dose tally")

    # checks for user provided base units
    base_units = get_score_units(tally)
    base_units = base_units * ureg.picosievert * ureg.centimeter ** 2

    # dose coefficients are flux to does coefficients and have units of [pSv*cm^2]
    # flux has [particles*cm/source particle] units
    # dose on a volume uses a flux score and the EnergyFunctionFilter with dose coefficients
    # dose on a volume has [pSv*cm^3/source_particle] units

    data_frame = tally.get_pandas_dataframe()

    tally_result = np.array(data_frame["mean"]) * base_units

    if required_units is None:
        tally_in_required_units = tally_result
    else:
        scaled_tally_result = scale_tally(
            tally,
            tally_result,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in get_data_frame_columns(data_frame):
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        if required_units is None:
            tally_std_dev_in_required_units = tally_std_dev_base
        else:
            scaled_tally_std_dev = scale_tally(
                tally,
                tally_std_dev_base,
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
    required_units: str = None,
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
            "the units of these are known and you can use the "
            "process_dose_tally function instead of the process_tally"
        )
        raise ValueError(msg)

    data_frame = tally.get_pandas_dataframe()

    base_units = get_score_units(tally)

    tally_result = np.array(data_frame["mean"]) * base_units

    if required_units is None:
        tally_in_required_units = tally_result
    else:
        scaled_tally_result = scale_tally(
            tally,
            tally_result,
            ureg[required_units],
            source_strength,
            volume,
        )
        tally_in_required_units = scaled_tally_result.to(required_units)

    if "std. dev." in get_data_frame_columns(data_frame):
        tally_std_dev_base = np.array(data_frame["std. dev."]) * base_units
        if required_units is None:
            tally_std_dev_in_required_units = tally_std_dev_base
        else:
            scaled_tally_std_dev = scale_tally(
                tally,
                tally_std_dev_base,
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
    required_units: str,
    source_strength: float,
    volume: float,
    atoms: float = None,
    energy_per_displacement: float = None,
):

    # energy_per_displacement
    time_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[time]"
    )
    length_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[length]"
    )
    mass_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[mass]"
    )
    displacement_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[displacements]"
    )

    if (
        time_diff == -2
        and mass_diff == 1
        and length_diff == 2
        and displacement_diff == -1
    ):

        if energy_per_displacement:
            energy_per_displacement = (
                energy_per_displacement * ureg.electron_volt / ureg["displacements"]
            )
            tally_result = tally_result / energy_per_displacement
        else:
            raise ValueError(
                f"energy_per_displacement is required but currently set to {energy_per_displacement}"
            )

    # per_displacement
    displacement_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[displacements]"
    )
    if displacement_diff == -1:
        if energy_per_displacement:
            energy_per_displacement = (
                energy_per_displacement * ureg.electron_volt / ureg["displacements"]
            )
            tally_result = tally_result / energy_per_displacement
        else:
            raise ValueError(
                f"energy_per_displacement is required but currently set to {energy_per_displacement}"
            )

    time_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[time]"
    )
    if time_diff != 0:
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
        tally_result.units, required_units, "[pulse]"
    )
    if time_diff != 0:
        if source_strength:
            source_strength = source_strength * ureg["1 / pulse"]
            if time_diff == -1:
                tally_result = tally_result / source_strength
            elif time_diff == 1:
                tally_result = tally_result * source_strength
        else:
            raise ValueError(
                f"source_strength is required but currently set to {source_strength}"
            )

    length_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[length]"
    )
    if length_diff != 0:
        if volume:
            volume_with_units = volume * ureg["centimeter ** 3"]
        else:
            # volume required but not provided so it is found from the mesh
            volume_from_mesh = compute_volume_of_voxels(tally)

            if volume_from_mesh:
                volume_with_units = volume_from_mesh * ureg["centimeter ** 3"]
            else:
                msg = (
                    f"A length dimentionality difference of {length_diff} "
                    f"was detected. However volume is set to {volume} and "
                    "volume could not be calculated from the mesh. Please "
                    "specify the volume argument"
                )
                raise ValueError(msg)

        if length_diff == 3:
            tally_result = tally_result / volume_with_units
        elif length_diff == -3:
            tally_result = tally_result * volume_with_units

    atom_diff = check_for_dimentionality_difference(
        tally_result.units, required_units, "[atom]"
    )
    if atom_diff != 0:
        if atoms:
            atoms = atoms * ureg["atom"]

            if atom_diff == 1:
                tally_result = tally_result / atoms
            elif atom_diff == -1:
                tally_result = tally_result * atoms

        else:
            msg = (
                f"atoms is required but currently set to {atoms}. Atoms "
                "can be calculated automatically from material and volume "
                "inputs"
            )
            raise ValueError(msg)
    return tally_result


def compute_volume_of_voxels(tally):
    """Finds the volume of the rectangular voxels that make up a Regular mesh
    tally."""
    if tally.contains_filter(openmc.MeshFilter):
        tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)

        mesh = tally_filter.mesh
        x = abs(mesh.lower_left[0] - mesh.upper_right[0]) / mesh.dimension[0]
        y = abs(mesh.lower_left[1] - mesh.upper_right[1]) / mesh.dimension[1]
        z = abs(mesh.lower_left[2] - mesh.upper_right[2]) / mesh.dimension[2]
        volume = x * y * z
        return volume
    else:
        print(f"volume of mesh element could not be obtained from tally {tally}")
        return False


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


def check_for_energy_filter(tally):

    # check it is a spectra tally by looking for a openmc.filter.EnergyFilter
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFilter):
            # spectra tally has units for the energy as well as the flux
            return True
    return False


def check_for_energy_function_filter(tally):
    # check for EnergyFunctionFilter which modify the units of the tally
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFunctionFilter):
            return True
    return False


def get_score_units(tally):
    """Finds the tally score from the supported scores. Then finds the units
    that the score results in"""

    if tally.scores == ["current"]:
        units = get_particles_from_tally_filters(tally, ureg)
        units = units / (ureg.source_particle)

    elif tally.scores == ["flux"]:
        # tally has units of particle-cm2 per source_particle
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        units = get_particles_from_tally_filters(tally, ureg)
        units = units * ureg.centimeter / ureg.source_particle

    elif tally.scores == ["heating"]:
        # heating units are eV / source_particle
        units = ureg.electron_volt / ureg.source_particle

    elif tally.scores == ["heating-local"]:
        # heating-local units are eV / source_particle
        units = ureg.electron_volt / ureg.source_particle

    elif tally.scores == ["damage-energy"]:
        # damage-energy units are eV / source_particle
        units = ureg.electron_volt / ureg.source_particle

    else:
        msg = (
            "units for tally can't be found. Tallies that are supported "
            "by get_score_units function are those with scores of current, "
            "flux, heating, heating-local, damage-energy"
        )
        raise ValueError(msg)

    return units


def check_for_dimentionality_difference(units_1, units_2, unit_to_compare):
    units_1_dimentions = units_1.dimensionality.get(unit_to_compare)
    units_2_dimentions = units_2.dimensionality.get(unit_to_compare)
    return units_1_dimentions - units_2_dimentions


def get_data_frame_columns(data_frame):
    if isinstance(data_frame.columns, pd.MultiIndex):
        data_frame_columns = data_frame.columns.get_level_values(0).to_list()
    else:
        data_frame_columns = data_frame.columns.to_list()
    return data_frame_columns
