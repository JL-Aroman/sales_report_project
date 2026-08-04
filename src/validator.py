"""CSV file and sales data validation module.

This module validates input CSV file paths, normalizes raw sales data,
and applies independent validation rules to pandas DataFrames.

Each validation rule is implemented in a separate helper function to keep
the validation process modular, maintainable, and easy to extend. The main
validation function coordinates these helpers, separates valid and invalid
records, collects errors and warnings, and prepares valid sales data for
analysis.
"""

from pathlib import Path
import pandas as pd
import re
from typing import Any, Dict, List
from src.errors import (
    EmptyPathError,
    FileNotFoundAppError,
    InvalidFilePathError,
    InvalidFileExtensionError,
    EmptyFileError, 
    FileReadError,
    EmptyDataFrameError,
    MissingColumnsError
)

REQUIRED_COLUMNS = [
    "producto_id",
    "producto",
    "categoria",
    "precio",
    "cantidad",
    "fecha"
]

def validate_csv_file(file_path: str) -> Path:
    """Validate a CSV file path and return it as a Path object.

Converts a string path into a Path object and verifies that the path
is not empty, exists in the file system, points to a regular file,
has a CSV extension, contains data, and can be read.

Args:
    file_path: String containing the path of the CSV file to validate.

Returns:
    A validated Path object ready for the CSV reading process.

Raises:
    EmptyPathError: If the provided path is None or empty.
    FileNotFoundAppError: If the path does not exist.
    InvalidFilePathError: If the path does not point to a regular file.
    InvalidFileExtensionError: If the file extension is not `.csv`.
    EmptyFileError: If the file contains zero bytes.
    FileReadError: If the file cannot be read
    """
    if file_path is None or file_path.strip() == "":
        raise EmptyPathError()
    new_file_path = Path(file_path)
    if not new_file_path.exists():
        raise FileNotFoundAppError()
    if not new_file_path.is_file():
        raise InvalidFilePathError()
    suffix = new_file_path.suffix
    if suffix.lower() != ".csv":
        raise InvalidFileExtensionError()
    if new_file_path.stat().st_size == 0:
        raise EmptyFileError()
    try:
        new_file_path.read_text()
    except OSError as e:
        raise FileReadError() from e
    return new_file_path

def normalize_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize string values in a raw sales DataFrame.

Creates a copy of the original DataFrame and applies field-specific
normalization rules. The function removes unnecessary whitespace,
converts product identifiers to uppercase, and preserves the original
DataFrame unchanged.

The input DataFrame is expected to contain the columns defined in
`REQUIRED_COLUMNS`, with their values represented as strings.

Args:
    df_raw: Raw DataFrame containing sales records as strings.

Returns:
    A new DataFrame containing normalized string values.
    """
    df_normalized = df_raw.copy()
    df_normalized["producto_id"] = df_normalized["producto_id"].str.replace(r"\s+", "", regex=True).str.upper()
    df_normalized["producto"] = df_normalized["producto"].str.replace(r"\s+", " ", regex=True).str.strip()
    df_normalized["categoria"] = df_normalized["categoria"].str.replace(r"\s+", " ", regex=True).str.strip()
    df_normalized["precio"] = df_normalized["precio"].str.replace(r"\s+", "", regex=True)
    df_normalized["cantidad"] = df_normalized["cantidad"].str.replace(r"\s+","", regex=True)
    df_normalized["fecha"] = df_normalized["fecha"].str.replace(r"\s+", "", regex=True)
    return df_normalized

def validated_empty_values(df_normalized: pd.DataFrame) -> Dict[str,Any]:
    """Detect empty values in the required DataFrame columns.

Examines every required column and records an error whenever an empty
string is found. Each affected row index is included in the invalid-index
collection so that the row can later be separated from valid records.

The reported CSV line number includes the header row, so two is added
to each DataFrame row index.

Args:
    df_normalized: Normalized DataFrame containing the sales records
        to validate.

Returns:
    A dictionary containing the following keys:

    - `invalid_indexes`: Row indexes containing empty required values.
    - `errors`: Detailed errors for every empty field detected.
    """
    validation_result = {
        "invalid_indexes": [],
        "errors": []
    }
    for column in REQUIRED_COLUMNS:
        empty_mask = list(df_normalized[column] == "")
        for i in range(len(empty_mask)):
            if empty_mask[i]:
                validation_result["errors"].append({
                "line_number": i + 2,
                "column": column,
                "error_type": "empty_value",
                "message": f"{column} vacío.",
                "original_value": ""
                })
                validation_result["invalid_indexes"].append(i)
    return validation_result

def validated_price(df_normalized: pd.DataFrame) -> Dict[str,Any]:
    """Validate price values in a normalized sales DataFrame.

