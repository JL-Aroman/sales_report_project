"""Report file management module.

This module handles the storage of generated sales report in the file system.

It creates the destination directory when necessary, generates unique
report filenames using the current date and time, writes report content
using UTF-8 encoding, and converts file-system failures into
application-specific exceptions.
"""
from pathlib import Path
from datetime import datetime

from src.errors import ReportSaveError


def save_report(
        report_text: str,
        output_folder: str | Path,
) -> Path:
    """Save a generated sales report to the file system.

    Creates the output directory and any missing parent directories before
    writing the report content

    The output file name is generated automatically using the base name
    `sales_report` followed by a timestamp containing the current date,
    time, and milliseconds.

    The report is written usings UTF-8 encoding.

    Args:
        report_text: Complete report content to write.
        output_folder: Directory where the report file will be stored.
    
    Returns:
        The path object pointing to the saved report file.

    Raises:
        ReportSaveError: If the output directory cannot be created or the 
            report file cannot be written.
    """
    file_name = "sales_report"
    timestamp = get_dynamic_name()
    output_filename = f"{file_name}_{timestamp}.txt"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = Path(f"{folder}/{output_filename}")
        with open(path, "w", encoding="utf-8") as file:
            file.write(report_text)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def get_dynamic_name() -> str:
    """Generate a timestamp string for dynamic report filenames.

    Uses the current local date and time to create a timestamp containing
    the year, month, day, hour, minute, second, and milliseconds.

    Returns:
        A timestamp string formmated as `YYYY-MM-DD_HH-MM-SS-FFF`.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    return timestamp