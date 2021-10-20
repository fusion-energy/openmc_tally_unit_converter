import openmc
import openmc_post_processor as opp


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")


# returns the tally with base units
result = opp.process_tally(
    tally=my_tally,
)


# scaled from picosievert to sievert
result = opp.process_tally(
    tally=my_tally,
    required_units="sievert cm **2 / simulated_particle"
)


# scaled from picosievert to sievert and normalised per pulse of 1.3e6 neutrons
result = opp.process_tally(
    tally=my_tally,
    source_strength=1.3e6,
    required_units="sievert cm **2 / pulse"
)

# scaled by mesh voxel volume and normalised per pulse of 1.3e6 neutrons
result = statepoint.process_tally(
    tally=my_tally,
    source_strength=1.3e6,
    required_units="picosievert / cm / pulse",
)

# the tally result with required units
print(result)
