
[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/openmc_post_processor/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/openmc_post_processor/actions/workflows/ci_with_install.yml)

[![Upload Python Package](https://github.com/fusion-energy/openmc_post_processor/actions/workflows/python-publish.yml/badge.svg)](https://github.com/fusion-energy/openmc_post_processor/actions/workflows/python-publish.yml)

This Python package aims to help convert OpenMC tallies to user specified units.

OpenMC tally results are save into at statepoint.h5 file without units.

This package ascertains the units of common tallies using the tally filters and scores attributes of the tally.

The package then allows users to scale the base tally units to different units. For example the package can easily convert cm to meters or electron volts to joules.

Additional inputs can be applied to normalize the the tallies. by the source strength of the source. For example if ```strength_strength``` is provided then tallies can converted from the base units to user friendly units. For example heating tallies are recorded in electron volts per source particle. However this can be converted to Watts.

Scaling by the volume of the cell or mesh is also possible by ```volume``` and requesting  units that require normalizing with volume. Follow on from the previous example with would allow conversion of heating tallies in their base units of electron volts per source particle to be converted to Watts per cm3.

| Tally type | Filters present | Scores present | Base units | Required units | function | Additional args |
|---|---|---|---|---|---|---|
| dpa | Cell or mesh | damage-energy | eV per simulated particle | MeV per simulated particle | process_tally |  |
|  |  |  |  | Joules per simulated particle | process_tally |  |
|  |  |  |  | Joules per second |  | source_strength |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

:point_right: [Examples](https://github.com/fusion-energy/openmc_post_processor/tree/main/examples)
