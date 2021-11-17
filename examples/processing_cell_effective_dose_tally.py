import openmc
import openmc_tally_unit_converter as otuc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_neutron_effective_dose")

# returns the tally with base units
tally_result, std_dev_result = otuc.process_dose_tally(tally=my_tally)
print(f"effective dose tally = {tally_result}", end="\n\n")


# returns the tally with scalled based units (MeV instead of eV)
tally_result, std_dev_result = otuc.process_dose_tally(
    tally=my_tally, required_units="sievert / source_particle"
)
print(f"effective dose scaled base units = {tally_result}", end="\n\n")


# returns the tally with normalisation per pulse
tally_result, std_dev_result = otuc.process_dose_tally(
    source_strength=1.3e6, tally=my_tally, required_units="sievert / pulse"
)
print(f"effective dose per pulse = {tally_result}", end="\n\n")


# returns the tally with normalisation for source strength
tally_result, std_dev_result = otuc.process_dose_tally(
    source_strength=1.3e6, tally=my_tally, required_units="Sv / second"
)
print(f"effective dose per second = {tally_result}", end="\n\n")
