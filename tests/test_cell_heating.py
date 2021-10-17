import unittest

import openmc_post_processor as opp
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = opp.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_heating")
        self.statepoint = statepoint

    def test_cell_tally_heating_no_processing(self):
        # returns the tally with base units
        result = self.statepoint.process_tally(
            tally=self.my_tally,
        )

        assert result.units == "electron_volt / simulated_particle"
        assert isinstance(result.magnitude, float)

    def test_cell_tally_heating_fusion_power_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = self.statepoint.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / second",
        )
        assert result.units == "electron_volt / second"
        assert isinstance(result.magnitude, float)

    def test_cell_tally_heating_pulse_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = self.statepoint.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / pulse",
        )
        assert result.units == "electron_volt / pulse"

    def test_cell_tally_heating_pulse_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = self.statepoint.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / pulse",
        )
        assert result.units == "megaelectron_volt / pulse"

    def test_cell_tally_heating_fusion_power_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = self.statepoint.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / second",
        )
        assert result.units == "megaelectron_volt / second"

    def test_cell_tally_heating_fusion_power_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = self.statepoint.process_tally(
            source_strength=1.3e6, tally=self.my_tally, required_units="joule / second"
        )
        assert result.units == "joule / second"

    def test_cell_tally_heating_pulse_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = self.statepoint.process_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="joules / pulse",  # joules or joule can be requested
        )
        assert result.units == "joule / pulse"


if __name__ == "__main__":
    unittest.main()
