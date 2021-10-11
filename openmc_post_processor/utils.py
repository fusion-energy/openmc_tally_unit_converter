import openmc


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


def get_tally_units(tally, ureg):
    """ """

    if tally.scores == ["flux"]:
        # tally has units of particle-cm2 per simulated_particle
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        units = get_particles_from_tally_filters(tally, ureg)
        units = [units * ureg.centimeter / ureg.simulated_particle]
        for filter in tally.filters:
            if isinstance(filter, openmc.filter.EnergyFilter):
                # spectra tally has units for the energy as well as the flux
                units = [ureg.electron_volt, units[0]]
            if isinstance(filter, openmc.filter.EnergyFunctionFilter):
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
