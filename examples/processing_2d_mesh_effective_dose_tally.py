import openmc_post_processor as opp
from matplotlib.colors import LogNorm

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")


# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)

opp.plot_2d_mesh_tally(result, "unprocessed_image.png")

# scaled from picosievert to sievert
result = statepoint.process_tally(
    tally=my_tally, required_units="sievert cm **2 / simulated_particle"
)

opp.plot_2d_mesh_tally(result, "scaled_image.png")

result = statepoint.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="sievert cm **2 / pulse"
)
opp.plot_2d_mesh_tally(result, "scaled_per_pulse_image.png")


result = statepoint.process_tally(
    source_strength=1.3e6,
    tally=my_tally,
    required_units="picosievert / cm / pulse",
)

opp.plot_2d_mesh_tally(
    values=result,
    filename="scaled_per_pulse_per_volume_image.png",
    vmin=1e6,
    label="picosievert / cm / pulse",
    scale= LogNorm()
)