Verifies that every non-empty value in the `precio` column can be
converted to a numeric value and is greater than zero.

Empty values are skipped because they are handled separately by
`validated_empty_values()`.

Args:
    df_normalized: Normalized DataFrame containing the sales records
        to validate.

Returns:
    A dictionary containing the following keys:

    - `invalid_indexes`: Row indexes containing invalid prices.
    - `errors`: Detailed errors for non-numeric, zero, or negative
      price values.
    """
    validation_result = {
        "invalid_indexes": [],
        "errors": []
    }
    for index, value in df_normalized["precio"].items():
        if value == "":
            continue
        try:
            new_value = float(value)
            if new_value <= 0:
                validation_result["errors"].append({
                    "line_number": index + 2,
                    "column": "precio",
                    "error_type": "negative_or_zero_value",
                    "message": "precio inválido. Debe ser mayor que 0.",
                    "original_value": value
                })
                validation_result["invalid_indexes"].append(index)
        except (ValueError, TypeError):
            validation_result["errors"].append({
                "line_number": index + 2,
                "column": "precio",
                "error_type": "invalid_number",
                "message": "precio inválido. Se esperaba un número mayor que 0.",
                "original_value": value  
            })
            validation_result["invalid_indexes"].append(index)
    return validation_result

def validated_amount(df_normalized: pd.DataFrame) -> Dict[str,Any]:
    """Validate quantity values in a normalized sales DataFrame.

Verifies that every non-empty value in the `cantidad` column can be
converted to a number, represents a whole number, and is greater than
zero. Decimal quantities are not accepted in version 1.0.

Empty values are skipped because they are handled separately by
`validated_empty_values()`.

Args:
    df_normalized: Normalized DataFrame containing the sales records
        to validate.

