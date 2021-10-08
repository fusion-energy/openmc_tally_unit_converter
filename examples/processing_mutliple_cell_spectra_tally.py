
import openmc_post_processor as opp

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath='statepoint.2.h5')

results = {}
for tally_name in ['1_neutron_spectra', '2_neutron_spectra', '3_neutron_spectra']:

    # gets one tally from the available tallies
    my_tally = statepoint.get_tally(name=tally_name)


    # returns the tally with normalisation per pulse
    result = statepoint.process_tally(
        tally=my_tally,
        required_units=['MeV', 'centimeter / pulse'],
        fusion_energy_per_pulse=1.3e6
    )
    results[tally_name] = result


opp.plot_step_line_graph(
    x_label='Energy [MeV]',
    y_label='neutron flux [centimeter / pulse]',
    x_scale='log',
    y_scale='log',
    values=results,
    trim_zeros=False,
    filename=f'{tally_name}.png'
)
