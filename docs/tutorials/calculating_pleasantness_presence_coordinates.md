SmellscaPy provides two functions for calculating **pleasantness** and **presence** coordinates from the PAQ ratings. 

```python
# Calculate pleasantness
df = calculate_pleasantness(df)

# Calculate presence
df = calculate_presence(df)
```
## **Calculate pleasantness**

The `calculate_pleasantness()` adds a new column to the Dataframe called **pleasantness_score** based on participants’ perceptual ratings.

The score is calculated combining multiple perceptual dimensions into a single numerical value, according to the equation provided by Torriani et al [[1]](#ref1).

```python
#Calculate constants
COS45 = np.cos(np.radians(45))
WEIGHT = 1 / (4 + np.sqrt(32))

#Calculate pleasantness score
def calculate_pleasantness(df):
    return df.assign(pleasantness_score=(
            (df['pleasant'] - df['unpleasant']) + 
            COS45 * (df['light'] - (df['overpowering'])) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )
```

## **Calculate presence**
The `calculate_presence()` adds a new column to the Dataframe called **presence_score** based on participants’ perceptual ratings.

The score is calculated combining multiple perceptual dimensions into a single numerical value, according to the equation provided by Torriani et al [[1]](#ref1).

```python
#Calculate constants
COS45 = np.cos(np.radians(45))
WEIGHT = 1 / (4 + np.sqrt(32))

#Calculate pleasantness score
def calculate_presence(df):
    return df.assign(presence_score=(
            (df['present'] - (df['absent'])) +
            COS45 * ((df['overpowering']) - df['light']) +
            COS45 * (df['engaging'] - (df['detached']))
        ) * WEIGHT
    )
```


|    | ResearcherID | RecordID | LocationID | …   | pleasantness_score | presence_score |
|----|--------------|----------|------------|-----|--------------------|----------------|
| 0  | 1.0          | P_12     | Bolzano    | …   | -0.146447          | -0.250000      |
| 1  | 1.0          | P_15     | Bolzano    | …   | 0.000000           | 0.000000       |
| 2  | 1.0          | P_11     | Bolzano    | …   | 0.780330           | 0.073223       |
| 3  | 1.0          | P_16     | Bolzano    | …   | 0.250000           | -0.500000      |
| 4  | 1.0          | P_11     | Bolzano    | …   | 0.780330           | 0.073223       |
| .. | ...          | ...      | ...        | …   | ...                | ...            |


## **References**
1. <a name="ref1"></a> G. Torriani, R. Albatici, F. Babich, M. Vescovi, M. Zampini, S. Torresin, Developing a principal components model of indoor smellscape perception in office buildings, Build Environ 279 (2025) 113044. https://doi.org/10.1016/j.buildenv.2025.113044.