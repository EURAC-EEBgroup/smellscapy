"""Smellscapy is a Python library for analysing and representing indoor smellscape perceptual data."""

import os 
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("smellscapy")
except PackageNotFoundError:
    __version__ = None


from smellscapy import databases, plotting, data
from smellscapy import calculations, constants
from smellscapy.databases import DataExample
from smellscapy.plotting import (density,scatter,simple_density)

__all__ = [
    "COS45",
    "WEIGHT",
    "calculate_pleasantness",
    "calculate_presence",
    "load_example_data_Eurac",
    "load_example_data_Measure2_Unitn",
    "plot_density",
    "plot_scatter",
    "plot_simple_density",
]



