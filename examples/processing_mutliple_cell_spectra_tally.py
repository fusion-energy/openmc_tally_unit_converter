import openmc
import openmc_post_processor as opp
from spectrum_plotter import plot_spectrum  # a convenient plotting package

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

results = {}
for tally_name in ["2_neutron_spectra", "3_neutron_spectra"]:

    # gets one tally from the available tallies
    my_tally = statepoint.get_tally(name=tally_name)

    # returns the tally with normalisation per pulse
    result = opp.process_spectra_tally(
        tally=my_tally,
        required_units="centimeter / pulse",
        required_energy_units="MeV",
        source_strength=1.3e6,
    )
    results[tally_name] = result


# plots a graph of the results
plot = plot_spectrum(
    spectrum=results,
    x_label="Energy [MeV]",
    y_label="neutron flux [centimeter / second]",
    x_scale="log",
    y_scale="log",
    # trim_zeros=False,
    filename="combine_spectra_plot.html",
    plotting_package='plotly'
)
