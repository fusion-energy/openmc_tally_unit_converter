
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import trim_zeros


def plot_step_line_graph(
    x: Iterable[float],
    y: Iterable[float],
    y_err: Optional[Iterable[float]] = None,
    x_label: Optional[str] = '',
    y_label: Optional[str] = '',
    x_scale: Optional[str] = 'linear',
    y_scale: Optional[str] = 'linear',
    title: Optional[str] = '',
    filename: Optional[str] = None,
    trim_zeros: Optional[bool] = True
) -> plt:
    """Plots a stepped line graph with optional shaded region for Y error.
    Intended use for ploting neutron / photon spectra

    Arguments:
        x: the x axis values of the plotted data,
        y: the y axis values of the plotted data,
        y_err: the y axis error values of the plotted data.
        x_label: the label to use on the x axis,
        y_label: the label to use on the y axis,
        x_scale: the scale to use for the x axis. Options are 'linear', 'log'
        y_scale: the scale to use for the y axis. Options are 'linear', 'log'
        title: the plot title
        filename: the filename to save the plot as
        trim_zeros: whether any zero values at the end of the x iterable
            should be removed from the plot.

    Returns:
        the matplotlib.pyplot object produced
    """

    if trim_zeros is True:
        y = np.trim_zeros(np.array(y))
        x = np.array(x[:len(y)])
        y_err = np.array(y_err[:len(y)])
    else:
        y = np.array(y)
        x = np.array(x)
        y_err = np.array(y_err)

    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # mid and post are also options but pre is used as energy bins start from 0
    plt.step(x, y, where='pre', label='pre (default)')

    plt.yscale(y_scale)
    plt.xscale(x_scale)

    if y_err is not None:
        lower_y = y-y_err
        upper_y = y+y_err
        plt.fill_between(x, lower_y, upper_y, step='pre', color='k', alpha=0.15)

    plt.title(title)
    if filename:
        plt.savefig(filename, bbox_inches='tight')

    return plt


import json

with open('results.json') as f:
  data = json.load(f)

x=data['652_neutron_spectra']['flux per second']['energy'][:-1]
y=data['652_neutron_spectra']['flux per second']['result']
y_err=data['652_neutron_spectra']['flux per second']['std. dev.']

plot_step_line_graph(
    x_label='Energy [MeV]',
    y_label='neutron flux [particles/cm2-s]',
    # x_scale='log',
    # y_scale='log',
    x=x,
    y=y,
    y_err=y_err,
    filename='step_line_graph.png'
)

# with open('results.json') as f:
#   data = json.load(f)
