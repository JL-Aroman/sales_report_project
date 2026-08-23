"""Report file management module.

This module handles the storage of generated sales reports in the file system.

It creates the destination directory when necessary, generates unique
report filenames using the current date and time, writes report content
using UTF-8 encoding, and converts file-system failures into
application-specific exceptions.
"""
from pathlib import Path
from datetime import datetime
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
