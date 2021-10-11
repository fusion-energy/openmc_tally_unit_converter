import openmc_post_processor as opp

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="1_flux")

print("default openmc tally result in base units", my_tally, end="\n\n")

print(opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6))

# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)
print(f"flux base units = {result}", end="\n\n")


# returns the tally with scalled based units (m instead of cm)
result = statepoint.process_tally(
    tally=my_tally, required_units="meter / simulated_particle"
)
print(f"flux scaled base units = {result}", end="\n\n")


# returns the tally with normalisation per pulse
result = statepoint.process_tally(
    source_strength=4.6e17,  # neutrons per 1.3MJ pulse
    tally=my_tally,
    required_units="centimeter / pulse",
)
print(f"flux per pulse = {result}", end="\n\n")


# returns the tally with normalisation for source strength
result = statepoint.process_tally(
    source_strength=5,  # neutrons per second 1e9Gw
    tally=my_tally,
    required_units="centimeter / second",
)
print(f"flux per second = {result}", end="\n\n")

# returns the tally with normalisation for source strength
result = statepoint.process_tally(
    source_strength=5,  # neutrons per 1.3MJ pulse
    tally=my_tally,
    required_units="centimeter / pulse",
)
print(f"flux per pulse = {result}", end="\n\n")

# returns the tally with normalisation for volume
result = statepoint.process_tally(
    # source_strength=1e9,
    volume=100,
    tally=my_tally,
    required_units="1 / centimeter ** 2",
)
print(f"flux per second = {result}", end="\n\n")
