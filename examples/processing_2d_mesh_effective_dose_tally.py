import openmc
import openmc_tally_unit_converter as otuc


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")


# returns the tally with base units
tally_result, std_dev_result  = otuc.process_dose_tally(
    tally=my_tally,
)
# the tally result with base units
print(f'mesh tally results {tally_result}', end='\n\n')


# scaled from picosievert to sievert
tally_result, std_dev_result  = otuc.process_dose_tally(
    tally=my_tally, required_units="sievert / simulated_particle"
)
# the tally result with required units
print(f'converted mesh tally results {tally_result}')
