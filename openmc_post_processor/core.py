
from pathlib import Path

import numpy as np
import openmc
import pint

from openmc_post_processor import find_fusion_energy_per_reaction, get_tally_units, check_for_dimentionality_difference

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
        source_strength=None,
        cell_volume=None,
    ):
        """Processes the tally converting the tally with default units obtained
        during simulation into the user specified units. In some cases
        additional user inputs will be required. Units with"""

        # user makes use of StatePoint.get_tally to find tally
        # passes the tally into this function along with the required units
        # the tally can be returned with base units or with converted units


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

                time_diff = check_for_dimentionality_difference(base_units[0], ureg[required_units], '[time]')
                if  time_diff != 0:
                    print('time scaling needed (seconds)')
                    source_strength = source_strength * ureg['1 / second']
                    if time_diff == -1:
                        tally_result = tally_result / source_strength
                    if time_diff == 1:
                        tally_result = tally_result * source_strength

                time_diff = check_for_dimentionality_difference(base_units[0], ureg[required_units], '[pulse]')
                if  time_diff != 0:
                    print('time scaling needed (pulse)')
                    source_strength = source_strength * ureg['1 / pulse']
                    if time_diff == -1:
                        tally_result = tally_result / source_strength
                    if time_diff == 1:
                        tally_result = tally_result * source_strength

                length_diff = check_for_dimentionality_difference(base_units[0], ureg[required_units], '[length]')
                if length_diff != 0:
                    print('length scaling needed')
                    if time_diff == -3:
                        tally_result = tally_result / cell_volume
                    if time_diff == 3:
                        tally_result = tally_result * cell_volume

                
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

        # if any(x in required_units for x in ['per pulse', '/ pulse', '/pulse']):
        #     value_to_convert = value_to_convert * self.number_of_neutrons_per_pulse
        #     value_to_convert = value_to_convert.to(required_units)

        value_to_convert = value_to_convert.to(required_units)

        return value_to_convert

    def convert_units(self, value_to_convert, required_units):

        # if any(x in required_units[1] for x in ['per second', '/ second', '/second']):
        #     value_to_convert[1] = value_to_convert[1] * self.number_of_neutrons_per_second
        #     # value_to_convert[1] = value_to_convert[1].to(required_units[1])

        # if any(x in required_units[1] for x in ['per pulse', '/ pulse', '/pulse']):
        #     value_to_convert[1] = value_to_convert[1] * self.number_of_neutrons_per_pulse
        #     # value_to_convert[1] = value_to_convert[1].to(required_units[1])

        value_to_convert[1] = value_to_convert[1].to(required_units[1])
        value_to_convert[0] = value_to_convert[0].to(required_units[0])

        return value_to_convert
