"""CSV file reading module.

This module reads a previously validated CSV file and converts its contents
into a pandas DataFrame for subsequent validation and analysis.

The source file is expected to be provided as a `Path` object. All CSV
columns are loaded as strings, and empty cells are preserved instead of
being automatically converted into missing values.

File-system, empty-file, and CSV parsing errors are converted into the
application-specific `FileReadError` exception.
"""
from pathlib import Path
import pandas as pd
from src.errors import FileReadError


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Read a validated CSV file into a pandas DataFrame.

    Reads the CSV file using UTF-8 encoding and loads every column as a
    string so that raw values can be validated consistently by later
    application modules.

    Empty cells are preserved as empty strings by disabling pandas'
    default missing-value conversion.

    Args:
        file_path: Validated filesystem path pointing to the source CSV file.

    Returns:
        A DataFrame containing the raw CSV data with all columns loaded as
        strings and empty cells preserved.

    Raises:
        FileReadError: If the file cannot be read, contains no data, or
            cannot be parsed as a valid CSV file.
    """
    try:
        df_raw = pd.read_csv(file_path, dtype=str, keep_default_na=False, encoding="utf-8")
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise FileReadError() from e
    return df_raw