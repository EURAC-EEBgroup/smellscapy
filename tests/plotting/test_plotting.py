import pytest

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import patch


from smellscapy.databases.DataExample import load_example_data
from smellscapy.surveys import validate
from smellscapy.calculations import calculate_pleasantness, calculate_presence

from smellscapy.plotting.density import plot_density
from smellscapy.plotting.joint import plot_joint
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_simple_density


@pytest.fixture
def processed_df():
    """Load example data dataframe and perform calculations."""

    df = load_example_data()
    df, _ = validate(df)

    df = calculate_pleasantness(df)
    df = calculate_presence(df)

    return df




class TestPlotFunctions:

    def test_plot_density(self, processed_df):
        with patch.object(plt, "show") as mock_show:
            plot_density(processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_density(processed_df, group_col = "LocationID", savefig=False)
        mock_show.assert_called_once()



    def test_plot_joint(self, processed_df):
        with patch.object(plt, "show") as mock_show:
            plot_joint(processed_df, savefig=True)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_joint(processed_df, group_col = "LocationID", savefig=True)
        mock_show.assert_called_once()

    

    def test_plot_scatter(self, processed_df):
        with patch.object(plt, "show") as mock_show:
            plot_scatter(processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_scatter(processed_df, group_col = "LocationID", savefig=False)
        mock_show.assert_called_once()

        

    def test_plot_simple_density(self, processed_df):
        with patch.object(plt, "show") as mock_show:
            plot_simple_density(processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_simple_density(processed_df, group_col = "LocationID", savefig=False)
        mock_show.assert_called_once()

        

