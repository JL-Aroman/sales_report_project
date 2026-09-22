"""Main application module for the Sales Report project.

This module acts as the console entry point for the application.

It defines the source CSV file and output directory, delegates the complete
sales-report generation workflow to the controller module, and displays the
generated output information in the console.

The controller returns both generated-output information and the complete
structured sales-analysis result. The console entry point uses the generated
report information and intentionally ignores the structured analysis result,
which is intended for other application components such as the graphical
dashboard.

The module also handles application-specific errors and unexpected exceptions
raised during execution.
"""


from src import controller
from src.errors import AppError


def main() -> None:
    """Execute the Sales Report console workflow.

    Defines the source CSV file and output directory and delegates the complete
    processing workflow to `controller.generate_sales_report()`.

    The controller is responsible for validating and reading the source data,
    validating sales records, calculating sales-analysis results, generating
    the supported reports and charts, and saving the resulting output files.

    The controller returns two dictionaries: the generated-output information
    and the complete structured sales-analysis result. This console entry point
    uses only the generated-output dictionary and intentionally ignores the
    structured analysis result.

    Generated-output information is displayed in the console. Nested
    dictionaries, such as collections of generated CSV or chart paths, are
    iterated so that each individual output name and value is displayed.

    Application-specific exceptions derived from `AppError` are caught and
    displayed as readable error messages. Unexpected exceptions are also caught
    and printed to prevent an unhandled application termination.

    Returns:
        None.
    """
    try:
        input_file_path = "data/sales.csv"
        output_folder = "reports"
        reports, _ = controller.generate_sales_report(input_file_path, output_folder)

        for item, value in reports.items():
            if isinstance(value, dict):
                for report, path in value.items():
                    print(f"{report}: {path}")
            else:
                print(f"{item}: {value}")
    except AppError as error:
        print(error)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()