import openmc
from spectrum_plotter import plot_spectrum_from_tally  # a convenient plotting package

# loads in the statepoint file containing tallies
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")

# constructs a dictionary of tallies
results = {}
results["2_neutron_spectra"] = statepoint.get_tally(name="2_neutron_spectra")
results["3_neutron_spectra"] = statepoint.get_tally(name="3_neutron_spectra")


# plots a graph of the results with the units as recorded in the tally
plot = plot_spectrum_from_tally(
    spectrum=results,
    x_label="Energy [eV]",
    y_label="neutron flux [centimeters / source_particle]",
    x_scale="log",
    y_scale="log",
    filename="combine_spectra_plot_1.html",
    required_energy_units="eV",
    plotting_package="plotly",
    required_units="centimeters / source_particle",
)


# plots a graph of the results with the units normalized for source strength
plot = plot_spectrum_from_tally(
    spectrum=results,
    x_label="Energy [MeV]",
    y_label="neutron flux [centimeter / second]",
    x_scale="log",
    y_scale="log",
    filename="combine_spectra_plot_2.html",
    required_energy_units="MeV",
    plotting_package="plotly",
    required_units="centimeter / second",
    source_strength=1.3e6,
)

# plots a graph of the results with the units normalized for source strength and volume
plot = plot_spectrum_from_tally(
    spectrum=results,
    x_label="Energy [MeV]",
    y_label="neutron flux [neutrons s^-1 cm^-2]",
    x_scale="log",
    y_scale="log",
    filename="combine_spectra_plot_3.html",
    required_energy_units="MeV",
    plotting_package="plotly",
    required_units="neutrons / second * cm ** -2",
    source_strength=1.3e7,
    volume=100,
)
