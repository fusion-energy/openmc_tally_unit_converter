import unittest

import openmc_tally_unit_converter as otuc
import pytest
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_damage-energy")

    def test_cell_tally_base_units(self):
        # returns the tally with base units
        result = otuc.process_tally(tally=self.my_tally)

        assert len(result) == 2
        assert result[0].units == "electron_volt / source_particle"
        assert result[1].units == "electron_volt / source_particle"
        assert isinstance(result[0][0].magnitude, float)
        assert isinstance(result[1][0].magnitude, float)

    def test_energy_no_processing(self):
        # returns the tally with base units
        result = otuc.process_damage_energy_tally(
            tally=self.my_tally, required_units="eV / source_particle"
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / source_particle"
        assert result[1].units == "electron_volt / source_particle"
        assert isinstance(result[0][0].magnitude, float)
        assert isinstance(result[1][0].magnitude, float)

    def test_energy_fusion_power_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_damage_energy_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / second",
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / second"
        assert result[1].units == "electron_volt / second"
        assert isinstance(result[0][0].magnitude, float)
        assert isinstance(result[1][0].magnitude, float)

    def test_energy_pulse_processing(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_damage_energy_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="eV / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "electron_volt / pulse"
        assert result[1].units == "electron_volt / pulse"

    def test_energy_pulse_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_damage_energy_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / pulse",
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / pulse"
        assert result[1].units == "megaelectron_volt / pulse"

    def test_energy_fusion_power_processing_and_scaling(self):

        # returns the tally with scalled based units (MeV instead of eV)
        result = otuc.process_damage_energy_tally(
            source_strength=4.6e17,  # neutrons per 1.3MJ pulse
            tally=self.my_tally,
            required_units="MeV / second",
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / second"
        assert result[1].units == "megaelectron_volt / second"

    def test_energy_fusion_power_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = otuc.process_damage_energy_tally(
            source_strength=1.3e6, tally=self.my_tally, required_units="joule / second"
        )

        assert len(result) == 2
        assert result[0].units == "joule / second"
        assert result[1].units == "joule / second"

    def test_energy_pulse_processing_and_conversion(self):

        # returns the tally with normalisation per pulse and conversion to joules
        result = otuc.process_damage_energy_tally(
            source_strength=1.3e6,
            tally=self.my_tally,
            required_units="joules / pulse",  # joules or joule can be requested
        )

        assert len(result) == 2
        assert result[0].units == "joule / pulse"
        assert result[1].units == "joule / pulse"

    def test_energy_per_atom(self):
        """makes use of material,"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="MeV / source_particle / atom",
            volume=5,
            material=my_mat,
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / atom / source_particle"
        assert result[1].units == "megaelectron_volt / atom / source_particle"

    def test_energy_per_second_per_atom(self):
        """makes use of material and volume to convert to per atom units"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="MeV / atom / second",
            source_strength=1,
            volume=5,
            material=my_mat,
        )

        assert len(result) == 2
        assert result[0].units == "megaelectron_volt / atom / second"
        assert result[1].units == "megaelectron_volt / atom / second"

    def test_displacements_per_source_particle(self):
        """makes use of energy_per_displacement to convert to displacements units"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / source_particle",
            energy_per_displacement=80,
        )

        assert len(result) == 2
        assert result[0].units == "displacements / source_particle"
        assert result[1].units == "displacements / source_particle"

    def test_displacements_per_second(self):
        """makes use of energy_per_displacement to get displacements per second"""

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / second",
            energy_per_displacement=80,
            source_strength=100,
        )

        assert len(result) == 2
        assert result[0].units == "displacements / second"
        assert result[1].units == "displacements / second"

    def test_displacements_per_atom(self):
        """makes use of material and volume to find damage energy per atom"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / atom",
            energy_per_displacement=80,
            volume=5,
            material=my_mat,
        )

        assert len(result) == 2
        assert result[0].units == "displacements / atom"
        assert result[1].units == "displacements / atom"

    def test_displacements_per_atom_per_second(self):
        """makes use of material and volume to find damage energy per atom per second"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / atom / second",
            energy_per_displacement=80,
            source_strength=100,
            volume=5,
            material=my_mat,
        )

        assert len(result) == 2
        assert result[0].units == "displacements / atom / second"
        assert result[1].units == "displacements / atom / second"

    def test_displacements_per_atom_per_second_vs_per_year(self):
        """makes use of material and volume to find damage energy per atom and
        makes comparision between a year and second dpa"""

        my_mat = openmc.Material()
        my_mat.add_element("Fe", 1)
        my_mat.set_density("g/cm3", 1)

        result_second = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / atom / second",
            energy_per_displacement=80,
            source_strength=100,
            volume=5,
            material=my_mat,
        )

        assert len(result_second) == 2
        assert result_second[0].units == "displacements / atom / second"
        assert result_second[1].units == "displacements / atom / second"

        result_year = otuc.process_damage_energy_tally(
            tally=self.my_tally,
            required_units="displacements / atom / year",
            energy_per_displacement=80,
            source_strength=100,
            volume=5,
            material=my_mat,
        )

        assert len(result_year) == 2
        assert result_year[0].units == "displacements / atom / year"
        assert result_year[1].units == "displacements / atom / year"

        assert (
            result_year[0].magnitude.sum()
            == 365.25 * 24 * 60 * 60 * result_second[0].magnitude.sum()
        )
        assert (
            result_year[1].magnitude.sum()
            == 365.25 * 24 * 60 * 60 * result_second[1].magnitude.sum()
        )


if __name__ == "__main__":
    unittest.main()
