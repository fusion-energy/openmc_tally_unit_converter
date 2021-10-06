


def find_fusion_energy_per_reaction(reactants: str) -> float:
    """Finds the average fusion energy produced per fusion reaction in joules
    from the fule type.
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

# import pint


# def find_fusion_energy_per_reaction(reactants: str) -> float:
#     """Finds the average fusion energy produced per fusion reaction in
#     joules from the fuel type.
#     Args:
#         reactants: the isotopes that are combined in the fusion even.
#             Options are "DD" or "DT"
#     Returns:
#         The average energy of a fusion reaction in Joules
#     """



#     if reactants == "DT":
#         fusion_energy_of_neutron_ev = 14.06 * 1e6 * ureg.electron_volt
#         fusion_energy_of_alpha_ev = 3.52 * 1e6 * ureg.electron_volt
#         fusion_energy_per_reaction_ev = (
#             fusion_energy_of_neutron_ev + fusion_energy_of_alpha_ev
#         )
#     elif reactants == "DD":
#         fusion_energy_of_trition_ev = 1.01 * 1e6 * ureg.electron_volt
#         fusion_energy_of_proton_ev = 3.02 * 1e6 * ureg.electron_volt
#         fusion_energy_of_he3_ev = 0.82 * 1e6 * ureg.electron_volt
#         fusion_energy_of_neutron_ev = 2.45 * 1e6 * ureg.electron_volt
#         fusion_energy_per_reaction_ev = (
#             0.5 * (fusion_energy_of_trition_ev + fusion_energy_of_proton_ev)
#         ) + (0.5 * (fusion_energy_of_he3_ev + fusion_energy_of_neutron_ev))
#     else:
#         raise ValueError(
#             "Only fuel types of DD and DT are currently supported")

#     fusion_energy_per_reaction_j = fusion_energy_per_reaction_ev.to('joules')

#     return fusion_energy_per_reaction_j