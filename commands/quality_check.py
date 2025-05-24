import pandas as pd

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
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    return {"constant_columns": constant_cols}

# Checking for unique counts of values in each column of the dataframe
def unique_counts(df):
    return df.unique().value_counts().to_dict()

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

# Checkinf for categorical inconsistencies in the dataframe
def categorical_inconsistencies(df, threshold=20):
    categorical_cols = [col for col in df.select_dtypes(include='object') if df[col].nunique() < threshold]
    return {
        col: df[col].value_counts().to_dict
        for col in categorical_cols
    }

def quality_check(df):
    return{
        "missing_values": missing_values(df),
        "duplicate_rows": duplicate_rows(df),
        "data_types": data_types(df),
        "constant_columns": constant_columns(df),
        "unique_counts": unique_counts(df),
        "numeric_range": numeric_range(df),
        "categorical_inconsistencies": categorical_inconsistencies(df)
    }