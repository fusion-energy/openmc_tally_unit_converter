import unittest

import openmc_post_processor as opp
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = opp.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="1_neutron_effective_dose")
        self.statepoint = statepoint

    def test_cell_tally_dose_no_processing(self):
        # returns the tally with base units
        result = self.statepoint.process_tally(
            tally=self.my_tally,
        )
        assert (
            result.units
            == "centimeter ** 2 * neutron * picosievert / simulated_particle"
        )

    def test_cell_tally_dose_processing_with_scaling(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally, required_units="sievert cm **2 / simulated_particle"
        )
        assert result.units == "centimeter ** 2 * sievert / simulated_particle"

    def test_cell_tally_dose_with_pulse_processing(self):
        result = self.statepoint.process_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="sievert cm **2 / pulse",
        )
        assert result.units == "centimeter ** 2 * sievert / pulse"

    def test_cell_tally_dose_with_second_processing(self):
        result = self.statepoint.process_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="sievert cm **2 / second",
        )
        assert result.units == "centimeter ** 2 * sievert / second"

    def test_cell_tally_dose_with_pulse_processing(self):
        result = self.statepoint.process_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            volume=100,
            required_units="sievert / second / cm",
        )
        # when dividing by volume perhaps units should emerge as sievert/second
        assert result.units == "sievert / second / centimeter"
