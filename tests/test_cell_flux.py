import unittest

import openmc_tally_unit_converter as otuc
import pytest
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_flux")

        statepoint = openmc.StatePoint(filepath="statepoint.1.h5")
        self.my_tally_2 = statepoint.get_tally(name="2_flux")

    def test_cell_tally_flux_with_no_std_dev(self):

        result = otuc.process_tally(
            tally=self.my_tally_2,
            required_units="centimeter / simulated_particle",
        )

        assert len(result) == 1
        assert result[0].units == "centimeter / simulated_particle"

    def test_cell_tally_flux_no_processing(self):

        result = otuc.process_tally(
            tally=self.my_tally,
            required_units="centimeter / simulated_particle",
        )

        assert len(result) == 2
        assert result[0].units == "centimeter / simulated_particle"
        assert result[1].units == "centimeter / simulated_particle"

    def test_cell_tally_flux_fusion_power_processing(self):

        # returns the tally with normalisation per pulse
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="centimeter / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "centimeter / pulse"
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_flux_pulse_processing(self):

        result = otuc.process_tally(
            source_strength=5,  # neutrons per second 1e9Gw
            tally=self.my_tally,
            required_units="centimeter / second",
        )

        assert len(result) == 2
        assert result[0].units == "centimeter / second"
        assert result[1].units == "centimeter / second"

    def test_cell_tally_flux_pulse_processing_and_scaling(self):

        result = otuc.process_tally(
            source_strength=5,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="meter / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "meter / pulse"
        assert result[1].units == "meter / pulse"

    def test_cell_tally_flux_volume_processing(self):

        result = otuc.process_tally(
            volume=100, tally=self.my_tally, required_units="1 / centimeter ** 2"
        )

        assert len(result) == 2
        assert result[0].units == "1 / centimeter ** 2"
        assert result[1].units == "1 / centimeter ** 2"
