import pytest

from smellscapy.databases.DataExample import load_example_data
from smellscapy.surveys import (
    ID_COLUMN_NAMES,
    ATTRIBUTES_COLUMN_NAMES
)



class TestDataExample:

    def test_load_example_data(self):
        df = load_example_data()

        assert df.shape == (482, 16) 
        assert all([col in df.columns for col in ID_COLUMN_NAMES])
        assert all([col in df.columns for col in ATTRIBUTES_COLUMN_NAMES])
