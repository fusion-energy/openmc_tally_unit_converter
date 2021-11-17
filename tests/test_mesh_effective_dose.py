import unittest

import openmc_tally_unit_converter as otuc
import openmc
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):
        # loads in the statepoint file containing tallies and finds three tallies

        # single batch mesh tally
        self.my_tally_2 = statepoint.get_tally(name="2_neutron_effective_dose")
        neutron_effective_dose_on_2D_mesh_xy