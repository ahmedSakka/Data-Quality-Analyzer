import re
import pandas as pd

# Checking out of range values
def out_of_range(df, column, min_value=None, max_value=None):
    if column not in df.columns:
        return[]
    violations = df[
        (df[column].notnull()) &
        ((min_value is not None and df[column] < min_value) |
         (max_value is not None and df[column] > max_value))
    ]
    return [f"Value {value} at index {i}" for i, value in violations[column].items()]

# Checking for invalid email formats
def invalid_email(df, column):
    if column not in df.columns:
        return []
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return [
        f"invalid email at index {i}: {value}"
        for i, value in df[column].dropna().items()
        if not re.match(pattern, str(value))
    ]

# Checking for negative values where only positives are expected
def negative_values(df, column):
    if column not in df.columns:
        return []
    negatives = df[df[column] < 0]
    return [f"Negative value {value} at index {i}" for i, value in negatives[column].items()]

# Checking for null critical columns
def required_fields(df, column):
    if column not in df.columns:
        return []
    nulls = df[df[column].isna()]
    return [f"Null value at index {i}" for i in nulls.index]

# Collecting all validation checks warnings
def validate_data(df, checks):
    warnings = {}

    # Defining your validation rules here
    rules = {
        "age": [lambda df: out_of_range(df, "age", 0, 120)],
        "email": [invalid_email],
        "price": [negative_values],
        "Country": [required_fields],
    }

    for column, checks in rules.items():
        for check in checks:
            issues = check(df)
            if issues:
                warnings.setdefault(column, []).extend(issues)

    return warnings