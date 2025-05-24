import pandas as pd
import numpy as np
from .validations import validate_data

# Checking for missing values in the dataframe
def missing_values(df):
    return df.isnull().sum().to_dict()

# Checking for duplicate rows in the dataframe
def duplicate_rows(df):
    return {"duplicate_rows": int(df.duplicated().sum())}

# Checking the data types in the dataframe
def data_types(df):
    return df.dtypes.astype(str).to_dict()

# Checking for constant columns in the dataframe
def constant_columns(df):
    constant_cols = [col for col in df.columns if df[col].nunique(dropna= False) <= 1]
    return {"constant_columns": constant_cols}

# Checking for unique counts of values in each column of the dataframe
def unique_counts(df):
    return {col: int(df[col].nunique(dropna= False)) for col in df.columns}

# Checking the numeric range of columns in the dataframe
def numeric_range(df):
    numeric_cols = df.select_dtypes(include=['number'])
    return {
        col: {
            "min": float(numeric_cols[col].min()),
            "max": float(numeric_cols[col].max()),
            "mean": float(numeric_cols[col].mean()),
            "std": float(numeric_cols[col].std())
        }
        for col in numeric_cols.columns
    }

# Checking for categorical inconsistencies in the dataframe
def categorical_inconsistencies(df, threshold=20):
    categorical_cols = [col for col in df.select_dtypes(include='object') if df[col].nunique(dropna= False) < threshold]
    return {
        col: df[col].value_counts(dropna= False).to_dict()
        for col in categorical_cols
    }

# Detecting outliers in the dataframe using IQR method
def outlier_detection(df):
    numeric_cols = df.select_dtypes(include= [np.number])
    outliers = {}
    for col in numeric_cols.columns:
        q1 = numeric_cols[col].quantile(0.25)
        q3 = numeric_cols[col].quantile(0.75)
        iqr = q3 -q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        count = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
        if count > 0:
            outliers[col] = int(count)
    return outliers

def quality_check(df, validate= False):
    report = {
        "Missing_values": missing_values(df),
        "Duplicate_rows": duplicate_rows(df),
        "Data_types": data_types(df),
        "Constant_columns": constant_columns(df),
        "Unique_counts": unique_counts(df),
        "Numeric_range": numeric_range(df),
        "Categorical_inconsistencies": categorical_inconsistencies(df),
        "Outliers": outlier_detection(df)
    }

    if validate:
        report["Warnings"] = validate_data(df)
    
    return report