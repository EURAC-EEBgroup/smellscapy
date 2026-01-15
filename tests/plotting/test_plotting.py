import pytest

import matplotlib.pyplot as plt
from plotly.basedatatypes import BaseFigure
import numpy as np
from unittest.mock import patch

from io import BytesIO
from PIL import Image

from smellscapy.databases.DataExample import load_example_data_Eurac, load_example_data_Measure2_Unitn
from smellscapy.surveys import validate
from smellscapy.calculations import calculate_pleasantness, calculate_presence

from smellscapy.plotting.density import plot_density
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_simple_density
from smellscapy.plotting.dynamic import plot_dynamic



@pytest.fixture
def eurac_processed_df():
    """Load Eurac example data dataframe and perform calculations."""

    df = load_example_data_Eurac()
    df, _ = validate(df)

    df = calculate_pleasantness(df)
    df = calculate_presence(df)

    return df


@pytest.fixture
def unitn_processed_df():
    """Load Unitn example data dataframe and perform calculations."""

    df = load_example_data_Measure2_Unitn()
    df, _ = validate(df)

    df = calculate_pleasantness(df)
    df = calculate_presence(df)

    return df


@pytest.fixture
def image_from_figure():
    def _convert(fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=100)
        buf.seek(0)
        return Image.open(buf)
    return _convert


@pytest.fixture
def image_from_go_figure():
    def _convert(fig):
        png_bytes = fig.to_image(format="png", scale=1)
        buf = BytesIO(png_bytes)
        return Image.open(buf)
    return _convert



class TestPlotFunctions:

    def test_plot_density(self, eurac_processed_df, unitn_processed_df, image_snapshot, image_from_figure):
        with patch.object(plt, "show") as mock_show:
            plot_density(eurac_processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_density(eurac_processed_df, group_col = "LocationID", savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show"):
            fig, ax = plot_density(eurac_processed_df, savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/density_eurac.png')

        with patch.object(plt, "show"):
            fig, ax = plot_density(eurac_processed_df, group_by_col = "Smell source", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/density_smellsource_eurac.png')

        with patch.object(plt, "show"):
            fig, ax = plot_density(unitn_processed_df, group_by_col = "Satisfaction", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/density_satisfaction_unitn.png')



    def test_plot_scatter(self, eurac_processed_df, unitn_processed_df, image_snapshot, image_from_figure):
        with patch.object(plt, "show") as mock_show:
            plot_scatter(eurac_processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_scatter(eurac_processed_df, group_by_col = "LocationID", savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show"):
            fig, ax = plot_scatter(eurac_processed_df, group_by_col = "LocationID", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/scatter_eurac.png')

        with patch.object(plt, "show"):
            fig, ax = plot_scatter(unitn_processed_df, group_by_col = "Satisfaction", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/scatter_unitn.png')

        

    def test_plot_simple_density(self, eurac_processed_df, unitn_processed_df, image_snapshot, image_from_figure):
        with patch.object(plt, "show") as mock_show:
            plot_simple_density(eurac_processed_df, savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show") as mock_show:
            plot_simple_density(eurac_processed_df, group_by_col = "LocationID", savefig=False)
        mock_show.assert_called_once()

        with patch.object(plt, "show"):
            fig, ax = plot_simple_density(eurac_processed_df, savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/simple_density_eurac.png')
        
        with patch.object(plt, "show"):
            fig, ax = plot_simple_density(eurac_processed_df, group_by_col = "Smell source", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/simple_density_smellsource_eurac.png')

        with patch.object(plt, "show"):
            fig, ax = plot_simple_density(unitn_processed_df, group_by_col = "Satisfaction", savefig=False)
        img = image_from_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/simple_density_satisfaction_unitn.png')
        


    def test_plot_dynamic(self, eurac_processed_df, image_snapshot, image_from_go_figure):
        with patch.object(BaseFigure, "show") as mock_fig_show:
            plot_dynamic(eurac_processed_df, time_col="How long have you been in your office without leaving?")
        mock_fig_show.assert_called_once()

        with patch.object(BaseFigure, "show") as mock_fig_show:
            plot_dynamic(
                eurac_processed_df, 
                time_col="How long have you been in your office without leaving?",
                group_by_col="Smell source",
            )
        mock_fig_show.assert_called_once()

        with patch.object(BaseFigure, "show") as mock_fig_show:
            fig = plot_dynamic(eurac_processed_df, time_col="How long have you been in your office without leaving?")
        img = image_from_go_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/dynamic_eurac.png')
        
        with patch.object(plt, "show"):
            fig =  plot_dynamic(
                eurac_processed_df, 
                time_col="How long have you been in your office without leaving?",
                group_by_col="Smell source",
            )
        img = image_from_go_figure(fig)
        image_snapshot(img, 'tests/__snapshots__/dynamic_smellsource_eurac.png')
