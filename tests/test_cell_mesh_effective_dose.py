import unittest

import openmc
import openmc_tally_unit_converter as otuc


class TestUsage(unittest.TestCase):
    def setUp(self):
        # loads in the statepoint file containing tallies and finds three tallies

        # two batch cell tally
        statepoint_2 = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint_2.get_tally(name="2_neutron_effective_dose")

        # two batch mesh tally
        self.my_tally_2 = statepoint_2.get_tally(name="neutron_effective_dose_on_2D_mesh_xy")

    def test_cell_tally_dose_processing_volume(self):

        result = otuc.process_dose_tally(
            tally=self.my_tally_2,
            required_units="sievert / source_particle",
            volume=100
        )
        assert len(result) == 2
        assert result[0].units == "sievert / source_particle"
        assert result[1].units == "sievert / source_particle"
