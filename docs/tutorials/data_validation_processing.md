SmellscaPy provides a function for data validation and for checking for data quality issues.

```python
# Validate the dataset
df, excl_df = validate(df)
```

The `validate()` function performs several checks on the data:

- **Mandatory column check**: it verifies that all mandatory columns are present in the input DataFrame. If any are missing, the function raises an exception listing the missing column names.

- **Attribute value validation**: it checks that all values in the perceptual attribute qualities columns are integers [1, 2, 3, 4, 5].

- **Missing data detection and removal**: the function scans the perceptual attribute qualities columns for missing values (NaN). Any rows containing missing attribute values are removed from the dataset.

The cleaned DataFrame (df) is returned as the first output. A second DataFrame (excl_df), containing the rows that were excluded due to invalid or missing data, is returned as the second output. If no rows were excluded, this will be None.