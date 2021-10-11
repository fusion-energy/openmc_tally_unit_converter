import unittest

import openmc_post_processor as opp
import pytest


class TestUsage(unittest.TestCase):
    def setUp(self):

        # loads in the statepoint file containing tallies
        statepoint = opp.StatePoint(filepath="statepoint.2.h5")
        self.my_tally = statepoint.get_tally(name="1_flux")
        self.statepoint = statepoint

    # todo make test for find_source_strength
    # print(opp.find_source_strength(fusion_energy_per_second_or_per_pulse=1.3e6))


if __name__ == "__main__":
    unittest.main()
