## **Loading example data**


Two **example datasets** are included with SmellscaPy to allow users to explore the package’s functionalities immediately. 
**DataExample_Eurac.csv** contains data collected by Eurac Research from 17 participants through a repeated questionnaire campaign conducted in an office building in Bolzano (Italy) between May and September 2025, and can be loaded using the `load_example_data_Eurac()` function. 
**DataExample_Measure2_Unitn.csv** refers to a controlled laboratory olfactory experiment involving 35 participants, carried out within the MEASURE 2.0 project at the University of Trento (Italy), and can be loaded using the `load_example_data_Measure2_Unitn()` function. 


```python
# Load example dataset
df = smpy.load_example_data_Eurac()
#or
df = smpy.load_example_Measure2_Unitn()
```
Both datasets contain both mandatory and optional variables. The mandatory columns are:

- **pleasant**, **present**, **light**, **engaging**, **unpleasant**, **absent**, **overpowering**, **detached**: perceptual quality attributes


```python
# Display basic information about the example dataset
print(f"Dataset shape: {df}")
print(f"Columns ({len(df.columns)}): {list(df.columns)}")
```


## **Loading your data**
If you have your own smellscape survey data, you can load it using pandas and then process it with SmellscaPy.

```python
import pandas as pd

# Load data from a CSV file
my_data = pd.read_csv('path/to/your/data.csv')
```

To use smellscapy, your input dataset must contain the following mandatory columns:

- **pleasant**, **present**, **light**, **engaging**, **unpleasant**, **absent**, **overpowering**, **detached**

Make sure that the column names match exactly as listed above. If your dataset uses different names, you will need to **rename the columns** before using SmellscaPy.

Additional requirements:

- **No missing values** are allowed in these columns.
- The values for the **eight perceptual attribute columns** must be **numeric**, ranging from 1 (corresponding to "Strongly disagree") to 5 (corresponding to "Strongly agree). 

Besides these required fields, you are free to include any other **additional columns** in your dataset as needed.

Please, refer to **[DataExample.csv](./DataExample.csv)** for a reference dataset.

