import pandas as pd
from smellscapy.constants import COS45, WEIGHT



def calculate_pleasantness(df: pd.DataFrame):
    """
    Calculate pleasantness for each row in a survey dataset. 

    This function process the provided survey DataFrame and appends 
    a new column called `'pleasantness_score'` based on pleasant, unpleasant and other parameters.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing survey data. Must include columns
        required for computing the score.

    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with an additional column `'pleasantness_score'`.

    Examples
    --------
        >>> import pandas as pd
        >>> from smellscapy.surveys import validate
        >>> from smellscapy.databases.DataExample import load_example_data
        >>> from smellscapy.calculations import calculate_pleasantness
        >>> df = load_example_data()
        >>> df, excl_df = validate(df)
        >>> df = calculate_pleasantness(df)
    """

    return df.assign(pleasantness_score=(
            (df['pleasant'] - df['unpleasant']) + 
            COS45 * (df['light'] - (df['overpowering'])) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )
    


def calculate_presence(df: pd.DataFrame):
    """
    Calculate presence for each row in a survey dataset. 

    This function process the provided survey DataFrame and appends 
    a new column called `'presence_score'` based on present, absent and other parameters.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing survey data. Must include columns
        required for computing the score.

    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with an additional column `'presence_score'`.

    Examples
    --------
        >>> import pandas as pd
        >>> from smellscapy.surveys import validate
        >>> from smellscapy.databases.DataExample import load_example_data
        >>> from smellscapy.calculations import calculate_presence
        >>> df = load_example_data()
        >>> df, excl_df = validate(df)
        >>> df = calculate_presence(df)
    
    """

    return df.assign(presence_score=(
            (df['present'] - (df['absent'])) +
            COS45 * ((df['overpowering']) - df['light']) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )

