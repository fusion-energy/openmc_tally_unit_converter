
import unittest

import openmc_post_processor as opp
import pytest


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
        # assert tally result is the same as the processed result


    def test_cell_tally_flux_scaling(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units='meter / simulated_particle',
        )

        assert result.units == 'meter / simulated_particle'
        # assert tally result is the same as the processed result / 100


    def test_cell_tally_flux_fusion_power_processing(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally,
            fusion_power=1e9,
            required_units='centimeter / second',
        )

        assert result.units == 'centimeter / second'
        # assert tally result is equal to the processed result scalled by number of neutrons per second

    def test_cell_tally_flux_fusion_power_scaling_processing(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally,
            fusion_power=1e9,
            required_units='meter / second',  # note meter instead of cm
        )

        assert result.units == 'meter / second'
        # assert tally result is equal to the processed result scalled by number of neutrons per second


if __name__ == "__main__":
    unittest.main()
