This page provides a quick star guide of the core features of the SmellscaPy package to help you get started quickly.
For a more detailed discussion of advanced functionalities — including step-by-step workflows, practical examples, and best practices — please refer to the **[User Guide](../user_guide/index.md)** and **[Tutorials](../tutorials/index.md)** sections.

## Installation
Smellscapy can be installed with pip:

```pyhon
pip install smellscapy
```
Requires **Python 3.12.9+**.

## Required packages
SmellscaPy uses several key packages:
 - **pandas**, for data pre-processing and analysis
 - **matplotlib** and **seaborn**, for data visualisation
 - **numpy**, for numerical operations
 - .........
 - **smellscapy**, for smellscape analysis

```python
# Import the necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import smellscapy as smpy
```

##  Loading Example Data


```python
# Load example dataset
df = load_example_data()
```

## Data validation

```python
# Validate data
df, excl_df = validate(df)
```

## Calculations
```python
# Compute perceptual indices
df = calculate_pleasantness(df)
df = calculate_presence(df)
```

## Plotting 
 
```python
# Visualization
plot_scatter(df)
plot_simple_density(df)
plot_joint(df)
plot_density(df)
```