import pytest

import pandas as pd
import numpy as np

from smellscapy.calculations import calculate_pleasantness, calculate_presence


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with survey data."""
    return pd.DataFrame(
        {
            "RecordID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
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



class TestCalculatePleasantness:

    def test_calculate_pleasantness(self, sample_df):
        df = calculate_pleasantness(sample_df)
        expected_values = np.array([0.28033009, 0.4267767, 0.10355339, 0, 0.1767767, 0.0732233, -0.10355339, -0.4267767, 0, 0.01256313])

        assert 'pleasantness_score' in df.columns
        np.testing.assert_allclose(df['pleasantness_score'].values, expected_values, rtol=1e-6, atol=1e-8)



class TestCalculatePresence:

    def test_calculate_presence(self, sample_df):
        df = calculate_presence(sample_df)
        expected_values = np.array([-0.0732233, -0.0732233, -0.04289322, 0, -0.0732233, -0.1767767, 0.20710678, 0.28033009, 0.10355339, 0.13388348])

        assert 'presence_score' in df.columns
        np.testing.assert_allclose(df['presence_score'].values, expected_values, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    pytest.main()