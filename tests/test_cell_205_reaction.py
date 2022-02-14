import unittest

import openmc_tally_unit_converter as otuc
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_205")

        statepoint = openmc.StatePoint(filepath="statepoint.1.h5")
        self.my_tally_2 = statepoint.get_tally(name="2_205")

    def test_cell_tally_with_no_std_dev(self):

        result = otuc.process_tally(
            tally=self.my_tally_2,
            required_units="reactions / source_particle",
        )

        assert len(result) == 1
        assert result[0].units == "reactions / source_particle"

    def test_cell_tally_base_units(self):

        result = otuc.process_tally(tally=self.my_tally)

        assert len(result) == 2
        assert result[0].units == "reactions / source_particle"
        assert result[1].units == "reactions / source_particle"

    def test_cell_tally_no_processing(self):

        result = otuc.process_tally(
            tally=self.my_tally,
            required_units="reactions / source_particle",
        )

        assert len(result) == 2
        assert result[0].units == "reactions / source_particle"
        assert result[1].units == "reactions / source_particle"

    def test_cell_tally_fusion_power_processing(self):

        # returns the tally with normalisation per pulse
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="reactions / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "reactions / pulse"
        assert result[1].units == "reactions / pulse"

    def test_cell_tally_pulse_processing(self):

        result = otuc.process_tally(
            source_strength=5,  # neutrons per second 1e9Gw
            tally=self.my_tally,
            required_units="reactions / second",
        )

        assert len(result) == 2
        assert result[0].units == "reactions / second"
        assert result[1].units == "reactions / second"

    def test_cell_tally_pulse_processing_and_scaling(self):

        result = otuc.process_tally(
            source_strength=5,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="gigareactions / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "gigareactions / pulse"
        assert result[1].units == "gigareactions / pulse"

    def test_cell_tally_volume_processing(self):

        result = otuc.process_tally(
            volume=100, tally=self.my_tally, required_units="reactions / centimeter ** 3"
        )

        assert len(result) == 2
        assert result[0].units == "reactions / centimeter ** 3"
        assert result[1].units == "reactions / centimeter ** 3"
