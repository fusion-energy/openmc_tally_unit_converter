
This Python package aims to help convert OpenMC tallies to user specified units.

OpenMC tallies are recorded save saved without units.

This package ascertains the units of common tallies using the tally filters and scores.

The Pint Python package to scale the base tally units to different units. For example Pint can easily convert cm to meters or electron volts to joules.

Additional inputs can be applied to normalise the the tallies by the source strength of the source. For example if ```neutrons_per_second``` is provided then tallies can be scaled and the base units of tallies can be converted to more user friendly units. For example heating tallies are recorded in electron volts per source particle. However this can be converted to Watt.
