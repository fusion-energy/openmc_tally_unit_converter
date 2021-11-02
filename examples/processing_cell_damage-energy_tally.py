import openmc_post_processor as opp
import openmc

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name="2_damage-energy")


# # returns the tally with base units
# result = opp.process_damage_energy_tally(
#     tally=my_tally,
#     required_units='eV / simulated_particle'
# )
# print(f"damage-energy base units = {result}", end="\n\n")


# # returns the tally with scalled based units (MeV instead of eV)
# result, std_dev = opp.process_damage_energy_tally(
#     tally=my_tally,
#     required_units="MeV / simulated_particle"
#     # required_units="displacements per atoms"
# )
# print(f"damage-energy scaled base units = {result}", end="\n\n")

# # returns the tally with scalled based units (MeV instead of eV)
# result, std_dev = opp.process_damage_energy_tally(
#     tally=my_tally,
#     required_units="MeV",
#     source_strength=1,
# )
# print(f"damage-energy scaled base units = {result}", end="\n\n")

# returns the tally with scalled based units (MeV instead of eV)

my_mat = openmc.Material()
my_mat.add_element("Fe", 1)
my_mat.set_density("g/cm3", 1)

# result, std_dev = opp.process_damage_energy_tally(
#     tally=my_tally,
#     required_units="MeV per atom",
#     source_strength=1,
#     volume=5,
#     material=my_mat,
# )
# print(f"damage-energy scaled base units = {result}", end="\n\n")

# result, std_dev = opp.process_damage_energy_tally(
#     tally=my_tally,
#     required_units="displacements",
#     source_strength=1,
#     volume=5,
#     material=my_mat,
#     energy_per_displacement=10,
#     recombination_fraction=0.1
# )
# print(f"damage-energy = {result}", end="\n\n")

result, std_dev = opp.process_damage_energy_tally(
    tally=my_tally,
    required_units="displacements per pulse",
    source_strength=0.5,
    volume=5,
    material=my_mat,
    energy_per_displacement=10,
    recombination_fraction=0.1,
)
print(f"damage-energy = {result}", end="\n\n")
