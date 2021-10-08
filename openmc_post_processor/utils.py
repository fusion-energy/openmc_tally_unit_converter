
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
        raise ValueError(
            "Only fuel types of DD and DT are currently supported")

    fusion_energy_per_reaction_j = fusion_energy_per_reaction_ev * 1.602176487e-19

    return fusion_energy_per_reaction_j

def get_particle_from_tally_filters(tally):
    for filter in tally.filters:
        if isinstance(filter, openmc.filter.EnergyFilter):

def get_tally_units(tally):
    """
    """

    # could be used to find particle
    # for filter in tally.filters:
    #     if isinstance(filter, openmc.filter.ParticleFilter):
    #         particle = filter.bins

    # could be used to find cells and then volume
    # for filter in tally.filters:
    #     if isinstance(filter, openmc.filter.CellFilter):
    #         cells = filter.bins

    # todo add logic that assigns Pint units to a tally
    # this can be ascertained by the tally filters / scores
    # as a first pass the tally.name can be used

    if tally.scores == ['flux']:
        units = ureg.centimeter / ureg.simulated_particle

    if 'heating' in tally.name:
        # 'electron_volt / simulated_particle'
        units = ureg.electron_volt / ureg.simulated_particle



    if 'effective_dose' in tally.name:
        # dose coefficients have pico sievert cm **2
        # flux has cm2 / simulated_particle units
        # dose on a surface uses a current score (units of per simulated_particle) and is therefore * area to get pSv / source particle
        # dose on a volume uses a flux score (units of cm2 per simulated particle) and therefore gives pSv cm**4 / simulated particle
        return [ureg.picosievert * ureg.centimeter **2 / ureg.simulated_particle]

    if 'neutron_flux' in tally.name:
        # tally has units of cm2 per simulated_particle
        # discussion on openmc units of flux
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        return [ureg.neutrons * ureg.centimeter / ureg.simulated_particle]

    if 'photon_flux' in tally.name:
        # tally has units of cm2 per simulated_particle
        # discussion on openmc units of flux
        # https://openmc.discourse.group/t/normalizing-tally-to-get-flux-value/99/4
        return [ureg.photon * ureg.centimeter / ureg.simulated_particle]

    if 'spectra' in tally.name:
        # tally (flux) has units of cm2 per simulated_particle
        # energy has units of electron volt
        return [ureg.electron_volt, ureg.centimeter / ureg.simulated_particle]

    # TODO damage-energy units of eV per source particle

    else:
        # default tallies are per simulated_particle
        return [1 / ureg.simulated_particle]