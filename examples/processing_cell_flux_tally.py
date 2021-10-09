
import openmc_post_processor as opp

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath='statepoint.2.h5')

# gets one tally from the available tallies
my_tally = statepoint.get_tally(name='1_flux')

print('default openmc tally result in base units', my_tally, end='\n\n')


# returns the tally with base units
result = statepoint.process_tally(
    tally=my_tally,
)
print(f'flux base units = {result}', end='\n\n')


# returns the tally with scalled based units (m instead of cm)
result = statepoint.process_tally(
    tally=my_tally,
    required_units='meter / simulated_particle'
)
print(f'flux scaled base units = {result}', end='\n\n')


# returns the tally with normalisation per pulse
result = statepoint.process_tally(
    fusion_energy_per_pulse=1.3e6,
    tally=my_tally,
    required_units='centimeter / pulse'
)
print(f'flux per pulse = {result}', end='\n\n')


# returns the tally with normalisation for source strength
result = statepoint.process_tally(
    fusion_power=1e9,
    tally=my_tally,
    required_units='centimeter / second'
)
print(f'flux per second = {result}', end='\n\n')
