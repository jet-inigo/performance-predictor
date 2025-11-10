# usage: from student_loader import load_student_dataset, load_student_subset
# load_student_dataset(path)
# load_student_subset(n, path)

import pandas as pd
from pathlib import Path

# Define the expected data types for each column
DTYPES = {
    "STUDENT_ID": "string",
    "ADMISSION_TYPE": "string",
    "STUDY_PROGRAM": "string",
    "TEST_SCORE_NEEDED_MAJOR": "float64",
    "ENTRY_TERM": "int64",
    "TEST_SCORE": "float64",
    "TERM_CODE": "int64",
    "TERM_GPA": "float64",
    "OVERALL_GPA": "float64",
    "HOURS_TAKEN": "float64",
    "HOURS_FINISHED": "float64",
    "HOURS_PASSED": "float64",
    "HOURS_FAILED": "float64",
    "HOURS_DROPPED": "float64",
    "SCHOOL_ID": "string",
}

def load_student_dataset(path: str = "anonymized/student_info_anonymized.csv") -> pd.DataFrame:
    """
    Load the full student performance dataset with correct data types.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The dataset with proper column types.
    """
    path = Path(path)

    # Load CSV without dtype enforcement to avoid conversion errors
    df = pd.read_csv(path, sep=';', low_memory=False)

    # Convert each column safely according to DTYPES
    for col, dtype in DTYPES.items():
        if col not in df.columns:
            continue
        if dtype.startswith("float") or dtype.startswith("int"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif dtype == "string":
            df[col] = df[col].astype("string")

    return df


def load_student_subset(n: int, path: str = "anonymized/student_info_anonymized.csv") -> pd.DataFrame:
    """
    Load a subset (first n rows) of the student dataset with correct data types.

    Args:
        n (int): Number of rows to load.
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Subset of dataset.
    """
    path = Path(path)

    # Load CSV without dtype enforcement to avoid conversion errors
    df = pd.read_csv(path, sep=';', low_memory=False, nrows=n)

    # Convert each column safely according to DTYPES
    for col, dtype in DTYPES.items():
        if col not in df.columns:
            continue
        if dtype.startswith("float") or dtype.startswith("int"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif dtype == "string":
            df[col] = df[col].astype("string")

    return df


if __name__ == "__main__":
    df_full = load_student_dataset()
    print(df_full.info())
    print(df_full.head())

    print("\nSubset:")
    df_subset = load_student_subset(5)
    print(df_subset)
