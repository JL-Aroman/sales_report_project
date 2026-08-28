"""Report file management module.

This module handles the storage of generated sales reports and structure 
analysis results in the file system.

It creates destination directories when necessary, generates a shared
dynamic base filename using the current date and time, saves plain-text
reports, exports complete analysis results as JSON, and saves aggregated 
analysis summaries as independent CSV files.

Text and JSON files are written usin UTF-8 encoding, shile CSV summaries
are generated from pandas DataFrames.
"""
from pathlib import Path
from datetime import datetime
import pandas as pd
import json

from typing import Dict, Any

from src.errors import ReportSaveError


def save_report(
        report_text: str,
        output_folder: str | Path,
        file_name: str
) -> Path:
    """Save a generated sales report to the file system.

    Creates the output directory and any missing parent directories before
    writing the report content to a text file.

    The function receives a previously generated base filename and adds the 
    `.txt` extension before saving the report using UTF-8 encoding.

    Args:
        report_text: Complete report content to write.
        output_folder: Directory where the report file will be stored.
        file_name: Base filename to use without the file extension.

    Returns: 
        The Path object pointing to the saved report file.

    Raises:
        ReportSaveError: If the output directory cannot be created or the 
            report file cannot be written.
    """
    output_filename = f"{file_name}.txt"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        with open(path, "w", encoding="utf-8") as file:
            file.write(report_text)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def create_report_base_name() -> str:
    """Generate a dynamic base filename for report output files.

    Uses the current local date and time to create a timestamp containing
    the year, month, day, hour, minute, second, and milliseconds.

    The timestamp is combined with the `sales_report` prefix to create a
    shared base filename that can be reused by different output formats.

    Returns:
        A base filename formatted as
        `sales_report_YYYY-MM-DD_HH-MM-SS-fff`
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    file_name = f"sales_report_{timestamp}"
    return file_name

def save_analysis_json(
        analysis_result: Dict[str, Any], 
        output_folder: str | Path, 
        file_name: str
) -> Path:
    """Save sales analysis result as a JSON file.

    Creates a copy of the analysis result and converts pandas DataFrame
    summaries into lists of dictionaries so that the data can be serialized 
    to JSON.

    The product and category summaries are always converted. Optional city
    and payment method summaries are also converted when they are available.

    The function receives a previously generated base filename and adds the
    `.json` extension before saving the data using UTF-8 encoding.

    Args:
        analysis_result: Dictionary containing the complete sales analysis
            results.
        output_folder: Directory where the JSON file will be stored.
        file_name: Base filename to use without the file extension.

    Returns:
        The Path object pointing to the saved JSON analysis file.

    Raises:
        ReportSaveError: If the output directory cannot be created or the 
            JSON file cannot be written.
    """
    analysis_json = analysis_result.copy()
    analysis_json["product_summary"] = analysis_json["product_summary"].to_dict(orient="records")
    analysis_json["category_summary"] = analysis_json["category_summary"].to_dict(orient="records")
    if "city_summary" in analysis_json.keys() and analysis_json["city_summary"] is not None:
        analysis_json["city_summary"] = analysis_json["city_summary"].to_dict(orient="records")
    if "payment_method_summary" in analysis_json.keys() and analysis_json["payment_method_summary"] is not None:
        analysis_json["payment_method_summary"] = analysis_json["payment_method_summary"].to_dict(orient="records")
    output_filename = f"{file_name}.json"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        with open(path, "w", encoding="utf-8") as file:
            json.dump(analysis_json, file, indent=4, ensure_ascii=False)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def save_analysis_result_csv_files(
        analysis_result: Dict[str, Any], 
        output_folder: str | Path, 
        file_name: str
) -> Dict[str, Any]:
    """Save analysisi summary DataFrames as independent CSV files.

    Creates individual CSV files for the product and category summaries.
    Optional city and payment method summaries are also saved when they are
    available in the analysis result.

    Each CSV file uses ghe shared report base filename followed by a descriptive
    suffix identifying the type o summary.

    The function delegates the creation of each CSV file an its path to 
    `create_save_analysis_result_csv_files_and_path()`

    Args:
        analysis_result: Dictionary containing the complete sales analysis
            results and summary DAtaFrames.
        output_folder: Directory where the CSV files will be stored.
        file_name: Shared base filename to use without a file extension.

    Returns:
        A dictionary containing the generated CSV file paths. The dictionary
        always contains `product_summary` and `category_summary`, and may also
        contain `city_summary` and `payment_method_summary` when those analyses 
        are available.
    """
    analysis_csv = analysis_result.copy()
    reports = {}
    reports["product_summary"] = create_save_analysis_result_csv_files_and_path(analysis_csv["product_summary"], output_folder, file_name, "products")
    reports["category_summary"] = create_save_analysis_result_csv_files_and_path(analysis_csv["category_summary"], output_folder, file_name, "categories")
    if "city_summary" in analysis_csv and analysis_csv["city_summary"] is not None:
        reports["city_summary"] = create_save_analysis_result_csv_files_and_path(analysis_csv["city_summary"], output_folder, file_name, "cities")
    if "payment_method_summary" in analysis_csv and analysis_csv["payment_method_summary"] is not None:
        reports["payment_method_summary"] = create_save_analysis_result_csv_files_and_path(analysis_csv["payment_method_summary"], output_folder, file_name, "payment_methods")
    return reports

def create_save_analysis_result_csv_files_and_path(
        df: pd.DataFrame, 
        folder: str | Path, 
        file_name: str, 
        prefix: str
) -> Path:
    """Create and save a single analysis summary CSV file.

    Builds a CSV filename using the shared report base filename and a descriptive
    prefix, creates the destination directory when necessary, and saves the
    provided DataFrame without its pandas index.

    Args:
        df: DataFrame containing the analysis summary to save.
        folder: Directory where the CSV file will be stored.
        file_name: Shared base filename to use without a file extension.
        prefix: Descriptive suffix used to identify the CSV summary.

    Returns:
        The Path object pointing to the saved CSV file.
    """
    output_filename = f"{file_name}_{prefix}.csv"
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / output_filename
    df.to_csv(path, index=False)
    return path