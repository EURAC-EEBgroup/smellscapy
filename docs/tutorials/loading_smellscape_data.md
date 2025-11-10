## **Loading example data**
An **example dataset** is included with SmellscaPy to help you explore its features right away. Use the `load_example_data()` function to load the example dataset:

```python
# Load example dataset
df = load_example_data()
```
The example dataset includes the following columns:

- **StudyID**: Unique identifier of the study
- **ParticipantID**: Unique participant ID
- **LocationID**: Name of the city where the study was conducted
- **pleasant**, **present**, **light**, **engaging**, **unpleasant**, **absent**, **overpowering**, **detached**: perceptual quality attributes

In addition, the dataset containes several optional variables:

- **How long have you been in your office without leaving?** – Duration of continuous stay in the office
- **How many people are currently present in your office room?** – Number of people sharing the same office
- **How would you rate your current mood?** – Self-reported mood
- **In this moment, how productive do you feel?** – Self-reported productivity
- **Smell source** – Dominant category of perceived smell source

These data were collected in **Bolzano, Italy**, during an office-based experimental campaign in 2025 involving **17 participants**.

```python
# Display basic information about the example dataset
print(f"Dataset shape: {df}")
print(f"Columns ({len(df.columns)}): {list(df.columns)}")
```


## **Loading your data**
If you have your own smellscape survey data, you can load it using pandas and then process it with SmellscaPy.

```python
# Load data from a CSV file
my_data = pd.read_csv('path/to/your/data.csv')
```

To use smellscapy, your input dataset must contain the following mandatory columns:

- **ResearcherID**
- **RecordID**
- **LocationID**
- **pleasant**, **present**, **light**, **engaging**, **unpleasant**, **absent**, **overpowering**, **detached**

Make sure that the column names match exactly as listed above. If your dataset uses different names, you will need to **rename the columns** before using SmellscaPy.

Additional requirements:

- **No missing values** are allowed in these columns.
- The values for the **eight perceptual attribute columns** must be **numeric**, ranging from 1 (corresponding to "Strongly disagree") to 5 (corresponding to "Strongly agree). 

Besides these required fields, you are free to include any other **additional columns** in your dataset as needed.

Please, refer to **[DataExample.csv](./DataExample.csv)** for a reference dataset.

