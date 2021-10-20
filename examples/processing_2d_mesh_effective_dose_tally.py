import openmc
import openmc_post_processor as opp


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")


# returns the tally with base units
result = opp.process_dose_tally(
    tally=my_tally,
)
# the tally result with required units
print(result)


# scaled from picosievert to sievert
result = opp.process_dose_tally(
    tally=my_tally,
    required_units="sievert cm **2 / simulated_particle"
)
# the tally result with required units
print(result)
