import unittest

import openmc_tally_unit_converter as otuc
import pytest
import openmc


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="2_flux")

    # todo make test for find_source_strength
    # print(otuc.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6))


if __name__ == "__main__":
    unittest.main()
