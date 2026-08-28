"""Main application module for the Sales Report project.

This module acts as the entry point for the application and coordinates the
complete sales-reporting workflow.

It validates the source CSV file, reads its contents into a pandas DataFrame,
validates and normalizes the sales records, performs the sales analysis,
generates the plain-text report, creates a shared dynamic base filename,
and saves the text report, the complete analysis results as a JSON file,
and the aggregated analysis summaries as independent CSV files.

The module also measures the total execution time and handles both expected
application-specific errors and unexpected exception.
"""

import time

from src import validator, csv_reader, analyzer, reporter, file_manager
from src.errors import AppError


def main() -> None:
    """Execute the complete sales report generation workflow.

    Coordinates the application modules in the following order:

    1. Starts the execution timer.
    2. Validates the source CSV file path.
    3. Reads the CSV file into a raw pandas DataFrame.
    4. Normalizes and validates the sales records.
    5. Analyzes the valid sales data.
    6. Generates the complete plain-text report-
    7. Generates a shared dinamic base filename for the output files.
    8. Saves the plain-text report in the destination folder.
    9. Saves the analysis result as a JSON file using the same base filename.
    10. Saves the aggregated analysis summaries as independent CSV files.
    11. Displays the paths of the generated text, JSON, and CSV files.
    12. Calculates and displays the total execution time.

    The text report, JSON analysis file, and CSV analysis summaries share the
    same dynamically generated base filename. CSV files also include a descriptive
    suffix identifying the type of summary.

    Application-specific exception derived from `AppError` are caught and 
    displayed as readable error messages. Unexpected exceptions are also 
    caught and printed to prevent an unhandled application termination.

    Returns:
        None.
    """
    try:
        start = time.perf_counter()

        file_path = validator.validate_csv_file("data/sales.csv")
        df_raw = csv_reader.read_csv_file(file_path)
        validation_result = validator.validate_dataframe(df_raw)
        analysis_result = analyzer.analyze_sales(validation_result)
        report = reporter.generate_report(
            analysis_result,
            validation_result["errors"],
            validation_result["warnings"],
            file_path
        )
        file_name = file_manager.create_report_base_name()
        saved_report_path = file_manager.save_report(report, "reports", file_name)
        saved_report_path_json = file_manager.save_analysis_json(analysis_result, "reports", file_name)
        saved_reports_csv = file_manager.save_analysis_result_csv_files(analysis_result, "reports", file_name)

        end = time.perf_counter()
        total_time = end - start

        print(f"Report saved at: {saved_report_path}")
        print(f"Report saved at: {saved_report_path_json}")
        print("Reports CSV")
        for key, value in saved_reports_csv.items():
            print(f"{key}: {value}")

        print(f"Execution time: {total_time:.4f} seconds")
    except AppError as error:
        print(error)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()