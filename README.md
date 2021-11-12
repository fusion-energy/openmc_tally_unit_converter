
This Python package aims to help convert OpenMC tallies to user specified units.

# Installation

```bash
pip install openmc_tally_unit_converter
```

# Usage

OpenMC tally results are save into a statepoint h5 file without units.

This package ascertains the base units of common tallies by inspecting their tally filters and scores.

```python
import openmc_tally_unit_converter as otuc
import openmc

# loads up tally from an openmc statepoint output file
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="my_cell_heating_tally")

# gets the base units of the tally
base_units = otuc.get_tally_units(my_tally)
print(base_units)
>>> eV per source_particle
```

The package then allows users to scale the base tally units to different units. For example the package can easily convert cm to meters or electron volts to joules.

```python
converted_tally = otuc.process_tally(
    tally=my_tally,
    required_units = Joules / source_particle
)

print(converted_tally)
>>> 2.4e-12 Joules per source_particle
```

Additional inputs can be applied to normalize the the tallies and convert the units further:

- The source strength of the source in particles per second can be specified with the ```strength_strength``` argument. This allows the tally results to be converted from the units of score per simulated particle to score per second.

- The volume of the cell in cm3 can also be specified with the ```volume``` argument. This allows the tally result to be converted from the base units to base units per unit volume.

:point_right: [Further examples](https://github.com/fusion-energy/openmc_tally_unit_converter/tree/main/examples)
