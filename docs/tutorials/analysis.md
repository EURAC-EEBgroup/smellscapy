SmellscaPy provides two functions for **statistical data analysis** of the **pleasantness** and **presence** score of a provided DataFrame.

```python
# Descriptive statistics
df = descriptive_statistics(df)

# Linear Mixed Model (LMM)
df = lmm_pleasantness(df)
df = lmm_presence(df)
```
## **Descriptive statistics**

The `descriptive_statistics()` computes and summarises the descriptive statistics of the smellscape dataset, focusing on the numerical variables
**pleasantness_score** and **presence_score**.

This function provides a concise statistical overview of the dataset, allowing users to interpret how perceived pleasantness and presence values are distributed—either overall or within subgroups defined by a categorical variable.

The analysis includes three main statistical dimensions:

- **Central tendency** : mean and median.
- **Dispersion** :  variance, standard deviation, minimum, maximum, interquartile range (IQR), and coefficient of variation.
- **Distribution shape**: skewness and kurtosis, indicating whether perceptions are symmetrically distributed or exhibit heavy/light tails.

If a **group_by_col** parameter is provided, the statistics are computed for each subgroup.
Otherwise, the function returns an aggregated summary for the entire dataset.

```python
#Descriptive statistics
s = descriptive_statistics(df)

#Descriptive statistics, grouped
s = descriptive_statistics (df, group_by_col="Smell source")

```

| Type        | Pleasantness | Presence  | Subgroup          |
|--------------|--------------|-----------|-------------------|
| **count**    | 40.0         | 40.0      | Body odours       |
| **mean**     | -0.0455      | -0.1461   | Body odours       |
| **std**      | 0.1966       | 0.2419    | Body odours       |
| **min**      | -0.3536      | -0.6464   | Body odours       |
| **25%**      | -0.2071      | -0.3308   | Body odours       |
| **50%**      | -0.0732      | -0.0581   | Body odours       |
| **75%**      | 0.1036       | 0.0000    | Body odours       |
| **max**      | 0.5000       | 0.5000    | Body odours       |
| **variance** | 0.0386       | 0.0585    | Body odours       |
| **skewness** | 0.5230       | 0.0322    | Body odours       |
| **kurtosis** | -0.1412      | -0.0707   | Body odours       |
| **count**    | 15.0         | 15.0      | Cleaning products |
| **mean**     | 0.2715       | 0.0775    | Cleaning products |
| **std**      | 0.1415       | 0.1431    | Cleaning products |
| **min**      | 0.0732       | -0.1893   | Cleaning products |
| **25%**      | 0.1679       | 0.0089    | Cleaning products |
| **50%**      | 0.2803       | 0.0607    | Cleaning products |
| **75%**      | 0.3384       | 0.1919    | Cleaning products |
| **max**      | 0.5732       | 0.2803    | Cleaning products |
| **variance** | 0.0200       | 0.0205    | Cleaning products |
| **skewness** | 0.3948       | -0.2815   | Cleaning products |
| **kurtosis** | -0.0680      | -0.6162   | Cleaning products |
| ...          | ...          | ...       | ...               |