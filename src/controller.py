"""Sales report workflow controller module.

This module coordinates the complete sales-report generation workflow.

It connects the file validation, CSV reading, data validation, sales analysis,
report generation, and file management modules. The controller receives the
source CSV path and output directory, processes the sales data, generates all
supported output formats, measures the total execution time, and returns a
structured dictionary containing processing totals, generated file paths, and
execution information.

The generated outputs currently include TXT, JSON, CSV, and XLSX files.

The module acts as the orchestration layer between the application interface
and the specialized backend processing modules.
"""


from src import validator, csv_reader, analyzer, reporter, file_manager
import time
from typing import Dict, Any


def generate_sales_report(input_file_path: str, output_folder: str) -> Dict[str, Any]:
    """Execute the complete sales-report generation workflow.

    Coordinates the specialized backend modules to validate the source CSV
    file, read its contents, normalize and validate sales records, analyze
    valid data, generate the human-readable report, and save all supported
    output files.

    A shared timestamp-based filename is generated and reused for all report
    formats created during the same execution.

    The function generates:

    - A human-readable TXT sales report.
    - A JSON file containing the complete structured analysis.
    - Independent CSV files containing analysis summaries.
    - An XLSX workbook containing sales analysis, rankings, validation errors,
      and validation warnings.

    The total workflow execution time is measured and included in the returned
    result.

    Args:
        input_file_path: Path of the source CSV file to process.
        output_folder: Directory where the generated report files will be
            stored.

    Returns:
        A dictionary containing processing totals, generated file paths, and
        execution information.

        The dictionary contains:

        - `total_rows`: Total number of processed sales records.
        - `total_valid_rows`: Number of records that passed validation.
        - `total_invalid_rows`: Number of records containing validation errors.
        - `report_path_txt`: Path of the generated TXT report.
        - `report_path_json`: Path of the generated JSON analysis file.
        - `reports_path_csv`: Dictionary containing the generated CSV summary
          file paths.
        - `report_path_xlsx`: Path of the generated XLSX workbook.
        - `execution_time`: Formatted string containing the total workflow
          execution time.
    """
    start = time.perf_counter()
    reports = {}
    file_path = validator.validate_csv_file(input_file_path)
    df_raw = csv_reader.read_csv_file(file_path)
    validation_result = validator.validate_dataframe(df_raw)
    analysis_result = analyzer.analyze_sales(validation_result)
    report_text  = reporter.generate_report(
    analysis_result,
    validation_result["errors"],
    validation_result["warnings"],
    file_path
    )
    reports["total_rows"] = analysis_result["total_rows"]
    reports["total_valid_rows"] = analysis_result["total_valid_rows"]
    reports["total_invalid_rows"] = analysis_result["total_invalid_rows"]
    file_name = file_manager.create_report_base_name()
    reports["report_path_txt"] = file_manager.save_report(report_text , output_folder, file_name)
    reports["report_path_json"] = file_manager.save_analysis_json(analysis_result, output_folder, file_name)
    reports["reports_path_csv"] = file_manager.save_analysis_result_csv_files(analysis_result, output_folder, file_name)
    reports["report_path_xlsx"] = file_manager.save_report_xlsx(analysis_result, validation_result["errors"], validation_result["warnings"], output_folder, file_name)
    end = time.perf_counter()
    total_time = end - start
    reports["execution_time"] = f"Execution time: {total_time:.4f} seconds"
    return reports