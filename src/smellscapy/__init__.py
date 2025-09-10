"""Smellscapy is a Python library for analysing and representing indoor smellscape perceptual data."""

import os 

from smellscapy._version import __version__  # noqa: F401

from smellscapy import databases, plotting, data
from smellscapy import calculations, constants
from smellscapy.databases import DataExample
from smellscapy.plotting import (
    density,
    scatter,
    joint,
    simple_density
)

__all__ = [
    "COS45",
    "WEIGHT",
    "calculate_pleasantness",
    "calculate_presence",
    "load_example_data",
    "plot_density",
    "plot_joint",
    "plot_scatter",
    "plot_simple_density",
]



