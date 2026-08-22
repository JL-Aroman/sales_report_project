"""Main application module for the Sales Report project.

This module acts as the entry point for the application and coordinates the
complete sales-reporting workflow.

It validates the source CSV file, reads its contents into a pandas DataFrame,
validates and normalizes the sales records, performs the sales analysis,
generates the plain-text report, and saves the resulting file.

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
    6. Generates the complete plain-text report.
    7. Saves the report in the destination folder.
    8. Calculates and displays the total execution time.

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
        saved_report_path = file_manager.save_report(report, "reports", "first_report.txt")

        end = time.perf_counter()
        total_time = end - start

        print(f"Report saved at: {saved_report_path}")

        print(f"Execution time: {total_time:.4f} seconds")
    except AppError as error:
        print(error)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()