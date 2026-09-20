"""CSV file and sales data validation module.

This module validates input CSV file paths, normalizes raw sales data, and
applies independent validation rules to pandas DataFrames.

Each validation rule is implemented in a separate helper function to keep
the validation process modular, maintainable, and easy to extend.

The main `validate_dataframe()` function coordinates normalization and
validation, collects detailed errors, separates valid and invalid records,
detects non-critical warnings, converts valid values to their appropriate
data types, and prepares validated sales data for analysis.

Required sales fields include product identifiers, product names, categories,
prices, quantities, and dates.

Optional fields such as `ciudad` and `metodo_pago` are preserved and
normalized when present without being required for the core validation
workflow.
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

    Converts the provided string path into a `Path` object and verifies that
    the path is not empty, exists in the file system, points to a regular
    file, has a `.csv` extension, contains at least one byte, and can be
    opened for reading.

    File readability is verified by opening the file in binary mode and
    reading a single byte. CSV contents are not parsed or decoded by this
    function; that responsibility belongs to the CSV-reading module.

    Args:
        file_path: String containing the path of the CSV file to validate.

    Returns:
        A validated `Path` object ready for the CSV-reading process.

    Raises:
        EmptyPathError: If the provided path is `None` or empty.
        FileNotFoundAppError: If the path does not exist.
        InvalidFilePathError: If the path does not point to a regular file.
        InvalidFileExtensionError: If the file extension is not `.csv`.
        EmptyFileError: If the file contains zero bytes.
        FileReadError: If the file cannot be opened or read.
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
        with new_file_path.open("rb") as file:
            file.read(1)
    except OSError as e:
        raise FileReadError() from e
    return new_file_path

def normalize_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Normalize string values in a raw sales DataFrame.

    Creates a copy of the original DataFrame and applies field-specific
    normalization rules while preserving the original input unchanged.

    Normalization includes:

    - Removing all whitespace from `producto_id` and converting it to
      uppercase.
    - Collapsing repeated whitespace and trimming `producto`.
    - Collapsing repeated whitespace and trimming `categoria`.
    - Removing whitespace from `precio`.
    - Removing whitespace from `cantidad`.
    - Removing whitespace from `fecha`.

    When the optional `ciudad` or `metodo_pago` columns are present, leading,
    trailing, and repeated internal whitespace is also normalized.

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
    if "ciudad" in df_normalized:
        df_normalized["ciudad"] = df_normalized["ciudad"].str.replace(r"\s+", " ", regex=True).str.strip()
    if "metodo_pago" in df_normalized:
        df_normalized["metodo_pago"] = df_normalized["metodo_pago"].str.replace(r"\s+", " ", regex=True).str.strip()
    return df_normalized

def validated_empty_values(df_normalized: pd.DataFrame) -> Dict[str,Any]:
    """Detect empty values in required sales columns.

    Examines every column listed in `REQUIRED_COLUMNS` and records a
    validation error whenever an empty string is found.

    Every affected row index is added to `invalid_indexes` so the row can
    later be separated from valid sales records.

    Reported CSV line numbers include the header row, so two is added to the
    corresponding DataFrame row position.

    Args:
        df_normalized: Normalized DataFrame containing the sales records to
            validate.

    Returns:
        A dictionary containing:

        - `invalid_indexes`: Row indexes containing empty required values.
        - `errors`: Detailed validation errors for every empty field detected.
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
        df_normalized: Normalized DataFrame containing the sales records to
            validate.

    Returns:
        A dictionary containing:

        - `invalid_indexes`: Row indexes containing invalid prices.
        - `errors`: Detailed validation errors for non-numeric, zero, or
          negative price values.
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
    zero.

    Decimal quantities are not accepted.

    Empty values are skipped because they are handled separately by
    `validated_empty_values()`.

    Args:
        df_normalized: Normalized DataFrame containing the sales records to
            validate.

    Returns:
        A dictionary containing:

        - `invalid_indexes`: Row indexes containing invalid quantities.
        - `errors`: Detailed validation errors for non-numeric, decimal,
          zero, or negative quantity values.
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
                    "message": "cantidad inválida. No se aceptan valores decimales.",
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
    `YYYY-MM-DD` format and represents an existing calendar date.

    The format is checked first using a regular expression. Values with the
    correct structure are then validated through pandas to confirm that the
    represented calendar date exists.

    Empty values are skipped because they are handled separately by
    `validated_empty_values()`.

    Args:
        df_normalized: Normalized DataFrame containing the sales records to
            validate.

    Returns:
        A dictionary containing:

        - `invalid_indexes`: Row indexes containing invalid dates.
        - `errors`: Detailed validation errors for incorrect date formats or
          nonexistent calendar dates.
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
    """Detect non-critical inconsistencies in valid sales records.

    Groups valid sales records by `producto_id` and verifies that each product
    identifier is associated with a consistent product name.

    When the same `producto_id` appears with different product names, the
    inconsistency is recorded as an `inconsistent_product_name` warning
    without invalidating the affected sales records.

    Duplicate product names are removed from the warning details while
    preserving their original encounter order.

    Args:
        df_valid_rows: DataFrame containing sales records that passed all
            critical validation rules.

    Returns:
        A dictionary containing:

        - `warnings`: List of detected non-critical product-name
          inconsistencies.
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

    Verifies that the DataFrame contains rows and includes every column listed
    in `REQUIRED_COLUMNS`.

    The function then normalizes the sales records and coordinates the
    independent validation helpers for empty values, prices, quantities, and
    dates.

    Rows containing one or more critical validation errors are separated from
    valid records. Duplicate invalid indexes produced by multiple errors in
    the same row are removed before the final DataFrames are created.

    Numeric fields in valid rows are converted to numeric pandas data types,
    while valid dates are converted to pandas datetime values.

    Non-critical product-name inconsistencies are detected only after invalid
    rows have been excluded.

    Optional columns such as `ciudad` and `metodo_pago` are preserved and
    normalized when present.

    Args:
        df_raw: Raw pandas DataFrame containing sales records as strings.

    Returns:
        A dictionary containing:

        - `df_valid_rows`: Records that passed all critical validation rules.
        - `df_invalid_rows`: Records containing one or more validation errors.
        - `errors`: Flat list containing detailed validation errors.
        - `warnings`: Flat list containing non-critical inconsistencies.
        - `total_rows`: Total number of normalized sales records.
        - `total_valid_rows`: Number of records that passed validation.
        - `total_invalid_rows`: Number of records containing critical errors.

    Raises:
        EmptyDataFrameError: If the input DataFrame contains no rows.
        MissingColumnsError: If one or more required columns are missing.
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
    