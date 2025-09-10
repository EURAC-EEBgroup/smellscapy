from smellscapy.constants import COS45, WEIGHT

def calculate_pleasantness(df):
    return df.assign(pleasantness_score=(
            (df['pleasant'] - df['unpleasant']) + 
            COS45 * (df['light'] - (df['overpowering'])) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )
    


def calculate_presence(df):
    return df.assign(presence_score=(
            (df['present'] - (df['absent'])) +
            COS45 * ((df['overpowering']) - df['light']) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )

