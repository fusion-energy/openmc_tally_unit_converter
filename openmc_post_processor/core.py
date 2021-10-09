
from pathlib import Path

import numpy as np
import openmc
import pint

from openmc_post_processor import find_fusion_energy_per_reaction, get_tally_units

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))


class StatePoint(openmc.StatePoint):
    def __init__(
        self,
        filepath: str
    ):
        self.filepath = str(filepath)

        super().__init__(filepath=self.filepath)


    def process_tally(
        self,
        tally,
        required_units=None,
        base_units=None,
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
            fusion_energy_per_reaction_j = find_fusion_energy_per_reaction(reactants) * ureg.joules / ureg.neutrons
            self.number_of_neutrons_per_second = fusion_power / fusion_energy_per_reaction_j
            print(f'number_of_neutrons_per_second {self.number_of_neutrons_per_second.to_base_units()}')

        if fusion_energy_per_pulse is not None:
            fusion_energy_per_pulse = fusion_energy_per_pulse * ureg.joules / ureg.pulse
            fusion_energy_per_reaction_j = find_fusion_energy_per_reaction(reactants) * ureg.joules / ureg.neutrons
            self.number_of_neutrons_per_pulse = fusion_energy_per_pulse / fusion_energy_per_reaction_j
            print(f'number_of_neutrons_per_pulse {self.number_of_neutrons_per_pulse.to_base_units()}')

        data_frame = tally.get_pandas_dataframe()

        # checks for user provided base units
        if not base_units:
            base_units = get_tally_units(tally, ureg)
            print(f'tally {tally.name} base units {base_units}')

        # there might be more than one based unit entry if spectra has been tallied
        if len(base_units) == 1:
            tally_result = data_frame["mean"].sum() * base_units[0]
            if required_units:
                print(f'tally {tally.name} required units {ureg[required_units]}')

                unit_diff = base_units[0] * ureg[required_units]

                # these are not ideal methods of checking
                if '/ [time]' in str(unit_diff.dimensionality):
                    print('* time needed')
                    # base_units[0] = base_units[0] * self.number_of_neutrons_per_pulse
                if base_units[0].dimensionality == '[length]' and ureg[required_units].dimensionality == '1 / [length] ** 2':
                    print('/ volume needed')
                
                tally_result = self.convert_unit(tally_result, required_units)
        else:  

            tally_result = []
            for filter in tally.filters:
                if isinstance(filter, openmc.filter.EnergyFilter):
                    tally_result.append(filter.values * base_units[0])
                    # skip other filters and contine ?
            # numpy array is needed as a pandas series can't have units
            tally_result.append(np.array(data_frame["mean"]) * base_units[1])

            if required_units:
                tally_result = self.convert_units(tally_result, required_units)

        return tally_result

    def convert_unit(self, value_to_convert, required_units):

        if any(x in required_units for x in ['per second', '/ second', '/second']):
            value_to_convert = value_to_convert * self.number_of_neutrons_per_second
            value_to_convert = value_to_convert.to(required_units)

        if any(x in required_units for x in ['per pulse', '/ pulse', '/pulse']):
            value_to_convert = value_to_convert * self.number_of_neutrons_per_pulse
            value_to_convert = value_to_convert.to(required_units)

        value_to_convert = value_to_convert.to(required_units)

        return value_to_convert

    def convert_units(self, value_to_convert, required_units):

        if any(x in required_units[1] for x in ['per second', '/ second', '/second']):
            value_to_convert[1] = value_to_convert[1] * self.number_of_neutrons_per_second
            # value_to_convert[1] = value_to_convert[1].to(required_units[1])

        if any(x in required_units[1] for x in ['per pulse', '/ pulse', '/pulse']):
            value_to_convert[1] = value_to_convert[1] * self.number_of_neutrons_per_pulse
            # value_to_convert[1] = value_to_convert[1].to(required_units[1])

        value_to_convert[1] = value_to_convert[1].to(required_units[1])
        value_to_convert[0] = value_to_convert[0].to(required_units[0])

        return value_to_convert