Returns:
    A dictionary containing the following keys:

    - `invalid_indexes`: Row indexes containing invalid quantities.
    - `errors`: Detailed errors for non-numeric, decimal, zero, or
      negative quantity values.
    """
    validation_result = {
        "invalid_indexes": [],
        "errors": []
    }
    for index, value in df_normalized["cantidad"].items():
        if value == "":
            continue
        try:
            new_value = float(value)
            if not new_value.is_integer():
                validation_result["errors"].append({
                    "line_number": index + 2,
                    "column": "cantidad",
                    "error_type": "decimal_not_allowed",
                    "message": "cantidad inválida. No se aceptan decimales en la versión 1.0.",
                    "original_value": value
                })
                validation_result["invalid_indexes"].append(index)
            elif new_value <= 0:
                validation_result["errors"].append({
                    "line_number": index + 2,
                    "column": "cantidad",
                    "error_type": "negative_or_zero_value",
                    "message": "cantidad inválida. Debe ser mayor que 0.",
                    "original_value": value  
                })
                validation_result["invalid_indexes"].append(index)
        except (ValueError, TypeError):
            validation_result["errors"].append({
                "line_number": index + 2,
                "column": "cantidad",
                "error_type": "invalid_integer",
                "message": "cantidad inválida. Se esperaba un número entero mayor que 0.",
                "original_value": value 
            })
            validation_result["invalid_indexes"].append(index)
    return validation_result

def validated_date(df_normalized: pd.DataFrame) -> Dict[str,Any]:
    """Validate date values in a normalized sales DataFrame.

    Verifies that every non-empty value in the `fecha` column follows the
    `YYYY-MM-DD` format and represents and existing calendar date.

    Empty values are skipped because they are handled separately by 
    `validated_empty_values()`

    Args:
        df_normalized: Normalized DataFrame containing the sales records
            to validate.

    Returns:
        A dictionary containing the following keys:

        - `invalid_indexes`: Row indexes containing invalid dates.
        - `errors`: Detailed errors for incorrect date formats or 
        nonexistent caldendar dates.
    """
    validation_result = {
        "invalid_indexes": [],
        "errors": []
    }
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    for index, value in df_normalized["fecha"].items():
        if value == "":
            continue
        if not isinstance(value, str) or not re.match(date_pattern, value):
            validation_result["errors"].append({
                "line_number": index + 2,
                "column": "fecha",
                "error_type": "invalid_date_format",
                "message": "fecha inválida. Se esperaba el formato YYYY-MM-DD.",
                "original_value": value
            })
            validation_result["invalid_indexes"].append(index)
            continue
        try:
            pd.to_datetime(value, format="%Y-%m-%d")
        except ValueError:
            validation_result["errors"].append({
                "line_number": index + 2,
                "column": "fecha",
                "error_type": "invalid_date_format",
                "message": "fecha inválida. La fecha no existe en el calendario.",
                "original_value": value
            })
            validation_result["invalid_indexes"].append(index)
    return validation_result

def detect_warnings(df_valid_rows: pd.DataFrame) -> Dict[str,Any]:
    """Detected non-critical inconsistencies in valid sales records.

    Groups valid records by `producto_id` and verifies that every product 
    identifier is associated eith a consistent product name.

    When the same identifier appears with different product names, the
    incosistency is registered as a warning without invalidating the
    affected records.

    Args:
        df_valid_rows: DataFrame containing sales records that passed all
            critical validation rules.

    Returns:
        A dictionary containing a `warnings` key with the detected
            product-name inconsistencies.
    """
    validated_result = {
        "warnings": []
    }
    df_group_by_producto_id = df_valid_rows.groupby("producto_id")
    for producto_id, group in df_group_by_producto_id:
        values = []
        for index, value in group["producto"].items():
            values.append(value)
        if len(set(values)) != 1:
            values = list(dict.fromkeys(values))
            validated_result["warnings"].append({
                "warning_type": "inconsistent_product_name",
                "field": "producto",
                "message": f"El producto_id {producto_id} aparece con nombres diferentes.",
                "affected_value": producto_id,
                "details": values
            })
    return validated_result

def validate_dataframe(df_raw: pd.DataFrame) -> Dict[str, Any]:
    """Validate the structure and contents of a raw sales DataFrame.

    Verifies thath the DataFrame contains data and includes all required
    columns. It then normalizes the sales records and coordinates the 
    independent validation function for empty values, prices, quantities, 
    and dates.

    Rows containing one or more critiacl errors are separrated from valid
    rows. Numeric fields and dates in valid rows are converted to their
    appropriate pandas data types. Non-critical producto-name incosistencies
    are collected separately as warnings

    Args:
        df_raw: Raw pandas DataFrame containing sales records as strings.
    
    Returns:
        A dictionary containing the following keys:

        - `df_valid_rows`: DataFrame containing records that passed all 
        critical validation rules.
        - `df_invalid_rows`: DataFrame containing records with one or more validations
        errors.
        - `errors`: Flat list containing detailed validation errors.
        - `warnings`: Flat list containing non-critical data inconsistencies.
        - `total_rows`: Total number of normalized sales records.
        - `total_valid_rows`: Number of records that passed validation.
        - `total:invalid_rows`: Number of records containing errors.

    Raises:
        EmptyDataFrameError: If the input DataFrame containings no rows or usable data.
        MissingColumnsError: If one or mor required columns are missings.
    """
    if df_raw.empty:
        raise EmptyDataFrameError()
    if set(REQUIRED_COLUMNS).issubset(df_raw.columns):
        df_normalized = normalize_dataframe(df_raw)
        errors = []
        warnings = []
        invalid_indexes = []
        validated_empty_value_dict = validated_empty_values(df_normalized)
        errors.extend(validated_empty_value_dict["errors"])
        invalid_indexes.extend(validated_empty_value_dict["invalid_indexes"])
        validate_price_dict = validated_price(df_normalized)
        errors.extend(validate_price_dict["errors"])
        invalid_indexes.extend(validate_price_dict["invalid_indexes"])
        validated_amount_dict = validated_amount(df_normalized)
        errors.extend(validated_amount_dict["errors"])
        invalid_indexes.extend(validated_amount_dict["invalid_indexes"])
        validated_date_dict = validated_date(df_normalized)
        errors.extend(validated_date_dict["errors"])
        invalid_indexes.extend(validated_date_dict["invalid_indexes"])
        numeric_columns = ["precio","cantidad"]
        invalid_indexes = list(set(invalid_indexes))
        invalid_indexes = sorted(invalid_indexes)
        df_valid_rows = df_normalized[~df_normalized.index.isin(invalid_indexes)].copy()
        df_valid_rows[numeric_columns] = df_valid_rows[numeric_columns].apply(pd.to_numeric, errors="coerce")
        df_valid_rows["fecha"] = pd.to_datetime(df_valid_rows["fecha"], format="%Y-%m-%d", errors="coerce")
        df_invalid_rows = df_normalized.loc[invalid_indexes].copy()
        validated_warnings_dict = detect_warnings(df_valid_rows)
        warnings.extend(validated_warnings_dict["warnings"])
        validation_result ={
            "df_valid_rows": df_valid_rows,
            "df_invalid_rows": df_invalid_rows,
            "errors": errors,
            "warnings": warnings,
            "total_rows": len(df_normalized),
            "total_valid_rows": len(df_valid_rows),
            "total_invalid_rows": len(df_invalid_rows)
        }
        return validation_result
    else:
        raise MissingColumnsError()


