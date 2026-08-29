"""Salse report workflow controller module.

This module coordinates the complete sales-report generation workflow.

It connects the validation, CSV reading, sales analysis, report generation,
and file management module. The controller receives the source CSV path
and output directory, processes the sales data, generates all supported
output files, measures the total execution time, and returns a structured 
dictionary containing processing totals, generated file paths, and execution
information.

The module acts as the orchestration layer between the application entry
point and the specialized processing modules.
"""


from src import validator, csv_reader, analyzer, reporter, file_manager
import time
from typing import Dict, Any


def generate_sales_report(input_file_path: str, output_folder: str) -> Dict[str, Any]:
    """Execute the complete sales report generation workflow.

    Coordinates the application modules to validate and read the source CSV
    file, validate and normalize its records, analyze valid sales data,
    generate the plain-text report, and save all supported output files.

    A shared dynamic base filename is generated for the output files. The
    function saves the plain-text report, the complete analysis result as 
    JSON, and the available analysis summaries as independent CSV files.

    The total execution time is measured and included in the returned result.

    Args:
        input_file_path: Path of the source CSV file to process.
        output_folder: Directory where the generated report files will 
            be stored.

    Returns:
        A dictionary containing the following results:

        - `total_rows`: Total number of processed sales records.
        - `total_invalid_rows`: Number of records that passed validation.
        - `total invalid_rows`: Number of records containing validation errors.
        - `report_path_txt`: Path of the generated plain-text report.
        - `report_path_json`: Path of the generated JSON analysis file.
        - `reports_path_csv`: Dictionary containing the paths of the generated
           CSV analysis summary files.
        - `execution_tiem`: Formatted string containing the total workflow execution time.
    """
    start = time.perf_counter()
    reports = {}
    file_path = validator.validate_csv_file(input_file_path)
    df_raw = csv_reader.read_csv_file(file_path)
    validation_result = validator.validate_dataframe(df_raw)
    analysis_result = analyzer.analyze_sales(validation_result)
    report = reporter.generate_report(
    analysis_result,
    validation_result["errors"],
    validation_result["warnings"],
    file_path
    )
    reports["total_rows"] = analysis_result["total_rows"]
    reports["total_valid_rows"] = analysis_result ["total_valid_rows"]
    reports["total_invalid_rows"] = analysis_result["total_invalid_rows"]
    file_name = file_manager.create_report_base_name()
    reports["report_path_txt"] = file_manager.save_report(report, output_folder, file_name)
    reports["report_path_json"] = file_manager.save_analysis_json(analysis_result, output_folder, file_name)
    reports["reports_path_csv"] = file_manager.save_analysis_result_csv_files(analysis_result, output_folder, file_name)
    end = time.perf_counter()
    total_time = end - start
    reports["execution_time"] = f"Execution time: {total_time:.4f} seconds"
    return reports