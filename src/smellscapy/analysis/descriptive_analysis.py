import pandas as pd

def descriptive_statistics (df : pd.DataFrame, group_by_col=None):
    """
        Generate descriptive statistics.

        Descriptive statistics include those that summarize the central
        tendency, dispersion and shape of a
        dataset's distribution, excluding ``NaN`` values.

        Analyzes the columns "pleasatness_score" and "presence_score" of the database (numerical continous variables between [-1,1])

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing "pleasantness_score" and "presence_score".
        
        **kwargs : dict, optional** 
        Additional keyword arguments to override default plotting parameters, including:
            - `group_by_col` : str or None, optional
            Name of the column in ``df`` to be used as categorical grouping
            variable. If None or not present in ``df``, a comprehensive statistical description is computed.

        Returns
        -------
        DataFrame
            Summary statistics of the DataFrame provided.


        Example
        --------

        >>> from smellscapy.databases.DataExample import load_example_data
        >>> from smellscapy.surveys import validate
        >>> df = load_example_data()
        >>> df,_ = validate(df)
        >>> s = descriptive_statistics(df)

                pleasantness_score  presence_score
        count              39.000000       39.000000
        mean                0.090199       -0.001022
        std                 0.164035        0.177936
        min                -0.353553       -0.353553
        25%                 0.000000       -0.088388
        std                 0.164035        0.177936
        min                -0.353553       -0.353553
        25%                 0.000000       -0.088388
        50%                 0.103553        0.000000
        50%                 0.103553        0.000000
        75%                 0.176777        0.133883
        max                 0.573223        0.280330
        median              0.103553        0.000000
        variance            0.026907        0.031661
        skewness            0.056743       -0.453332
        kurtosis            1.584875       -0.471179   
     
        dtype: float64

        """


    if group_by_col is not None and group_by_col in df.columns:
        df_subgroups = df.groupby(group_by_col)
        s = pd.DataFrame(columns= ["type", 'pleasantness_score', 'presence_score', "subgroup"])
        for name, subgroup in df_subgroups:
            df_temp = subgroup[['pleasantness_score', 'presence_score']]
            s1 = df_temp.describe()
            s1.loc['median'] = df_temp.median()
            s1.loc['variance'] = df_temp.var() 
            s1.loc['skewness'] = df_temp.skew()
            s1.loc['kurtosis'] = df_temp.kurtosis()
            s1["type"] = s1.index
            s1["subgroup"] = name
            print(group_by_col)
            print(name)
            s= pd.concat([s, s1], ignore_index=True)
    

    else:
        df_temp = df[['pleasantness_score', 'presence_score']]
        s = df_temp.describe()
        s.loc['median'] = df_temp.median()
        s.loc['variance'] = df_temp.var() 
        s.loc['skewness'] = df_temp.skew()
        s.loc['kurtosis'] = df_temp.kurtosis()
    
    print(s)

    s.to_csv("descriptive_statistics.csv")

    return s