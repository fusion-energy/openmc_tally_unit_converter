import openmc
import openmc_tally_unit_converter as otuc


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="heating_on_2D_mesh_xy")


# returns the tally with base units
result = otuc.get_tally_units(
    tally=my_tally,
)
# the tally result with base units which should be eV per simulated particle
print(f"The base tally units for this heating tally are {result}")


# scaled from picosievert to sievert
result = otuc.process_tally(
    tally=my_tally,
    required_units="watts / meter ** 3",
    source_strength=1e21,  # number of neutrons per second emitted by the source
)

print("mesh results with new units", result)
