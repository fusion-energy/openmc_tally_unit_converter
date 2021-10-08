
import openmc_post_processor as opp

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath='statepoint.2.h5')

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name='1_neutron_spectra')


# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)
print(f'spectra with base units = {result}', end='\n\n')


# returns the tally with normalisation per pulse
result = statepoint.process_tally(
    tally=my_tally,
    required_units=['eV', 'centimeter / pulse'],
    fusion_energy_per_pulse=1.3e6
)
print(f'spectra per pulse = {result}', end='\n\n')


# returns the tally scalled and normalisation for source strength
print(f'spectra per second = {result}', end='\n\n')
result = statepoint.process_tally(
    tally=my_tally,
    required_units=['MeV', 'centimeter / second'],
    fusion_power=1e9
)
print(f'spectra per pulse = {result}', end='\n\n')

# plots a graph of the results
opp.plot_step_line_graph(
    x_label='Energy [MeV]',
    y_label='neutron flux [centimeter / second]',
    x_scale='log',
    y_scale='log',
    x=result[0],
    y=result[1],
    # y_err=y_err,
    trim_zeros=False,
    filename='step_line_graph.png'
)
