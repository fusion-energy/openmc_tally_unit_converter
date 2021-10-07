
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
    required_units=['centimeter / pulse', 'eV'],
    fusion_energy_per_pulse=1.3e6
)
print(f'spectra per pulse = {result}', end='\n\n')


# returns the tally with normalisation for source strength
print(f'spectra per second = {result}', end='\n\n')
result = statepoint.process_tally(
    tally=my_tally,
    required_units=['centimeter / second', 'eV'],
    fusion_power=1e9
)
print(f'spectra per pulse = {result}', end='\n\n')
