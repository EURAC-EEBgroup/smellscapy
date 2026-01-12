
from importlib import resources
from loguru import logger
import pandas as pd





def load_example_data_Eurac() -> pd.DataFrame: 
    """ 
    Load the data example csv file to a DataFrame.
    """
    
    data_resource = resources.files("smellscapy.data").joinpath("DataExample_Eurac.csv")
    with resources.as_file(data_resource) as f:
        data = pd.read_csv(f, sep=";")
    logger.info("Loaded data example from Smellscapy's included CSV file.")
    return data

def load_example_data_Measure2_Unitn() -> pd.DataFrame: 
    """ 
    Load the data example csv file to a DataFrame.
    """
    
    data_resource = resources.files("smellscapy.data").joinpath("DataExample_Measure2_Unitn.csv")
    with resources.as_file(data_resource) as f:
        data = pd.read_csv(f, sep=";")
    logger.info("Loaded data example from Smellscapy's included CSV file.")
    return data