import openmc_post_processor as opp
from regular_mesh_plotter import plot_mesh, plot_stl_slice, get_tally_extent
from matplotlib.colors import LogNorm

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")


# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)

# opp.plot_2d_mesh_tally(result, "unprocessed_image.png")

# scaled from picosievert to sievert
result = statepoint.process_tally(
    tally=my_tally, required_units="sievert cm **2 / simulated_particle"
)

# opp.plot_2d_mesh_tally(result, "scaled_image.png")

result = statepoint.process_tally(
    source_strength=1.3e6, tally=my_tally, required_units="sievert cm **2 / pulse"
)
# opp.plot_2d_mesh_tally(result, "scaled_per_pulse_image.png")


result = statepoint.process_tally(
    source_strength=1.3e6,
    tally=my_tally,
    required_units="picosievert / cm / pulse",
)


stl_slice = plot_stl_slice(
    stl_or_mesh='steel.stl',
    plane_origin = None,
    plane_normal = [0, 0, 1],
    rotate_plot = 0,
    filename='slice.png'
)

extent = get_tally_extent(my_tally)
print(extent)
plot_mesh(
    extent=extent,
    values= result,
    scale=None,  # LogNorm(),
    vmin=None,
    label="picosievert / cm / pulse",
    base_plt=stl_slice,
    filename= 'test.png',
#     vmin=1e6,
)


# print(result)
# print(result.shape)
