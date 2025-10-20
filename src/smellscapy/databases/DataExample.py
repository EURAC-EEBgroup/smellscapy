
from importlib import resources
from loguru import logger
import pandas as pd



def load_example_data() -> pd.DataFrame: 
    """ 
    Load the data example csv file to a DataFrame.
    """
    
    data_resource = resources.files("smellscapy.data").joinpath("DataExample.csv")
    with resources.as_file(data_resource) as f:
        data = pd.read_csv(f, sep=";")
    logger.info("Loaded data example from Smellscapy's included CSV file.")
    return data