import openmc
import openmc_post_processor as opp


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="heating_on_3D_mesh")


# returns the tally with base units
result = opp.get_tally_units(
    tally=my_tally,
)
# the tally result with base units which should be eV per simulated particle
print(f'The base tally units for this heating tally are {result}')

# this finds the number of neutrons emitted per second by a 1GW fusion DT plasma
source_strength = opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1e9, reactants='DT')

# scaled from picosievert to sievert
result = opp.process_tally(
    tally=my_tally,
    required_units="watts / meter ** 3",
    source_strength=source_strength  # number of neutrons per second emitted by the source
)

print('mesh results with new units' ,result)
