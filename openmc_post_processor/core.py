
from pathlib import Path

import openmc
import pint
from openmc_post_processor import find_fusion_energy_per_reaction

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))


class StatePoint(openmc.StatePoint):
    def __init__(
        self,
        filepath: str
    ):
        self.filepath = str(filepath)

        super().__init__(filepath=self.filepath)

    def get_tally_units(self, tally):
        """
        """
        # todo add logic that assigns Pint units to a tally
        # this can be ascertained by the tally filters
        # perhaps as a first pass the tally.name can be used

        if 'heating' in tally.name:
            # 'electron_volt / simulated_particle'
            return ureg.electron_volt / ureg.simulated_particle

        if 'effective_dose' in tally.name:
            # pSv cm^2
            return ureg.picosievert / ureg.simulated_particle

        if 'flux' in tally.name:
            # simulated_particle/cm2-s
            return ureg.simulated_particle/ ureg.centimeter ** 2 / ureg.second

        else:
            # default tallies are per simulated_particle
            return 1 / ureg.simulated_particle

    def process_tally(
        self,
        tally,
        required_units=None,
        fusion_power=None,
        fusion_energy_per_pulse=None,
        reactants='DT'
    ):
        """Processes the tally converting the tally with default units obtained
        during simulation into the user specified units. In some cases
        additional user inputs will be required. Units with"""

        # user makes use of StatePoint.get_tally to find tally
        # passes the tally into this function along with the required units
        # the tally can be returned with base units or with converted units

        if fusion_power:
            fusion_power = fusion_power * ureg.watts
            fusion_energy_per_reaction_j = find_fusion_energy_per_reaction(reactants) * ureg.joules
            number_of_neutrons_per_second = fusion_power / fusion_energy_per_reaction_j
            print(f'number_of_neutrons_per_second {number_of_neutrons_per_second.to_base_units()}')

        if fusion_energy_per_pulse is not None:
            fusion_energy_per_pulse = fusion_energy_per_pulse * ureg.joules / ureg.pulse
            fusion_energy_per_reaction_j = find_fusion_energy_per_reaction(reactants) * ureg.joules
            number_of_neutrons_per_pulse = fusion_energy_per_pulse / fusion_energy_per_reaction_j
            print(f'number_of_neutrons_per_pulse {number_of_neutrons_per_pulse.to_base_units()}')

        data_frame = tally.get_pandas_dataframe()

        base_units = self.get_tally_units(tally)
        print(f'tally {tally.name} base units {base_units}')

        tally_result = data_frame["mean"].sum() * base_units

        if required_units:
            if any(x in required_units for x in ['per second', '/ second', '/second']):
                tally_result = tally_result * number_of_neutrons_per_second
                tally_result = tally_result.to(required_units)

            if any(x in required_units for x in ['per pulse', '/ pulse', '/pulse']):
                tally_result = tally_result * number_of_neutrons_per_pulse
                tally_result = tally_result.to(required_units)

            tally_result = tally_result.to(required_units)
        print(f'tally_result {tally_result}')
        print()
        return tally_result
