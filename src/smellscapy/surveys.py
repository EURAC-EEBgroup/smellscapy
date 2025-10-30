
from typing import Dict, List, Optional, Tuple
import pandas as pd
import itertools
from loguru import logger



ATTRIBUTES_VALUES = [1, 2, 3, 4, 5]
"""
Allowed inclusive range for attribute values.
Values can range from 1 (minimum) to 5 (maximum).
"""


ATTRIBUTES_COLUMN_NAMES = [
    "pleasant", 
    "present",
    "light",
    "engaging",
    "unpleasant",
    "absent",
    "overpowering",
    "detached"
]
"""
List of allowed column names for survey data.
The survey DataFrame must include these columns.
"""



def validate(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """ 
    Validate a survey DataFrame for required columns and acceptable value ranges.

    This function ensures that the provided DataFrame contains all necessary
    survey and ID columns, and that all numeric responses fall within the
    defined set `ATTRIBUTES_VALUES`.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing survey data. Must include columns listed in
        `ATTRIBUTES_COLUMN_NAMES`.

    Returns
    -------
    df : pandas.DataFrame
        A DataFrame containing only valid rows with complete data.
    excl_df : pandas.DataFrame
        A DataFrame containing rows removed due to missing values.

    Raises
    ------
    Exception "Missing mandatory column/s"
        If any required columns are missing
        
    Exception "Attribute values are not valid" 
        If any numeric responses fall outside the allowed range.


    Examples
    --------

    >>> import pandas as pd
    >>> from smellscapy.databases.DataExample import load_example_data
    >>> from smellscapy.surveys import validate
    >>> df = load_example_data()
    >>> df, excl_df = validate(df) # passes without error

    """
    logger.info("Validating data...")

    df = df.copy()
    # verificare che chh,tte le colonne 
    missing_columns = []
    for col in ATTRIBUTES_COLUMN_NAMES:
        if not col in df.columns:
            missing_columns.append(col)

    if missing_columns:
        raise Exception(f"Missing mandatory column/s: {', '.join(missing_columns)}")
    

    df_attr = df[ATTRIBUTES_COLUMN_NAMES]
    df_err = df_attr.applymap(lambda x: x in ATTRIBUTES_VALUES if pd.notna(x) else True)
    if any(df_err.eq(False).any()):
        raise Exception("Attribute values are not valid. Please use numbers in range [1, 2, 3, 4, 5]")

    # verificare attributes
    invalid_indices = []
    for i, row in df_attr.iterrows():
        if  row.isna().any():
            invalid_indices.append(i)
    
    if invalid_indices:
        excl_df = df.iloc[invalid_indices]
        df = df.drop(df.index[invalid_indices])
        logger.info(f"Found {len(invalid_indices)} samples with missing data")
        logger.info(f"Removed {len(invalid_indices)} rows with invalid data")
    else:
        excl_df = None
        logger.info("All data passed quality checks")

    return df, excl_df




