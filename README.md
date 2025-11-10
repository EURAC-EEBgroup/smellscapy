![Smellscapy Logo](docs/Logo.png)

# Smellscapy

[![PyPI version]](.......)
[![Documentation Status]](...)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

**Smellscapy** is a Python library for analysing and representing **indoor smellscape perceptual data**.  
It provides tools for **data validation, calculation of perceptual indices, and visualization** to support reproducible research in sensory and environmental studies.

## Features

- **Data validation & preprocessing** of smellscape survey datasets  
- **Computation of perceptual indicators** (i.e., pleasantness, presence)  
- **Visualizations**: scatter plots, density plots, joint plots  
- **Integration with the Python scientific stack** (Pandas, NumPy, Matplotlib)  
- **Ready-to-use example datasets** for tutorials and testing  

## Installation

Smellscapy can be installed with pip:

```bash
pip install smellscapy
```
Requires **Python 3.12.9+**.

## Quick Start

Here’s a minimal example using the included sample dataset.  
It loads the data, validates it, computes perceptual indicators, and generates simple visualizations:

```python
from smellscapy.surveys import validate
from smellscapy.databases.DataExample import load_example_data
from smellscapy.calculations import calculate_pleasantness, calculate_presence
from smellscapy.plotting.scatter import plot_scatter
from smellscapy.plotting.simple_density import plot_simple_density

# Load example dataset
df = load_example_data()

# Validate data
df, excl_df = validate(df)

# Compute perceptual indices
df = calculate_pleasantness(df)
df = calculate_presence(df)

# Visualization
plot_scatter(df)
plot_simple_density(df)
plot_joint(df)
plot_density(df)
```

Tutorials for using Smellscapy can be found in the [documentation](https://smellscapy.readthedocs.io/en/latest/).

## Citation

If you are using Smellscapy in your research, please help our scientific visibility by citing our work! Please include a citation to our accompanying paper:


G. Torriani, R. Albatici, F. Babich, M. Vescovi, M. Zampini, S. Torresin, Developing a principal components model of indoor smellscape perception in office buildings, Build Environ 279 (2025) 113044. https://doi.org/10.1016/j.buildenv.2025.113044.

## Contributing

If you would like to contribute or if you have any bugs you have found while using `Smellscapy', please feel free to get in touch or submit an issue or pull request!

## Licence
This project is licensed under the BSD 3-Clause License. Please see [LICENSE](LICENCE) for licence guidelines.
