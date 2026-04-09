"""Smellscapy is a Python library for analysing and representing indoor smellscape perceptual data."""

import os 
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("smellscapy")
except PackageNotFoundError:
    __version__ = None


from smellscapy import databases, plotting, data
from smellscapy import calculations, constants
from smellscapy.databases.DataExample import (load_example_data_Eurac, load_example_data_Measure2_Unitn)
from smellscapy.plotting.simple_density import (plot_simple_density) 
from smellscapy.plotting.scatter import (plot_scatter)
from smellscapy.plotting.dynamic import (plot_dynamic)
from smellscapy.surveys import validate
from smellscapy.calculations import (calculate_pleasantness, calculate_presence)
from smellscapy.analysis.descriptive_analysis import (descriptive_statistics)

__all__ = [
    "COS45",
    "WEIGHT",
    "validate",
    "calculate_pleasantness",
    "calculate_presence",
    "load_example_data_Eurac",
    "load_example_data_Measure2_Unitn",
    "plot_density",
    "plot_scatter",
    "plot_simple_density",
    "plot_dynamic",
    "descriptive_statistics"
]



