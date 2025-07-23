
from typing import Dict, List, Optional, Tuple
import pandas as pd
import itertools
from loguru import logger


ATTRIBUTES_VALUE_RANGE =(1, 5)
ATTRIBUTES_VALUES = [1, 2, 3, 4, 5]
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

ID_COLUMN_NAMES = [
    "RecordID", 
    "ResearcherID",
    "LocationID"
]



def validate(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """ 

    """
    logger.info("Validating data...")

    # verificare che chh,tte le colonne 
    missing_columns = []
    for col in itertools.chain(ID_COLUMN_NAMES, ATTRIBUTES_COLUMN_NAMES):
        if not col in df.columns:
            missing_columns.append(col)

    if missing_columns:
        raise Exception(f"Missing mandatory column/s: {', '.join(missing_columns)}")
    

    df_attr = df[ATTRIBUTES_COLUMN_NAMES]
    df_err = df.applymap(lambda x: x in ATTRIBUTES_VALUES if pd.notna(x) else True)
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




