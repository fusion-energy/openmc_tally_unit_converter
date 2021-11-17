import unittest

import openmc_tally_unit_converter as otuc
import openmc
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_neutron_effective_dose")

        statepoint = openmc.StatePoint(filepath="statepoint.1.h5")
        self.my_tally_2 = statepoint.get_tally(name="2_neutron_effective_dose")

    # todo test that processing a flux tally results in a ValueError as it is missing the EnergyFunctionFilter

    def test_cell_tally_dose_no_std_dev(self):

        result = otuc.process_dose_tally(
            tally=self.my_tally_2,
        )

        assert len(result) == 1
        assert result[0].units == "neutron * picosievert / source_particle"

    def test_cell_tally_dose_base_units(self):
        # returns the tally with base units
        result = otuc.process_dose_tally(tally=self.my_tally, required_units=None)
        assert len(result) == 2
        assert result[0].units == "picosievert / source_particle"
        assert result[1].units == "picosievert / source_particle"

    def test_cell_tally_dose_no_processing(self):
        # returns the tally with base units
        result = otuc.process_dose_tally(
            tally=self.my_tally,
        )
        assert len(result) == 2
        assert result[0].units == "picosievert / source_particle"
        assert result[1].units == "picosievert / source_particle"

    def test_cell_tally_dose_processing_with_scaling(self):

        result = otuc.process_dose_tally(
            tally=self.my_tally, required_units="sievert / source_particle"
        )
        assert len(result) == 2
        assert result[0].units == "sievert / source_particle"
        assert result[1].units == "sievert / source_particle"

    def test_cell_tally_dose_with_pulse_processing(self):
        result = otuc.process_dose_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="sievert / pulse",
        )
        assert len(result) == 2
        assert result[0].units == "sievert / pulse"
        assert result[1].units == "sievert / pulse"

    def test_cell_tally_dose_with_second_processing(self):
        result = otuc.process_dose_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="sievert / second",
        )
        assert len(result) == 2
        assert result[0].units == "sievert / second"
        assert result[1].units == "sievert / second"

    def test_cell_tally_dose_with_pulse_processing(self):
        result = otuc.process_dose_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            volume=100,
            required_units="sievert / second / cm**3",
        )
        # when dividing by volume perhaps units should emerge as sievert/second
        assert len(result) == 2
        assert result[0].units == "sievert / second / centimeter **3"
        assert result[1].units == "sievert / second / centimeter **3"
