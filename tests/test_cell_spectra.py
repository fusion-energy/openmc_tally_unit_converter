import unittest

import openmc_tally_unit_converter as otuc
import pytest
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_neutron_spectra")

    def test_cell_tally_spectra_no_processing(self):
        # returns the tally with base units
        result = otuc.process_spectra_tally(tally=self.my_tally, required_units=None)
        # units for energy
        assert result[0].units == "electron_volt"
        # units for flux
        assert result[1].units == "centimeter * neutron / source_particle"

    def test_cell_tally_spectra_pulse_processing(self):

        result = otuc.process_spectra_tally(
            tally=self.my_tally,
            required_units="centimeter / pulse",
            required_energy_units="eV",
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "electron_volt"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling(self):
        result = otuc.process_spectra_tally(
            tally=self.my_tally,
            required_units="centimeter / pulse",
            required_energy_units="joule",
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "joule"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling_2(self):
        result = otuc.process_spectra_tally(
            tally=self.my_tally,
            required_units="centimeter / pulse",
            required_energy_units="megajoule",
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "megajoule"
        # units for flux
        assert result[1].units == "centimeter / pulse"

    def test_cell_tally_spectra_pulse_processing_and_scaling_3(self):
        result = otuc.process_spectra_tally(
            tally=self.my_tally,
            required_units="centimeter / pulse",
            required_energy_units="MeV",
            source_strength=1.3e6,
        )
        # units for energy
        assert result[0].units == "megaelectron_volt"
        # units for flux
        assert result[1].units == "centimeter / pulse"
