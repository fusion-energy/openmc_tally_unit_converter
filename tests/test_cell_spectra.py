import unittest

import openmc_post_processor as opp
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = opp.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="1_neutron_spectra")
        self.statepoint = statepoint

    def test_cell_tally_spectra_no_processing(self):
        # returns the tally with base units
        result = self.statepoint.process_tally(
            tally=self.my_tally,
        )
        # units for energy
        assert result[0].units == "electron_volt"
        # units for flux
        assert result[1].units == "centimeter * neutron / simulated_particle"

    def test_cell_tally_spectra_pulse_processing(self):

        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units=["eV", "centimeter / pulse"],
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "electron_volt"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling(self):
        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units=["joule", "centimeter / pulse"],
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "joule"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling_2(self):
        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units=["megajoule", "centimeter / pulse"],
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "megajoule"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling_3(self):
        result = self.statepoint.process_tally(
            tally=self.my_tally,
            required_units=["MeV", "centimeter / pulse"],
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "megaelectron_volt"
        # units for flux
        assert result[1].units == "centimeter / pulse"
