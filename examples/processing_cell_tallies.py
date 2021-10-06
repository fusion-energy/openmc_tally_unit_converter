import openmc_post_processor as opp

statepoint = opp.StatePoint(filepath='statepoint.10.h5')

print(statepoint.tallies)

statepoint.process_tally(
    tally=statepoint.tallies[1],
)

statepoint.process_tally(
    fusion_energy_per_pulse=1.3e6,
    tally=statepoint.tallies[2],
    required_units='Melectron_volt / pulse'
)

statepoint.process_tally(
    fusion_energy_per_pulse=1.3e6,
    tally=statepoint.tallies[3],
    # required_units=''
)

statepoint.process_tally(
    fusion_power=1e9,
    tally=statepoint.tallies[4],
    # required_units='joules / second'
)