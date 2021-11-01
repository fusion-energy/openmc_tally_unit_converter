import openmc
import openmc_post_processor as opp


# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_neutron_spectra")


# returns the tally with base units
result = opp.process_spectra_tally(
    tally=my_tally,
)
print(f"spectra with base units = {result}", end="\n\n")

# returns the tally with base units
result = opp.process_spectra_tally(
    tally=my_tally,
    required_units="centimeter",
    required_energy_units="MeV",
)
print(f"spectra with base units = {result}", end="\n\n")


# returns the tally with normalisation per pulse
result = opp.process_spectra_tally(
    tally=my_tally,
    required_units="centimeter / pulse",
    required_energy_units="eV",
    source_strength=1.3e6,
)
print(f"spectra per pulse = {result}", end="\n\n")


# returns the tally scalled and normalisation for source strength
print(f"spectra per second = {result}", end="\n\n")
result = opp.process_spectra_tally(
    tally=my_tally,
    required_units="centimeter / second",
    required_energy_units="MeV",
    source_strength=1e9,
)
print(f"spectra per pulse = {result}", end="\n\n")
