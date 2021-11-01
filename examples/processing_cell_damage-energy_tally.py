import openmc_post_processor as opp
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_damage-energy")


# returns the tally with base units
result = opp.process_tally(
    tally=my_tally,
    required_units='eV / simulated_particle'
)
print(f"damage-energy base units = {result}", end="\n\n")


# returns the tally with scalled based units (MeV instead of eV)
result, std_dev = opp.process_tally(tally=my_tally, required_units="MeV / simulated_particle")
print(f"damage-energy scaled base units = {result}", end="\n\n")
