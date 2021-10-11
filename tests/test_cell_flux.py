
import unittest

import openmc_post_processor as opp
import pytest
import openmc_post_processor as opp


class TestUsage(unittest.TestCase):

    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = opp.StatePoint(filepath='statepoint.2.h5')
        self.my_tally = statepoint.get_tally(name='1_flux')
        self.statepoint = statepoint


    def test_cell_tally_flux_no_processing(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units='centimeter / simulated_particle',
        )

        assert result.units == 'centimeter / simulated_particle'

    def test_cell_tally_flux_fusion_power_processing(self):

        # returns the tally with normalisation per pulse
        result = self.statepoint.process_tally(
            source_strength=4.6e17, # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units='centimeter / pulse'
        )
        assert result.units == 'centimeter / pulse'

    def test_cell_tally_flux_pulse_processing(self):

        result = self.statepoint.process_tally(
            source_strength=5, # neutrons per second 1e9Gw
            tally=self.my_tally,
            required_units='centimeter / second'
        )
        assert result.units == 'centimeter / second'

    def test_cell_tally_flux_pulse_processing_and_scaling(self):

        result = self.statepoint.process_tally(
            source_strength=5, # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units='meter / pulse'
        )
        assert result.units == 'meter / pulse'

    def test_cell_tally_flux_pulse_processing_and_scaling(self):

        result = self.statepoint.process_tally(
            volume=100,
            tally=self.my_tally,
            required_units='1 / centimeter ** 2'
        )
        assert result.units == '1 / centimeter ** 2'
        
