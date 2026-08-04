"""File reading and pandas conversion module.

This module converts an input Path object (previously validated) into a pandas DataFrame object.
"""
from pathlib import Path
import pandas as pd
from src.errors import FileReadError


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Reads a CSV file and converts it into a pandas DataFrame.

    This function receives a Path object to subsequently
    convert it into a pandas DataFrame object.

    Args:
        file_path: The filesystem path of the file to be converted.

    Returns:
        pd.DataFrame: A tabular DataFrame containing the raw CSV data,
            as string, with empty cells preserved for validation

    Raises:
        FileReadError: If the CSV file cannot be read, is empty,
            or contains parsing errors.
    """
    try:
        df_raw = pd.read_csv(file_path, dtype=str, keep_default_na=False)
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise FileReadError() from e
    return df_raw