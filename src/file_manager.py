"""Report file management module.

This module handles the storage of generated sales reports in the file
system.

It creates the destination directory when necessary, writes report content
using UTF-8 encoding, and converts file-system failures into application-specific
exceptions.

"""
from pathlib import Path

from src.errors import ReportSaveError


def save_report(
        report_text: str,
        output_folder: str | Path,
        output_filename: str
) -> Path:
    """Save a generated sales report to the file system.

    Creates the output directory and any missing parent directories before
    writing the report content to the requested file. Existing files with the 
    same name are overwritten.

    The report is written using UTF-8 encoding.

    Args:
        report_text: Complete report content to write.
        output_folder: Directory where the report file will be stored.
        output_filename: Name of the output file, including its extension.
    
    Returns:
        The path object pointing to the saved report file.

    Raises:
        ReportSaveError: If the output directory cannot be created or the 
            report file cannot be written.
    """
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = Path(f"{folder}/{output_filename}")
        with open(path, "w", encoding="utf-8") as file:
            file.write(report_text)
    except OSError as error:
        raise ReportSaveError() from error
    return path