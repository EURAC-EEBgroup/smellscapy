from smellscapy.constants import COS45, WEIGHT

def calculate_pleasantness(df):
    df['pleasantness_score'] = (
        (df['Pleasant'] - df['Unpleasant']) + 
        COS45 * (df['Light'] - (df['Overpowering'])) +
        COS45 * (df['Engaging'] - (df['Detached']))
    ) * WEIGHT

def calculate_presence(df):
    df['presence_score'] = (
    (df['Present'] - (df['Absent'])) +
    COS45 * ((df['Overpowering']) - df['Light']) +
    COS45 * (df['Engaging'] - (df['Detached']))
) * WEIGHT
