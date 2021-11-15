import openmc_tally_unit_converter as otuc
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_flux")

# print(otuc.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6))

# returns the tally with base units
result = otuc.process_tally(
    tally=my_tally, required_units="centimeter / simulated_particle"
)
print(f"flux base units = {result[0].units}", end="\n\n")


# returns the tally with scalled based units (m instead of cm)
result = otuc.process_tally(
    tally=my_tally, required_units="centimeter * particle / simulated_particle"
)
print(f"flux scaled base units = {result[0].units}", end="\n\n")


# returns the tally with normalisation per pulse
result = otuc.process_tally(
    source_strength=4.6e17,  # neutrons per 1.3MJ pulse
    tally=my_tally,
    required_units="centimeter / pulse",
)
print(f"flux per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength
result = otuc.process_tally(
    source_strength=5,  # neutrons per second 1e9Gw
    tally=my_tally,
    required_units="centimeter / second",
)
print(f"flux per second = {result}", end="\n\n")

# returns the tally with normalisation for source strength
result = otuc.process_tally(
    source_strength=5,  # neutrons per 1.3MJ pulse
    tally=my_tally,
    required_units="centimeter / pulse",
)
print(f"flux per pulse = {result}", end="\n\n")

# returns the tally with normalisation for volume
result = otuc.process_tally(
    volume=100,
    tally=my_tally,
    required_units="1 / centimeter ** 2",
)
print(f"flux per second = {result}", end="\n\n")
