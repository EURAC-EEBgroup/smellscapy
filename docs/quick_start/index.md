This page provides a quick star guide of the core features of the SmellscaPy package to help you get started quickly.
For a more detailed discussion of functionalities and practical examples please refer to the **[Tutorials](../tutorials/index.md)** section.

## **Installation**
You can install **SmellscaPy** from PyPI using `pip`:

```pyhon
pip install smellscapy
```
Requires **Python 3.12.9+**.

## **Required packages**
SmellscaPy builds upon several widely used Python libraries for data science and visualisation:

- **pandas** – data pre-processing and analysis  
- **numpy** – numerical operations  
- **matplotlib** – core data visualisation  
- **seaborn** – advanced statistical visualisation  
- **smellscapy** – core smellscape analysis functions

```python
# Import the necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import smellscapy as smpy
```

##  **Loading Example Data**
SmellscaPy includes an example dataset to help you explore its features right away.
Use the `load_example_data()` function to load the **sample smellscape dataset**:

```python
# Load example dataset
df = load_example_data()
```

## **Data validation**
Before performing any analysis, it is highly recommended to **validate your dataset** to ensure data quality and consistency.  
The `validate()` function checks for common issues such as:

- Missing or null values  
- Incorrect data types or formatting errors  
- Incomplete or inconsistent records  

It then returns two outputs:

- `df`: a **cleaned and validated DataFrame** ready for analysis  
- `excl_df`: a **DataFrame of excluded records** that did not pass validation, useful for quality control or further inspection


```python
# Validate data
df, excl_df = validate(df)
```

## **Calculations**
Once your data has been validated, you can compute the key **perceptual indices** directly with SmellscaPy by employing the following functions:

- `calculate_pleasantness()` – computes the perceived **pleasantness** score of each smellscape observation  
- `calculate_presence()` – estimates the perceived **presence** score of each smellscape observation


```python
# Compute perceptual indices
df = calculate_pleasantness(df)
df = calculate_presence(df)
```

Each function adds a new column to the DataFrame containing the calculated metric, allowing you to integrate perceptual analysis seamlessly into your data workflow.

## **Plotting** 
 SmellscaPy provides a suite of intuitive and ready-to-use plotting functions to help you **visualise smellscape data** and gain insights into patterns, distributions, and relationships between perceptual variables.  

**Available Plotting Functions:**

- `plot_scatter()` – creates a two-dimensional scatter plot that visualises the relationship between Pleasantness and Presence for each observation.
- `plot_simple_density()` – displays a simplified 2D Kernel Density Estimation (KDE) density plot using only the 50th percentile contour of the distribution. Optionally, the plot can also include the scatter distribution and 1D KDE marginal distributions.
- `plot_density()` – visualises the full 2D density distribution of the dataset using KDE.Optionally, the plot can also include the scatter distribution and 1D KDE marginal distributions.
- `plot_dynamic()` – makes the simple density plot dynamic, showing the temporal evolution of perception over time.

<iframe src="plot_dynamic_example.html"
        width="100%"
        height="600"
        style="border:none;">
</iframe>

```python
# Generate Basic Visualisation
plot_scatter(df)
plot_simple_density(df)
plot_density(df)

# Generate Dynamic Visualisation
plot_dynamic(df)
```
**Tip**: Since all SmellscaPy plotting functions are built on matplotlib and seaborn, you can easily customise them by passing additional arguments or modifying the returned plot objects — for example, adjusting figure size, colour palettes, or adding annotations for publication-quality visuals.

## **Analysis** 
SmellscaPy includes a function for descriptive statistical analysis of computed Perceived Pleasantness and Presence values.
`descriptive_statistics()` allows users to quantitatively explore the main characteristics of their smellscape datasets:

- **Central tendency**: mean and median
- **Dispersion** : variance, standard deviation, minimum, maximum, interquartile range, and coefficient of variation
- **Distribution shape**:  skewness and kurtosis

```python
# Descriptive statistics of pleasantness and presence votes
descriptive_statistics(df)
```