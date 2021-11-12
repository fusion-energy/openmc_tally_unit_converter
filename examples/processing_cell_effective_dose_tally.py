import openmc
import openmc_tally_unit_converter as otuc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_neutron_effective_dose")


# returns the tally with base units
result = otuc.process_dose_tally(tally=my_tally)
print(f"effective dose base units = {result}", end="\n\n")


# returns the tally with scalled based units (MeV instead of eV)
result = otuc.process_dose_tally(
    tally=my_tally, required_units="sievert cm **2 / simulated_particle"
)
print(f"effective dose scaled base units = {result}", end="\n\n")


# returns the tally with normalisation per pulse
result = otuc.process_dose_tally(
    source_strength=1.3e6, tally=my_tally, required_units="sievert cm **2 / pulse"
)
print(f"effective dose per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength
otuc.process_dose_tally(
    source_strength=1.3e6, tally=my_tally, required_units="Sv cm **2 / second"
)
print(f"effective dose per second = {result}", end="\n\n")
