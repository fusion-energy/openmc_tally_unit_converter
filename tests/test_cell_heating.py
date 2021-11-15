import unittest

import openmc_tally_unit_converter as otuc
import pytest
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_heating")

    def test_cell_tally_heating_no_processing(self):
        # returns the tally with base units
        result = otuc.process_tally(
            tally=self.my_tally, required_units="eV / simulated_particle"
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / simulated_particle"
        assert result[1].units == "electron_volt / simulated_particle"
        assert isinstance(result[0][0].magnitude, float)
        assert isinstance(result[1][0].magnitude, float)

    def test_cell_tally_heating_fusion_power_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / second",
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / second"
        assert result[1].units == "electron_volt / second"
        assert isinstance(result[0][0].magnitude, float)
        assert isinstance(result[1][0].magnitude, float)

    def test_cell_tally_heating_pulse_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / pulse"
        assert result[1].units == "electron_volt / pulse"

    def test_cell_tally_heating_pulse_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / pulse"
        assert result[1].units == "megaelectron_volt / pulse"

    def test_cell_tally_heating_fusion_power_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / second",
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / second"
        assert result[1].units == "megaelectron_volt / second"

    def test_cell_tally_heating_fusion_power_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = otuc.process_tally(
            source_strength=1.3e6, tally=self.my_tally, required_units="joule / second"
        )

        assert len(result) == 2
        assert result[0].units == "joule / second"
        assert result[1].units == "joule / second"

    def test_cell_tally_heating_pulse_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = otuc.process_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="joules / pulse",  # joules or joule can be requested
        )

        assert len(result) == 2
        assert result[0].units == "joule / pulse"
        assert result[1].units == "joule / pulse"


if __name__ == "__main__":
    unittest.main()
