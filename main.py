"""Main application module for the Sales Report project.

This module acts as the console entry point for the application.

It defines the source CSV file and output directory, delegates the complete
sales-report generation workflow to the controller module, and displays the 
paths of the generated output files.

The module also handles application-specific errors and unexpected exceptions 
raised during execution.
"""


from src import controller
from src.errors import AppError


def main() -> None:
    """Execute the Sales Report application workflow.

    Defines the source CSV file and output directory and delegates the complete
    processing workflow to `controller.generated_sales_report()`.

    The controller is reponsible for validationg and reading the source data,
    analyzing valid sales records, generating the report, and saving the
    resulting output files.

    The returned report paths are displayed in the console. Nested dictionaries, 
    such as collections of generated CSV file, are iterated so that each
    individual report name and path is displayed.

    Application-specific exceptions derived from `AppError` are caught and
    displayed as readable error messages. Unexpected exceptions are also caught
    and printed to prevent an unhandled application termination.

    Returns:
        None.
    """
    try:
        input_file_path = "data/sales.csv"
        output_folder = "reports"
        reports = controller.generate_sales_report(input_file_path, output_folder)

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