import openmc_post_processor as opp


# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="1_neutron_effective_dose")


# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)
print(f"effective dose base units = {result}", end="\n\n")


# returns the tally with scalled based units (MeV instead of eV)
result = statepoint.process_tally(
    tally=my_tally, required_units="sievert cm **2 / simulated_particle"
)
print(f"effective dose scaled base units = {result}", end="\n\n")


# returns the tally with normalisation per pulse
result = statepoint.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="sievert cm **2 / pulse"
)
print(f"effective dose per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength
statepoint.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="Sv cm **2 / second"
)
print(f"effective dose per second = {result}", end="\n\n")


# # returns the tally with normalisation per pulse and conversion to joules
# result = statepoint.process_tally(
#     fusion_energy_per_pulse=1.3e6,
#     tally=my_tally,
#     required_units='joules / pulse'
# )
# print(f'effective dose per pulse = {result}', end='\n\n')


# # returns the tally with normalisation for source strength and conversion to joules
# result = statepoint.process_tally(
#     fusion_power=1e9,
#     tally=my_tally,
#     required_units='joules / second'
# )
# print(f'effective dose per second = {result}', end='\n\n')
