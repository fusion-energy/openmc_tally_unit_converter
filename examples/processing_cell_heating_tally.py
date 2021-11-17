import openmc_tally_unit_converter as otuc
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_heating")


# returns the tally with base units
result = otuc.process_tally(tally=my_tally, required_units="eV / source_particle")
print(f"heating base units = {result}", end="\n\n")


# returns the tally with scalled based units (MeV instead of eV)
result = otuc.process_tally(tally=my_tally, required_units="MeV / source_particle")
print(f"heating scalled base units = {result}", end="\n\n")


# returns the tally with normalisation per pulse
result = otuc.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="MeV / pulse"
)
print(f"heating per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength
otuc.process_tally(source_strength=1e9, tally=my_tally, required_units="MeV / second")
print(f"heating per second = {result}", end="\n\n")


# returns the tally with normalisation per pulse and conversion to joules
result = otuc.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="joules / pulse"
)
print(f"heating per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength and conversion to joules
result = otuc.process_tally(
    source_strength=1e9, tally=my_tally, required_units="joules / second"
)
print(f"heating per second = {result}", end="\n\n")
