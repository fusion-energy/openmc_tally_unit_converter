
This Python package aims to help convert OpenMC tallies to user specified units.

# Installation

```bash
pip install openmc_tally_unit_converter
```

# Usage

OpenMC tally results are save into a statepoint h5 file without units.

This package ascertains the base units of common tallies by inspecting their
tally filters and scores.

The following worked example is for a heating tally. Other supported tallies
are heating-local, flux, effective dose and damage-energy (used to find DPA)
tallies are also supported.

```python
import openmc_tally_unit_converter as otuc
import openmc

# loads up tally from an openmc statepoint output file
statepoint = openmc.StatePoint(filepath="statepoint.2.h5")
my_tally = statepoint.get_tally(name="my_cell_heating_tally")

# gets the base units of the tally
tally = otuc.process_tally(tally=my_tally)
print(tally)
>>> 218559.22320927 electron_volt / source_particle
```

The package then allows users to scale the base tally units to different units. For example the package can easily convert cm to meters or electron volts to joules.

```python
converted_tally = otuc.process_tally(
    tally=my_tally,
    required_units = "joules / source_particle"
)

print(converted_tally)
>>> 3.50170481e-14 Joules / source_particle
```

Additional inputs can be applied to normalize the the tallies and convert the
units further:

- The source strength of the source in particles per second can be specified with the ```strength_strength``` argument. This allows the tally results to be converted from the units of score per simulated particle to score per unit time (e.g seconds, hours, days etc).

```python
converted_tally = otuc.process_tally(
    tally=my_tally,
    source_strength=1e20,  # input units for this argument are particles per second
    required_units = "joules / minute"
)

print(converted_tally)
>>> 2.10102288e+08 joules / source_particle
```

- The volume of the cell in cm3 can also be specified with the ```volume``` argument. This allows the tally result to be converted from the base units to base units per unit volume.

```python
converted_tally = otuc.process_tally(
    tally=my_tally,
    source_strength=13458.3,  # input units for this argument are particles per second
    volume=12,  # input units are in cm3
    required_units = "joules / second / meter **3"
)

print(converted_tally)
>>> 3.92724948e-05 Joules / meter ** 3 / second
```

:point_right: [Further examples](https://github.com/fusion-energy/openmc_tally_unit_converter/tree/main/examples)
