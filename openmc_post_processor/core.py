from pathlib import Path

import numpy as np
import openmc
import pint

from openmc_post_processor import get_tally_units, check_for_dimentionality_difference

ureg = pint.UnitRegistry()
ureg.load_definitions(str(Path(__file__).parent / "neutronics_units.txt"))


class StatePoint(openmc.StatePoint):
    def __init__(self, filepath: str):
        self.filepath = str(filepath)

        super().__init__(filepath=self.filepath)

    def process_tally(
        self,
        tally,
        required_units=None,
        base_units=None,
        source_strength=None,
        volume=None,
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
            print(f"tally {tally.name} base units {base_units}")

        # there might be more than one based unit entry if spectra has been tallied
        if len(base_units) == 1:
            if len(data_frame["mean"]) == 1:
                # just a single number in the tally result
                tally_result = data_frame["mean"].sum() * base_units[0]
            else:
                print("found mesh tally")
                # more than one number, a mesh tally
                # my_slice = tally.get_slice(scores=tally.scores)
                tally_filter = tally.find_filter(filter_type=openmc.MeshFilter)
                shape = tally_filter.mesh.dimension.tolist()
                if 1 in shape:
                    # 2d mesh
                    shape.remove(1)
                # my_slice.mean.shape = shape
                # tally_result = my_slice.mean * base_units[0]
                tally_result = np.array(data_frame["mean"]) * base_units[0]
                tally_result = tally_result.reshape(shape)

            if required_units:
                print(f"tally {tally.name} required units {ureg[required_units]}")
                # base_units, required_units, ureg
                tally_result = self.scale_tally(
                    tally_result,
                    base_units[0],
                    ureg[required_units],
                    ureg,
                    source_strength,
                    volume,
                )
                tally_result = self.convert_unit(tally_result, required_units)
        else:

            tally_result = []
            for filter in tally.filters:
                if isinstance(filter, openmc.filter.EnergyFilter):
                    energy_base = filter.values * base_units[0]
                    # skip other filters and contine ?

            # numpy array is needed as a pandas series can't have units
            tally_base = np.array(data_frame["mean"]) * base_units[1]

            if required_units:
                scaled_tally_result = self.scale_tally(
                    tally_base,
                    base_units[1],
                    ureg[required_units[1]],
                    ureg,
                    source_strength,
                    volume,
                )
                tally_results = self.convert_units(
                    [energy_base, scaled_tally_result], required_units
                )
                return tally_results
            else:
                return [energy_base, tally_base]

        return tally_result

    def convert_unit(self, value_to_convert, required_units):

        value_to_convert = value_to_convert.to(required_units)

        return value_to_convert

    def convert_units(self, value_to_convert, required_units):

        value_to_convert[1] = value_to_convert[1].to(required_units[1])
        value_to_convert[0] = value_to_convert[0].to(required_units[0])

        return value_to_convert

    def scale_tally(
        self, tally_result, base_units, required_units, ureg, source_strength, volume
    ):
        time_diff = check_for_dimentionality_difference(
            base_units, required_units, "[time]"
        )
        if time_diff != 0:
            print("time scaling needed (seconds)")
            if source_strength:
                source_strength = source_strength * ureg["1 / second"]
                if time_diff == -1:
                    tally_result = tally_result / source_strength
                if time_diff == 1:
                    tally_result = tally_result * source_strength
            else:
                raise ValueError(
                    f"source_strength is required but currently set to {source_strength}"
                )

        time_diff = check_for_dimentionality_difference(
            base_units, required_units, "[pulse]"
        )
        if time_diff != 0:
            print("time scaling needed (pulse)")
            if source_strength:
                source_strength = source_strength * ureg["1 / pulse"]
                if time_diff == -1:
                    tally_result = tally_result / source_strength
                if time_diff == 1:
                    tally_result = tally_result * source_strength
            else:
                raise ValueError(
                    f"source_strength is required but currently set to {source_strength}"
                )

        length_diff = check_for_dimentionality_difference(
            base_units, required_units, "[length]"
        )
        if length_diff != 0:
            print("length scaling needed")
            if volume:
                volume = volume * ureg["1 / centimeter ** 3"]
                if length_diff == -3:
                    tally_result = tally_result / volume
                if length_diff == 3:
                    tally_result = tally_result * volume
            else:
                raise ValueError(f"volume is required but currently set to {volume}")

        return tally_result
