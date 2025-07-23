from smellscapy.constants import COS45, WEIGHT

def calculate_pleasantness(df):
    df['pleasantness_score'] = (
        (df['pleasant'] - df['unpleasant']) + 
        COS45 * (df['light'] - (df['overpowering'])) +
        COS45 * (df['engaging'] - (df['detached']))
    ) * WEIGHT

def calculate_presence(df):
    df['presence_score'] = (
    (df['present'] - (df['absent'])) +
    COS45 * ((df['overpowering']) - df['light']) +
    COS45 * (df['engaging'] - (df['detached']))
) * WEIGHT
