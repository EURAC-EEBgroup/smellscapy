import os
import pytest

import smellscapy



def test_core_smellscapy_modules():
    assert hasattr(smellscapy, "data"), "Missing data module in Smellscapy"
    assert hasattr(smellscapy, "databases"), "Missing databases module in Smellscapy" 
    assert hasattr(smellscapy, "plotting"), "Missing plotting module in Smellscapy"
