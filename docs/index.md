![Smellscapy Logo](https://raw.githubusercontent.com/EURAC-EEBgroup/smellscapy/main/docs/Logo.png) <!-- markdownlint-disable-line MD041 -->

# **Welcome to SmellscaPy**

[![PyPI version](https://badge.fury.io/py/smellscapy.svg)](https://badge.fury.io/py/smellscapy)
[![Docs status](https://github.com/EURAC-EEBgroup/smellscapy/actions/workflows/docs.yml/badge.svg)](https://github.com/EURAC-EEBgroup/smellscapy/actions/workflows/docs.yml)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


**SmellscaPy** is a Python library for analysing and representing **indoor smellscape perceptual data**.  
It provides tools for **data validation, calculation of perceptual indices, visualization, descriptive statistics** to support reproducible research in smellscape studies.

## **Key Features**

- **Data validation & preprocessing** of smellscape survey datasets  
- **Computation of perceptual indicators** (i.e., pleasantness, presence)  
- **Visualizations**: scatter plots, density plots, simplified density plots, dynamic plots 
- **Integration with the Python scientific stack** (Pandas, NumPy, Matplotlib)  
- **Ready-to-use example datasets** for tutorials and testing
- **Analysis**: descriptive statistics

<iframe src="plot_dynamic_example.html"
        width="100%"
        height="600"
        style="border:none;">
</iframe>


## **Installation**

SmellscaPy can be installed with pip:

```bash
pip install smellscapy
```
Requires **Python 3.12.9+**.

## **Documentation**
This [documentation](overview/index.md) is designed to help you understand and use SmellscaPy effectively.

### **Tutorials**
Practical examples showing how to use our project in real-world scenarios. For more information, please see the [Tutorials](tutorials/index.md) section.

<!-- ## **Web Application**

A web app is available to use the library directly through an interface at the following [link]...... -->

## **License**

This project is licensed under the BSD 3-Clause License. Please see [LICENSE](license.md) for licence guidelines.

## **Contributing**

If you would like to contribute or if you have any bugs you have found while using `SmellscaPy', please feel free to get in touch or submit an issue or pull request!

## **Aknowledgment**
The smellscape-representation methods implemented in the plotting functions of SmellscaPy are derived and adapted from the probabilistic soundscape framework described in the publication by Andrew Mitchell et al. [[1]](#ref1) and implemented in the Soundscapy open-source library (c) 2025, Andrew Mitchell All rights reserved [[2]](#ref2).
We gratefully acknowledge the authors of Soundscapy for their conceptual and methodological foundation, which significantly informed the development of the smellscape visualisation tools in this project.

## **Citation** 

Please cite us if you use the _SmellscaPy_ library: 

G. Torriani, R. Albatici, F. Babich, M. Vescovi, M. Zampini, S. Torresin, Developing a principal components model of indoor smellscape perception in office buildings, Build Environ 279 (2025) 113044. https://doi.org/10.1016/j.buildenv.2025.113044.


1. <a name="ref1"></a> Mitchell, A., Aletta, F., & Kang, J. (2022). How to analyse and represent quantitative soundscape data. _JASA Express Letters, 2_, 37201.
2. <a name="ref2"></a> Mitchell, A. (2024, October). Soundscapy: A python package for soundscape assessment and analysis. In INTER-NOISE and NOISE-CON Congress and Conference Proceedings (Vol. 270, No. 7, pp. 4029-4039). Institute of Noise Control Engineering.
