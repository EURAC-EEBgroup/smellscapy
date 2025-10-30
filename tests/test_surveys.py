import pytest

import re
import pandas as pd
import numpy as np

from smellscapy.surveys import (
    ATTRIBUTES_VALUES, 
    ATTRIBUTES_COLUMN_NAMES, 
    validate
)


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with survey data."""
    return pd.DataFrame(
        {
            "RecordID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "ResearcherID": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "LocationID": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "pleasant": [4, 4, 3, 3, 3, 3, 2, 2, 3, 2],
            "present": [3, 3, 3, 3, 3, 3, 4, 4, 3, 4],	
            "light": [3, 4, 3, 3, 3, 3, 4, 2, 2, 4],	
            "engaging": [2, 3, 2, 3, 2, 3, 3, 3, 3, 4],	
            "unpleasant": [2, 2, 2, 3, 2, 3, 3, 4, 3, 4],	
            "absent": [3, 3, 2, 3, 3, 4, 2, 2, 2, 2],	
            "overpowering": [2, 2, 2, 3, 2, 2, 4, 4, 2, 2],	
            "detached": [2, 2, 3, 3, 2, 3, 3, 4, 3, 3],
        }
    )



class TestSurveyAttributes:

    def test_attributes_values(self):
        assert len(ATTRIBUTES_VALUES) == 5
        assert ATTRIBUTES_VALUES == [1, 2, 3, 4, 5]

    def test_attributes_column_names(self):
        assert len(ATTRIBUTES_COLUMN_NAMES) == 8
        assert ATTRIBUTES_COLUMN_NAMES == [
            "pleasant", 
            "present",
            "light",
            "engaging",
            "unpleasant",
            "absent",
            "overpowering",
            "detached"
        ]



class TestDataFrameValidation:

    def test_validate(self, sample_df):
        df, _ = validate(sample_df)

        assert df.shape == (10, 11)  # Adjust these numbers if they change


    def test_missing_mandatory_columns(self, sample_df):
        df = sample_df.drop(columns=ATTRIBUTES_COLUMN_NAMES)
        with pytest.raises(
            Exception, match="Missing mandatory column/s: pleasant, present, light, engaging, unpleasant, absent, overpowering, detached"
        ):
            _, _ = validate(df)

        df = sample_df.drop(columns=['present', 'engaging'])
        with pytest.raises(
            Exception, match="Missing mandatory column/s: present, engaging"
        ):
            _, _ = validate(df)


    def test_values_outside_range(self, sample_df):
        df = sample_df.copy()
        df.loc[2, 'pleasant'] = 999
        df.loc[5, 'absent'] = -3

        with pytest.raises(
            Exception, match=re.escape("Attribute values are not valid. Please use numbers in range [1, 2, 3, 4, 5]")
        ):
            _, _ = validate(df)


    def test_missing_data(self, sample_df):
        df = sample_df.copy()
        df.loc[2, 'pleasant'] = None
        df.loc[5, 'absent'] = None

        df, excl_df = validate(df)
        assert df.shape[0] == 8
        assert excl_df.shape[0] == 2 # 2 rows removed



if __name__ == "__main__":
    pytest.main()