import openmc_post_processor as opp
from regular_mesh_plotter import plot_mesh, plot_stl_slice
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

mesh = my_tally.filters[2]
mesh.mesh.lower_left
mesh.mesh.upper_right

plot_mesh(
    extent=[-200,200, -200,200],
    values= result,
    scale=None,  # LogNorm(),
    vmin=None,
    label="",
    base_plt=stl_slice,
    filename= 'test.png',
)

# opp.plot_2d_mesh_tally(
#     values=result,
#     filename="scaled_per_pulse_per_volume_image.png",
#     vmin=1e6,
#     label="picosievert / cm / pulse",
#     scale= LogNorm()
# )

print(result)
print(result.shape)