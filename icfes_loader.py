# usage: from icfes_loader import load_icfes_dataset, load_icfes_subset
# load_icfes_dataset(path)
# load_icfes_subset(n, path)

import pandas as pd
from pathlib import Path

# Explicit column data types (as before)
DTYPES = {
    "SCHOOL_ID": "string",
    "PUNT_LECTURA_CRITICA": "float64",
    "PERCENTIL_LECTURA_CRITICA": "float64",
    "PUNT_MATEMATICAS": "float64",
    "PERCENTIL_MATEMATICAS": "float64",
    "PUNT_C_NATURALES": "float64",
    "PERCENTIL_C_NATURALES": "float64",
    "PUNT_SOCIALES_CIUDADANAS": "float64",
    "PERCENTIL_SOCIALES_CIUDADANAS": "float64",
    "PUNT_INGLES": "float64",
    "PERCENTIL_INGLES": "float64",
    "PUNT_GLOBAL": "float64",
    "PERCENTIL_GLOBAL": "float64",
    "semestre": "int64"
}

def load_icfes_dataset(path: str = "anonymized/icfes_combined_anonymized.csv") -> pd.DataFrame:
    """
    Load the full ICFES dataset with correct data types.
    Automatically handles non-numeric values gracefully.
    """
    path = Path(path)

    # Read once without dtype enforcement to avoid header casting errors
    df = pd.read_csv(path, sep=';', low_memory=False)

    # Convert numeric columns safely
    for col, dtype in DTYPES.items():
        if col not in df.columns:
            continue  # skip if column missing
        if dtype.startswith("float") or dtype.startswith("int"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif dtype == "string":
            df[col] = df[col].astype("string")

    return df


def load_icfes_subset(n: int, path: str = "anonymized/icfes_combined_anonymized.csv") -> pd.DataFrame:
    """
    Load a subset (first n rows) of the ICFES dataset with correct data types.

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
    df_full = load_icfes_dataset()
    print(df_full.info())
    print(df_full.head())

    print("\nSubset:")
    df_subset = load_icfes_subset(5)
    print(df_subset)
