# Sales Report

> **Project Status:** Version 2.0.4 completed - Functional console application. This project has been manually tested with a sample sales CSV file.

Sales Report is a modular Python application for validating sales data, analyzing valid records, generating structured reports, and exporting analysis results in multiple formats.

The project includes a PySide6 graphical interface that allows users to select a source CSV file, choose an output directory, generate reports, inspect generated TXT, JSON, and CSV files, and open the output directory directly from the application.

The application interface and user-facing messages are displayed in Spanish, while the project source code and technical documentation are maintained in English.

---

## Project Architecture (Current State)

The project follows a modular architecture in which each module is responsible for a specific part of the application workflow.

The application separates graphical presentation, workflow orchestration, validation, analysis, report generation, file management, and error handling.

The current application relationship can be represented as:

`Graphical Application Entry Point`

→ `SalesReportWindow`

→ `controller.generate_sales_report()`

→ `validator`

→ `csv_reader`

→ `analyzer`

→ `reporter`

→ `file_manager`

→ TXT / JSON / CSV output files

Generated report files can then be opened from the graphical interface through:

`FileViewerWindow`

The main modules include:

* `controller`: Coordinates the complete sales-report generation workflow.
* `validator`: Validates the source file, normalizes records, validates sales data, and detects warnings.
* `csv_reader`: Reads the validated CSV file into a pandas `DataFrame`.
* `analyzer`: Calculates sales metrics, rankings, and aggregated summaries.
* `reporter`: Generates the structured plain-text sales report.
* `file_manager`: Saves TXT, JSON, and CSV output files.
* `errors`: Defines application-specific exceptions and Spanish user-facing error messages.
* `gui.main_windows`: Provides the main PySide6 graphical interface.
* `gui.file_viewer_window`: Displays generated TXT, JSON, and CSV files in read-only viewer windows.
* Graphical application entry point: Initializes `QApplication`, creates the main window, and starts the Qt event loop.

---

## Installation and Usage

### Requirements

Before running the project, make sure the following tools are installed:

* Python 3.10 or later.
* `pip`, the Python package installer.
* Git, if the project will be cloned from GitHub.
* `PySide6`, used to build and run the graphical desktop interface.

The required Python libraries, including PySide6 and the data-processing dependencies, are listed in:

`requirements.txt`

Install all project dependencies using:

```bash
pip install -r requirements.txt
```

---

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Move into the project directory:

```bash
cd sales_report_project
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

5. Install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Input CSV File

The application processes sales information from a CSV file selected by the user.

The CSV file must contain the following required columns:

```text
producto_id,producto,categoria,precio,cantidad,fecha
```

The expected date format is:

```text
YYYY-MM-DD
```

The application also supports the following optional columns:

* `ciudad`
* `metodo_pago`

These columns are not required for the core validation process.

When present, they are normalized and used to generate additional sales analysis summaries.

### Minimum CSV Example

```csv
producto_id,producto,categoria,precio,cantidad,fecha
P001,Producto A,Categoria A,150.50,2,2026-07-01
P002,Producto B,Categoria B,89.90,5,2026-07-02
```

### CSV Example with Optional Columns

```csv
producto_id,producto,categoria,precio,cantidad,fecha,ciudad,metodo_pago
P001,Producto A,Categoria A,150.50,2,2026-07-01,Guadalajara,Tarjeta
P002,Producto B,Categoria B,89.90,5,2026-07-02,Zapopan,Efectivo
```

---

## Running the Application

The application is launched through its PySide6 graphical application entry point.

When the application starts, the main window allows the user to:

1. Select a source CSV file.
2. Optionally select a custom output directory.
3. Use `reports/` as the default output directory when no custom folder is selected.
4. Start the sales-report generation process.
5. View the current application status.
6. View the paths of generated report files.
7. Open generated TXT, JSON, and CSV files.
8. Open the configured output directory.

---

## Application Workflow

When the user starts report generation, the application performs the following workflow:

1. Verifies that a source CSV file has been selected.
2. Sends the source file path and output directory to `controller.generate_sales_report()`.
3. Starts the execution timer.
4. Validates the source CSV file.
5. Reads the validated file into a pandas `DataFrame`.
6. Normalizes and validates the sales records.
7. Separates valid and invalid rows.
8. Detects validation warnings.
9. Analyzes the valid sales records.
10. Calculates general sales metrics.
11. Generates product and category summaries.
12. Generates Top 5 product rankings.
13. Generates city analysis when `ciudad` is available.
14. Generates payment-method analysis when `metodo_pago` is available.
15. Generates the structured plain-text sales report.
16. Creates a shared dynamic base filename.
17. Saves the plain-text report as a TXT file.
18. Saves the complete structured analysis as a JSON file.
19. Saves product and category summaries as independent CSV files.
20. Saves city and payment-method CSV summaries when those optional analyses are available.
21. Calculates the total execution time.
22. Returns processing results and generated file paths to the graphical interface.
23. Displays the generated file paths in the application.
24. Enables the controls used to inspect the generated reports.

---

## Generated Output Files

Generated report files are stored in the selected output directory.

If no custom directory is selected, the default directory is:

```text
reports/
```

If the destination directory does not exist, the application creates it when necessary.

All files generated during the same execution share a dynamically generated base filename containing the current local date and time.

The base filename follows this format:

```text
sales_report_YYYY-MM-DD_HH-MM-SS-fff
```

For example:

```text
sales_report_2026-08-28_16-30-25-125
```

A normal execution generates:

```text
reports/sales_report_2026-08-28_16-30-25-125.txt
reports/sales_report_2026-08-28_16-30-25-125.json
reports/sales_report_2026-08-28_16-30-25-125_products.csv
reports/sales_report_2026-08-28_16-30-25-125_categories.csv
```

When optional analysis data is available, the application may also generate:

```text
reports/sales_report_2026-08-28_16-30-25-125_cities.csv
reports/sales_report_2026-08-28_16-30-25-125_payment_methods.csv
```

Each execution generates a new dynamic base filename, allowing report files from different executions to be stored independently.

---

## Generated TXT Report

The TXT file contains the human-readable sales report.

Depending on the available data, the report may include:

* General sales summary.
* Total processed rows.
* Valid and invalid row totals.
* Total income.
* Total units sold.
* Best-selling product.
* Highest-income product.
* Highest-income category.
* Highest-income city when available.
* Highest-income payment method when available.
* Top 5 best-selling products.
* Top 5 highest-income products.
* Product summary.
* Category summary.
* City summary when available.
* Payment-method summary when available.
* Validation errors.
* Validation warnings.

The report is saved using UTF-8 encoding.

---

## Generated JSON Analysis

The JSON file contains the structured sales analysis results.

pandas `DataFrame` summaries are converted into JSON-compatible lists of dictionaries before serialization.

The JSON output always contains the product and category analysis results and may also contain city and payment-method analysis when those optional fields are available.

The file is written using UTF-8 encoding and formatted indentation.

---

## Generated CSV Summaries

The application generates independent CSV files for aggregated sales summaries.

The following summaries are always generated:

* Product summary.
* Category summary.

The following summaries are generated when the corresponding optional data is available:

* City summary.
* Payment-method summary.

The physical filenames use the following suffixes:

* `_products.csv`
* `_categories.csv`
* `_cities.csv`
* `_payment_methods.csv`

The CSV-path dictionary returned by the file-management workflow uses the following Spanish keys:

* `resumen_producto`
* `resumen_categoria`
* `ciudad_resumen`
* `metodo_de_pago_resumen`

The city and payment-method entries are optional.

---

## Graphical Report Viewing

After a successful report-generation process, the graphical interface displays the generated output paths.

The user can:

* Open the generated TXT report.
* Open the generated JSON analysis file.
* Select a generated CSV summary from a combo box.
* Open the selected CSV summary.
* Open the output directory using the operating system file manager.

TXT, JSON, and CSV files are displayed through an independent read-only `FileViewerWindow`.

The viewer reads the selected report using UTF-8 encoding and displays its contents without modifying the original file.

---

## Application Status and Errors

The graphical interface provides status messages during the application workflow.

The status area informs the user about events such as:

* CSV file selection.
* Output-folder selection.
* Start of report generation.
* Missing source-file selection.
* Successful report generation.
* Processing errors.

Application-specific exceptions inherit from:

`AppError`

Expected application errors use Spanish default messages because they are intended to be displayed directly to the user.

When an application-specific or unexpected error occurs during report generation, the graphical interface updates the status and displays the error through a critical message box.

The graphical application remains open so that the user can correct the problem and try again.

---

## Output Directory Access

After successful report generation, the graphical interface enables the option:

`Abrir carpeta de salida`

The application opens the configured output directory using the platform-specific operating-system mechanism:

* Windows: `os.startfile()`
* macOS: `open`
* Linux and compatible systems: `xdg-open`

This allows generated report files to be accessed directly from the desktop application.

---

### Custom Exceptions Module

The custom exceptions module defines the application-specific errors used throughout the Sales Report project.

Its purpose is to make expected application failures easier to identify, handle, propagate, and present consistently across the backend and graphical interface.

All custom exceptions inherit from `AppError`, which acts as the common base class for application-specific errors.

The default exception messages are written in Spanish because they are intended to be displayed directly to the user through the graphical interface.

The module currently handles errors related to:

* Empty, missing, or invalid file paths.
* Unsupported file extensions.
* Empty or unreadable CSV files.
* Missing or invalid CSV headers.
* Missing required columns.
* Invalid CSV structures.
* Empty or unusable DataFrames.
* Data validation failures.
* Absence of valid rows for analysis.
* Report generation failures.
* Report saving failures.

#### Base Exception

`AppError` is the base class for all application-specific exceptions.

It stores the error message received during initialization and provides that message through its string representation.

This allows the application to handle all expected project-specific errors through a common exception type while preserving specialized subclasses for different failure conditions.

#### User-Facing Error Messages

Each specialized exception provides a default error message in Spanish.

These messages are designed to be presented directly to the user when an expected application error occurs.

For example:

`La ruta del archivo está vacía.`

`La ruta del archivo no existe.`

`La extensión del archivo no es compatible.`

`El archivo no se pudo leer correctamente.`

`No hay filas válidas disponibles para el análisis.`

`No se pudo guardar el archivo del reporte.`

A custom message may also be provided when creating an exception, replacing its default message.

#### Exception Hierarchy

* `AppError`: Base class for all application-specific exceptions.

* `EmptyPathError`: Raised when the provided file path is empty.

* `FileNotFoundAppError`: Raised when the provided file path does not exist.

* `InvalidFilePathError`: Raised when the path does not point to a valid file.

* `InvalidFileExtensionError`: Raised when the file extension is not supported.

* `EmptyFileError`: Raised when the CSV file exists but contains no usable content.

* `FileReadError`: Raised when the CSV file cannot be read correctly.

* `MissingColumnsError`: Raised when the CSV file does not contain all required columns.

* `EmptyHeadersError`: Raised when the CSV file has no valid headers.

* `InvalidCSVStructureError`: Raised when the CSV structure is invalid.

* `EmptyDataFrameError`: Raised when the DataFrame contains no rows or usable data.

* `DataValidationError`: Raised when the DataFrame validation process fails.

* `NoValidRowsError`: Raised when no valid rows are available for sales analysis.

* `ReportGenerationError`: Raised when the plain-text report cannot be generated.

* `ReportSaveError`: Raised when a generated report file cannot be saved.

#### Error Propagation

Specialized backend modules raise these exceptions when an expected application failure occurs.

The exceptions can propagate through the controller until they reach the graphical interface.

Because all custom exceptions inherit from `AppError`, the GUI can handle expected application errors through a common exception block.

#### Graphical Interface Integration

The main graphical interface catches application-specific exceptions using:

```python
except AppError as error:
```

When an `AppError` occurs during report generation, the GUI can present the Spanish error message directly to the user.

This separates technical exception handling from user-facing feedback while maintaining a consistent error hierarchy across the application.

#### Custom Error Messages

Each specialized exception accepts an optional `message` argument.

When no custom message is provided, the exception uses its predefined Spanish message.

A custom message can be supplied when additional context is required without changing the exception type.

#### Responsibilities

This module is responsible for:

* Defining the common `AppError` base exception.
* Defining specialized exceptions for expected application failures.
* Providing default user-facing messages in Spanish.
* Supporting consistent exception handling across the project.
* Allowing custom messages when additional error context is required.

This module is not responsible for:

* Detecting every error condition directly.
* Displaying graphical error dialogs.
* Logging errors.
* Recovering from failed operations.

Those responsibilities belong to the modules that raise, catch, or present the corresponding exceptions.

---

### File Validation and Data Normalization Module

The file validation and data normalization module prepares the input CSV file and its raw sales data for the processing workflow.

It validates the input file path, normalizes string values inside pandas `DataFrame` objects, applies independent validation rules, separates valid and invalid records and collects errors and warnings.

Each validation rule is implemented in a separate helper function. This modular structure makes the validation process easier to maintain, test, and extend.

The moudle also supports optional fields, such as `ciudad` and `metodo_pago`, wich are preserved and normalized when present without being required for the core validation workflow.

- `validate_csv_file()`
- `normalize_dataframe()`
- `validated_empty_values()`
- `validated_price()`
- `validated_amount()`
- `validated_date()`
- `detect_warnings()`
- `validate_dataframe()`

#### File Validation Process

The `validate_csv_file()` function performs the following checks:

1. Verifies that the provided path is not `None` or empty.
2. Converts the string path into a `Path` object.
3. Confirms that the path exists in the file system.
4. Ensures that the path points to a file rather than a directory.
5. Validates that the file has a `.csv` extension.
6. Ensures that the file is not empty.
7. Confirms that the file can be read.
8. Returns the validated `Path` object.

#### Data Normalization Process

The `normalize_dataframe()` function creates a copy of the raw `DataFrame` and applies the following normalization rules.

1. Removes all whitespace form `producto_id`.
2. Converts `producto_id` values to uppercase.
3. Remove leading and trailing whitspace form `producto`.
4. Replaces repeatd whitespace inside `producto` with a single space.
5. Remove leading and trailing whitespace form `categoria`.
6. Replaces repeated withespaces inside `categoria` with a single space.
7. Remove all withespaces form `precio`, `cantidad`, and, `fecha`
8. If the optional `ciudad` column is present, removes leading and trailing whitespaces and replaces repeated internal whitespaces with a single space.
9. If the optional `metodo_pago` column is present, removes leading and trailing whitespaces and replaces repeated internal whitespaces with a single space.
10. Returns a new normalized `DataFrame` without modifying the original one.

#### Independent Validation Functions

The validation rules are divided into independent helper functions:

- `validated_empty_values()`: Detects empty values in required fields.
- `validated_price()`: Verifies that prices are numeric and greater than zero.
- `validated_amount()`: Verifies that quantities are whole numbers greater than zero.
- `validated_date()`: Verifies the date format and confirms that each date exists in the calendar.
- `detect_warnings()`: Detects non-critical inconsistencies in valid sales records.

Each critical validation function returns:

- `invalid_indexes`: Row indexes containing validation errors.
- `errors`: Detailed information about the detected errors.

The `detect_warnings()` function returns:

- `warnings`: Non-critical inconsistencies that do not invalidate sales records.

#### DataFrame Validation Process

The `validate_dataframe()` function coordinates the complete validation workflow.

It performs the following operations:

1. Verifies that the input `DataFrame` is not empty.
2. Confirms that all required columns are present.
3. Normalizes the raw sales data.
4. Preserves supported optional columns when present.
5. Executes the empty-value validation.
6. Executes the price validation.
7. Executes the quantity validation.
8. Executes the date validation.
9. Collects all detected errors and invalid row indexes.
10. Removes duplicate invalid indexes.
11. Separates valid and invalid rows.
12. Converts valid prices and quantities into numeric values.
13. Converts valid dates into pandas datetime values.
14. Detects warnings in valid sales records.
15. Returns the complete validation result.

#### Required Columns

The validation process expects the following columns:

- `producto_id`
- `producto`
- `categoria`
- `precio`
- `cantidad`
- `fecha`

#### Optional Columns

The current version supports the following optional columns:

- `ciudad`
- `metodo_pago`

#### Validation Result

The `validate_dataframe()` function returns a dictionary containing:

- `df_valid_rows`: A `DataFrame` containing records that passed all critical validation rules.
- `df_invalid_rows`: A `DataFrame` containing records with one or more validation errors.
- `errors`: A flat list containing detailed validation errors.
- `warnings`: A flat list containing non-critical data inconsistencies.
- `total_rows`: The total number of normalized records.
- `total_valid_rows`: The number of records that passed validation.
- `total_invalid_rows`: The number of records containing errors.

Optional columns present in the original CSV file are preserved in the resulting valid and invalid `DataFrame` objects.

#### Input and Output

##### `validate_csv_file()`

- **Input:** A string containing the path of the CSV file.
- **Output:** A validated `Path` object ready for the CSV reading process.

##### `normalize_dataframe()`

- **Input:** A raw pandas `DataFrame` containing sales data as strings.
- **Output:** A new `DataFrame` containing normalized string values while preserving supported optional columns.

##### Validation Helper Functions

- **Input:** A normalized pandas `DataFrame`.
- **Output:** A dictionary containing validation errors and invalid row indexes.

##### `detect_warnings()`

- **Input:** A pandas `DataFrame` containing valid sales records.
- **Output:** A dictionary containing non-critical validation warnings.

##### `validate_dataframe()`

- **Input:** A raw pandas `DataFrame` containing sales records as strings.
- **Output:** A dictionary containing valid rows, invalid rows, errors, warnings, and validation totals.

#### Related Exceptions

The module may raise the following custom exceptions:

- `EmptyPathError`
- `FileNotFoundAppError`
- `InvalidFilePathError`
- `InvalidFileExtensionError`
- `EmptyFileError`
- `FileReadError`
- `EmptyDataFrameError`
- `MissingColumnsError`

---

### CSV Reading Module

The CSV reading module converts a previously validated CSV file into a pandas `DataFrame`.

Its main function, `read_csv_file()`, receives a `Path` object, reads the CSV file using pandas, and returns the raw data in a tabular structure ready for validation and processing.

All columns are initially read as strings, and empty cells are preserved as empty strings. This prevents automatic data type conversion and allows the validation module to inspect the original values consistently.

#### Reading Process

1. Receives a previously validated `Path` object.
2. Reads the CSV file using `pandas.read_csv()`.
3. Loads all column values as strings.
4. Preserves empty cells as empty strings instead of converting them into `NaN` values.
5. Converts the file contents into a pandas `DataFrame`.
6. Returns the raw `DataFrame` for the next stage of the application workflow.
7. Converts file-reading, empty-data, and CSV-parsing failures into a custom `FileReadError`.

#### Input and Output

- **Input:** A validated `Path` object pointing to the CSV file.
- **Output:** A pandas `DataFrame` containing the raw CSV data as strings, with empty cells preserved for validation.

#### Related Exceptions

- `FileReadError`

---

### Sales Analysis Module

The sales analysis module processes previously validated sales records and calculates the main metrics required for report generation.

Each analysis operation is implemented in a separate helper function. This modular structure makes the analysis workflow easier to maintain, test, and extend without modifying the entire module.

The module currently provides the following functions:

- `create_income_column()`
- `get_total_income()`
- `get_total_units_sold()`
- `get_product_summary()`
- `get_category_summary()`
- `get_records_with_max_value()`
- `analyze_sales()`
- `get_city_summary()`
- `get_top_5_best_selling_products()`
- `get_top_5_highest_income_products()`
- `get_payment_method_summary()`

#### Income Calculation

The `create_income_column()` function calculates the income generated by each valid sales record.

It multiplies `precio` by `cantidad` and stores the result in a new `ingreso_fila` column.

#### General Sales Metrics

The module calculates the following general metrics:

- `get_total_income()`: Adds all values from the `ingreso_fila` column.
- `get_total_units_sold()`: Adds all values from the `cantidad` column.

These functions return standard Python numeric values ready to be included in the final analysis result.

#### Product Summary

The `get_product_summary()` function groups valid sales records by `producto_id`.

For each product, it preserves the first associated product name and category and calculates the total units sold and total income.

The product summary contains the following fields:

- `producto_id`
- `producto`
- `categoria`
- `unidades_vendidas`
- `ingreso_total`

#### Category Summary

The `get_category_summary()` function groups valid sales records by `categoria` and calculates the total units sold and total income for each category.

The category summary contains the following fields:

- `categoria`
- `unidades_vendidas`
- `ingreso_total`

#### City Summary

The `get_city_summary()` function groups valid sales records by `ciudad` when the optional city column is available.

It excludes empty city values and calculates the total units sold and total income for each city.

The city summary is sorted from highest to lowest total income.

The city summary contains following fields:

- `ciudad`
- `unidades_vendidas`
- `ingreso_total`

City analysis is optional and is only performed when the `ciudad` column is present.

#### Payment Method Summary

The `get_payment_method_summary()` function groups valid sales records by `metodo_pago` when the optional payment method column is available.

It excludes empty payment method values and calculates the total units sold and total income for each payment method.

The payment method summary contains the following fields:

- `metodo_pago`
- `unidades_vendidas`
- `ingreso_total`

Payment method analysis is optional and is only performed when the `metodo_pago` column is present.

#### Maximum-Value Records

The `get_records_with_max_value()` function identifies all records containing the maximum value in a specified column.

This reusable function is used to determine:

- The product or products with the highest number of units sold.
- The product or products with the highest total income.
- The category or categories with the highest total income.
- The city or cities with the highest total income when city data is available.
- The payment method or payment methods with the highest total income when payment method data is available.

If multiple records share the maximum value, all tied records are included in the result.

#### Top Product Rankings

The also generates Top 5 products rankings:

- `get_top_5_best_selling_products()`: Returns up to five products with the highest number of units sold. Total income is used as a secondary sorting criterion.
- `get_top_5_highest_income_products()`: Returns up to five products with th highest total income.

Both functions return the selected products as lists of dictionaries.

#### Sales Analysis Process

The `analyze_sales()` function coordinates the complete analysis workflow.

It performs the following operations:

1. Extracts the valid sales rows and validation totals.
2. Creates a copy of the valid sales `DataFrame`.
3. Verifies that at least one valid row is available.
4. Creates the `ingreso_fila` column.
5. Calculates the total income generated by valid sales.
6. Calculates the total number of units sold.
7. Creates the product summary.
8. Creates the category summary.
9. Identifies the best-selling product or products.
10. Identifies the product or products with the highest income.
11. Identifies the category or categories with the highest income.
12. Creates the Top 5 best-selling products ranking.
13. Cretaes the Top 5 highest-income products ranking.
14. If the optional `ciudad` column is present, creates the city summary.
15. Identifies the city or cities with th highest income then city data is available.
16. If the optional `metodo_pago` column is present, creates the payment method summary.
17. Identifies the payment method or payment methods with the highest income when payment method data is available.
18. Returns the complete analysis result.

#### Analysis Result

The `analyze_sales()` function returns a dictionary containing:

- `total_rows`: The total number of processed sales records.
- `total_valid_rows`: The number of records that passed validation.
- `total_invalid_rows`: The number of records containing validation errors.
- `total_income`: The total income generated by valid sales.
- `total_units_sold`: The total number of units sold.
- `product_summary`: A pandas `DataFrame` containing aggregated results for each product.
- `category_summary`: A pandas `DataFrame` containing aggregated results for each category.
- `best_selling_product`: A list containing the product or products with the highest number of units sold.
- `highest_income_product`: A list containing the product or products with the highest total income.
- `highest_income_category`: A list containing the category or categories with the highest total income.
- `top_5_best_selling_products`: A list containing up to five products with the highest number of units sold.
- `top_5_highest_income_products`: A list containing up to five products with the highest total income.

When the optional `ciudad` column is present, the analysis result also contains:

- `city_summary`: A pandas `DataFrame` containing aggregated results for each city.
- `highest_income_city`: A list containing the city or cities with the highest total income.

When the optional `metodo_pago` column is present, the analysis result also contains:

- `payment_method_summary`: A pandas `DataFrame` containing aggregated results for each payment method.
- `highest_income_payment_method`: A list containing the payment method or payment methods with the highes total income.

#### Input and Output

##### Analysis Helper Functions

- **Input:** A pandas `DataFrame` containing valid sales records or aggregated sales information and, when required, the name of the column to evaluate.
- **Output:** A calculated value, and aggregated `DataFrame`, a list of records containing a maximum value, or a Top 5 product ranking.

##### `analyze_sales()`

- **Input:** A dictionary containing valid sales rows and validation totals.
- **Output:** A dictionary containing general sales metrics, product summries, category summaries, Top 5 product rankings, highest-performing records, and optional ciy and payment method analysis result.

#### Related Exceptions

- `NoValidRowsError`

---

### Sales Report Generation Module

The sales report generation module converts sales analysis results, validation errors, and warnings into a structured plain-text report.

Each report section is generated by an independent helper function. This modular structure makes the reporting workflow easier to maintain, test, modify, and extend.

The report can also include Top 5 product rankings and optional city-based and payment-method-based information when these data are available.

The module currently provides the following functions:

- `get_general_summary()`
- `get_best_selling_product()`
- `get_highest_income_product()`
- `get_highest_income_category()`
- `get_product_summary()`
- `get_category_summary()`
- `get_errors()`
- `get_warnings()`
- `generate_report()`
- `get_highest_income_city()`
- `get_top_5_best_selling_products()`
- `get_top_5_highest_income_products()`
- `get_city_summary()`
- `get_highest_income_payment_method()`
- `get_payment_method_summary()`

#### General Summary

The `get_general_summary()` function generates the main sales metrics section.

It includes:

- Total processed rows.
- Total valid rows.
- Total invalid rows.
- Total income.
- Total units sold.

The total income is formatted with thousands separators and two decimal places.

#### Best-Selling Product

The `get_best_selling_product()` function formats the product or products with the highest number of units sold.

For each product, the section includes:

- `producto_id`
- `producto`
- `unidades_vendidas`

If multiple products share the highest number of units sold, all tied products are included.

#### Highest-Income Product

The `get_highest_income_product()` function formats the product or products that generated the highest total income.

For each product, the section includes:

- `producto_id`
- `producto`
- `ingreso_total`

If multiple products share the highest income, all tied products are included.

#### Highest-Income Category

The `get_highest_income_category()` function formats the category or categories that generated the highest total income.

For each category, the section includes:

- `categoria`
- `ingreso_total`

If multiple categories share the highest income, all tied categories are included.

#### Highest-Income City

The `get_highest_income_city()` function fromats the city or cities that generated the highest total income.

For each city, the section includes:

- `ciudad`
- `ingreso_total`
- `unidades_vendidas`

If multiple citites share the highest income, all tied cities, are included. 

This section is only generated when city analysis is available.

#### Highest-Income Payment Method

The `get_highest_income_payment_method()` function formats the payment method or payment methods that generated the highest total income.

For each payment method, the section includes:

- `metodo_pago`
- `ingreso_total`
- `unidades_vendidas`

If multiple payment methods share the highest income, all tied payment methods are included.

This section is only generated when payment method analysis is available.

#### Top Product Rankings

The module generates two Top 5 product ranking sections:

- `get_top_5_best_selling_products()`: Formats up to five products with the higest number of units sold.
- `get_top_5_highest_income_products()`: Formats up to five products with the highest total income.

Each ranking includes the product position, identifier, name, units sold, and total income.

#### Product, Category, City and Payment Method Summaries

The module converts the aggregated pandas `DataFrame` objects into plain-text tables.

- `get_product_summary()`: Generates the complete product summary table.
- `get_category_summary()`: Generates the complete category summary table.
- `get_city_summary()`: Generates the complete city summary table when city data is available.
- `get_payment_method_summary()`: Generates the complete payment method summary table when payment method data is available.

The `ingreso_total` values are formmated as corruncy before the summaries are converted into plain-text tables.

The city summary is optional and is only included when `city_summary` is available in the analysis result.

The payment method summary is optional and is only included when `payment_method_summary` is available in the analysis result.

The pandas indexes are excluded from the generated tables.

#### Validation Errors

The `get_errors()` function generates the validation errors section.

It performs the following operations:

1. Sorts errors by CSV line number.
2. Includes the affected column.
3. Includes the error type.
4. Includes the descriptive error message.
5. Includes the original value when one is available.
6. Indicates when no validation errors were found.

Each validation error may contain:

- `line_number`
- `column`
- `error_type`
- `message`
- `original_value`

#### Validation Warnings

The `get_warnings()` function generates the non-critical warnings section.

It performs the following operations:

1. Sorts warnings by the affected product identifier.
2. Includes the warning type.
3. Includes the warning message.
4. Includes the inconsistent values detected.
5. Indicates when no warnings were found.

Each warning may contain:

- `affected_value`
- `warning_type`
- `message`
- `details`

Warnings are included in the report without invalidating the affected sales records.

#### Report Generation Process

The `generate_report()` function coordinates the complete report generation workflow.

It performs the following operations:

1. Creates the sales report title.
2. Includes the source CSV filename.
3. Includes the report generation date.
4. Adds the general sales summary.
5. Adds the best-selling product section.
6. Adds the highest-income product section.
7. Adds the highest-income category section.
8. Adds the highest-income city section when city data is available.
9. Adds the highest-income payment method section when payment method data is available-
10. Adds the Top 5 best-selling products section.
11. Adds the Top 5 highest-income products section.
12. Adds the complete product summary.
13. Adds the complete category summary.
14. Add the complete city summary when city data is available.
15. Adds the complete payment method summary when payment method data is available.
16. Adds the validation errors sections.
17. Adds the validation warnings section.
18. Combines all sections into a sinble plain-text report.

#### Report Structure

The generated report contains the following sections:

1. `SALES REPORT`
2. Source file and generation date.
3. `GENERAL SUMMARY`
4. `BEST SELLING PRODUCT`
5. `HIGHEST INCOME PRODUCT`
6. `HIGHEST INCOME CATEGORY`
7. `HIGHEST INCOME CITY` when city data is available.
8. `HIGHEST INCOME PAYMENT METHOD` when payment method data is available.
9. `TOP 5 BEST SELLING PRODUCTS`
10. `TOP 5 HIGHEST INCOME PRODUCTS`
11. `PRODUCT SUMMARY`
12. `CATEGORY SUMMARY`
13. `CITY SUMMARY` when city data is available.
14. `PAYMENT METHOD SUMMARY`when payment method data is available.
15. `VALIDATIONS ERRORS`
16. `WARNINGS`

#### Input and Output

##### Report Helper Functions

- **Input:** Sales analyis results, including general metrics, rankings, product, category, city, and payment method summaries, validation errors, or validation warnings.
- **Output:** A formatted string containing a specific report section.

##### `generate_report()`

- **Input:** An analysis-result dictionary, a list of validation errors, a list of warnings, and the source CSV `Path`.
- **Output:** A complete plain-text sales report ready to be displayed or saved.

---

### Report File Management Module

The report file management module handles the storage of generated sales reports and structured analysis results in the file system.

The module generates a shared dynamic base filename that can be used to save the plain-text report, the complete JSON analysis, and individual CSV analysis summaries.

The module currently provides the following functions:

* `save_report()`
* `create_report_base_name()`
* `save_analysis_json()`
* `save_analysis_result_csv_files()`
* `create_save_analysis_result_csv_files_and_path()`

#### Report Saving Process

The `save_report()` function performs the following operations:

1. Receives the generated report text.
2. Receives the destination folder.
3. Receives a previously generated base filename.
4. Adds the `.txt` extension to the base filename.
5. Converts the output folder into a `Path` object.
6. Creates the output directory and any missing parent directories.
7. Builds the complete output file path.
8. Opens the destination file using UTF-8 encoding.
9. Writes the report content to the file.
10. Returns the `Path` object pointing to the saved report.

#### Dynamic Base Filename Generation

The `create_report_base_name()` function generates a shared base filename using the current local date and time.

The generated value follows this format:

`sales_report_YYYY-MM-DD_HH-MM-SS-fff`

For example:

`sales_report_2026-08-23_13-45-30-125`

The same base filename is used to generate different output files from the same execution.

For example:

`sales_report_2026-08-23_13-45-30-125.txt`

`sales_report_2026-08-23_13-45-30-125.json`

The same base filename is also used to generate the individual CSV analysis summaries.

For example:

`sales_report_2026-08-23_13-45-30-125_products.csv`

`sales_report_2026-08-23_13-45-30-125_categories.csv`

Optional CSV files may also be generated:

`sales_report_2026-08-23_13-45-30-125_cities.csv`

`sales_report_2026-08-23_13-45-30-125_payment_methods.csv`

#### JSON Analysis Saving Process

The `save_analysis_json()` function saves the complete sales analysis result as a JSON file.

Before serialization, pandas `DataFrame` summaries are converted into lists of dictionaries so that they can be serialized correctly.

The following summaries are always converted:

* `product_summary`
* `category_summary`

The following summaries are converted when available:

* `city_summary`
* `payment_method_summary`

The function adds the `.json` extension to the provided base filename and writes the resulting JSON file using UTF-8 encoding and formatted indentation.

The original `analysis_result` dictionary is not modified directly because the function creates a shallow copy before preparing the JSON-compatible structure.

#### CSV Analysis Summary Saving Process

The `save_analysis_result_csv_files()` function saves aggregated analysis summaries as independent CSV files.

The following analysis summaries are always saved:

* `product_summary`
* `category_summary`

The following analysis summaries are saved only when they are available:

* `city_summary`
* `payment_method_summary`

Each generated CSV file uses the shared base filename followed by a descriptive suffix.

The function returns a dictionary containing the paths of the generated CSV files.

The returned dictionary uses Spanish keys to identify each generated summary:

* `resumen_producto`: Path of the product summary CSV file.
* `resumen_categoria`: Path of the category summary CSV file.
* `ciudad_resumen`: Path of the city summary CSV file when city analysis is available.
* `metodo_de_pago_resumen`: Path of the payment method summary CSV file when payment-method analysis is available.

The product and category entries are always included.

The city and payment-method entries are included only when the corresponding optional analysis exists.

#### CSV Result Dictionary

The dictionary returned by `save_analysis_result_csv_files()` follows this structure:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "ciudad_resumen": Path(...),
    "metodo_de_pago_resumen": Path(...)
}
```

The `ciudad_resumen` and `metodo_de_pago_resumen` entries are optional.

These dictionary keys identify the generated files inside the application and do not change the physical CSV filenames.

The internal analysis dictionary continues to use the following keys:

* `product_summary`
* `category_summary`
* `city_summary`
* `payment_method_summary`

#### Individual CSV File Creation

The `create_save_analysis_result_csv_files_and_path()` function creates and saves a single analysis summary CSV file.

It receives a pandas `DataFrame`, the destination folder, the shared base filename, and a descriptive prefix.

The function performs the following operations:

1. Builds the complete CSV filename using the shared base filename and prefix.
2. Converts the destination folder into a `Path` object.
3. Creates the destination directory and any missing parent directories.
4. Builds the complete output path.
5. Saves the DataFrame as a CSV file without its pandas index.
6. Returns the resulting `Path` object.

The descriptive prefixes currently used by the application are:

* `products`
* `categories`
* `cities`
* `payment_methods`

#### Input and Output

##### `save_report()`

* **Input:** The complete report text, the destination folder, and a base filename without an extension.
* **Output:** A `Path` object pointing to the saved TXT report file.

The output folder may be provided as either a string or a `Path` object.

##### `create_report_base_name()`

* **Input:** None.
* **Output:** A dynamic base filename containing the `sales_report` prefix and the current date and time.

##### `save_analysis_json()`

* **Input:** The analysis-result dictionary, the destination folder, and a base filename without an extension.
* **Output:** A `Path` object pointing to the saved JSON analysis file.

##### `save_analysis_result_csv_files()`

* **Input:** The analysis-result dictionary, the destination folder, and a shared base filename without an extension.
* **Output:** A dictionary containing the `Path` objects of the generated CSV analysis files, identified by the keys `resumen_producto`, `resumen_categoria`, and, when available, `ciudad_resumen` and `metodo_de_pago_resumen`.

##### `create_save_analysis_result_csv_files_and_path()`

* **Input:** A pandas `DataFrame`, the destination folder, a shared base filename, and a descriptive prefix.
* **Output:** A `Path` object pointing to the saved CSV file.

#### Error Handling

File-system errors produced while creating destination directories, writing the text report, or writing the JSON analysis file are converted into the custom `ReportSaveError` exception.

The TXT and JSON saving functions explicitly catch `OSError` exceptions and raise `ReportSaveError`.

CSV file creation currently does not convert file-system or pandas CSV-writing errors into `ReportSaveError`. Errors raised while creating or saving CSV files are propagated directly to the caller.

#### Related Exception

* `ReportSaveError`

---

### Main Application Module

The main application module acts as the console entry point for the Sales Report application.

It defines the source CSV file and output directory, delegates the complete sales-reporting workflow to the `controller` module, and displays the paths of the generated output files.

The module currently provides the following function:

- `main()`

#### Application Workflow

The `main()` function performs the following operations:

1. Defines the source CSV file path.
2. Defines the output folder.
3. Calls `controller.generate_sales_report()` to execute the complete reporting workflow.
4. Receives a dictionary containing the generated report paths.
5. Iterates through the returned results.
6. Displays the paths of the generated text and JSON files.
7. Detectes nested dictionaries containing groups of generated files.
8. Displays each individual CSV analysis file path.
9. Handles application-specific and unexpected exceptions.

#### Generate Output Results

The `main()` function receives the generated output paths from `controller.generate_sales_report()`

The returned result may contain direct file paths and nested dictionaries containing groups of generated files.

The main application does not create or save these file directly. Its responsibility is to display the results returned by the controller.

The generated files may include:

- A plain-text sales report.
- A JSON analysis file.
- Product summary CSV.
- Category summary CSV.
- City summary CSV when available.
- Payment method summary CSV when available.

#### Module Coordination

The main application interacts directly with the following module:

- `controller`: Coordinates the complete sales-report generation workflow and returns the generated output file paths.

The internal coordination between validation, CSV reading, analysis, report generation, and file management is delegate to the `controller` module.

#### Current Input and Output

- **Source file:** `data/sales.csv`
- **Output folder:** `reports`
- **Generated files:** The controller may generate a `.txt` sales report, a `.json` analysis file, and individual `.csv` analysis summary files.

All output files use the same dynamically generated base filename.

The following CSV summaries are always generated:

- Product summary.
- Category summary.

The following CSV summaries are generated when the corresponding optional analysis is available:

For example:

`sales_report_2026-08-23_14-30-25-125.txt`
`sales_report_2026-08-23_14-30-25-125.json`
`sales_report_2026-08-23_14-30-25-125_products.csv`
`sales_report_2026-08-23_14-30-25-125_categories.csv`

The source and output locations are currently defined directly inside the `main()` function.

#### Error Handling 

The main application handles two categories of errors:

- Application-specific exceptions derived from `AppError`
- Unexpected exceptions raised during execution.

When an error occurs, its message is displayed and the application workflow stops.

#### Application Entry Point

The following condition ensures that `main()` is executed only when the module is started directly:

`if __name__ == "__main__":`

This prevents the complete application workflow from running automatically when the module is imported by another Python file.

#### Input and Output

##### `main()`

- **Input:** The source CSV path and output folder configured inside the main application workflow.
- **Output:** Console messages displaying the file paths returned by `controller.generate_sales_report()`

#### Related Exceptions

- `AppError`
- Unexpected Python exceptions

---

### Sales Report Controller Module

The sales report controller module coordinates the complete sales-report generation workflow.

It acts as the orchestration layer between the main application and the specialized modules responsible for file validation, CSV reading, data validation, sales analysis, report generation, and file storage.

The controller receives teh source CSV file path and output folder, executes the complete processing workflow, generates all supported output files, measures the total execution time, and returns a structured dictionary containing processing totals, generated file paths, and execution information.

The module currently provides the following function:

- `generate_sales_report()`

#### Controller Workflow

The `generate_sales_report()` function perfroms the following operations:

1. Starts the execution timer.
2. Validates the source CSV file using `validator.validate_csv_file()`.
3. Reads the validate CSV file using `csv_reader.read_csv_file()`.
4. Normaizes and validates the sales records using `validator.validate_dataframe()`.
5. Analyzes the valid sales records using `analyzer.analyze_sales()`. 
6. Generates the complete plain-text sales report using `reporter.generate_report()`. 
7. Stores the total number of processed, valid, and invalid rows in the controller result. 8. Generates a shared dynamic base filename using `file_manager.create_report_base_name()`. 9. Saves the plain-text sales report using `file_manager.save_report()`. 
10. Saves the complete analysis result as a JSON file using `file_manager.save_analysis_json()`.
11. Saves the available analysis summaries as independent CSV files using `file_manager.save_analysis_result_csv_files()`. 
12. Calculates the total execution time. 
13. Adds the execution time to the controller result. 
14. Returns the complete result dictionary to the caller.

#### Module Coordination

The controller coordinates th following module:

- `validator`: Validates the source file path, normalizes sales data, validates records, and separates valid and invalid rows.
- `csv_reader`: Reads the validated CSV file and converts its contents into a pandas `DataFrame`.
- `analyzer`: Calculates sales metrics, aggregated summaries, rankings, and optional analyses.
- `reporter`: Converts analysis results, validation errors, and warnings into a structured plain-text sales report.
- `file_manager`: Generates the shared dynamic base filename and saves the generated TXT, JSON, and CSV files.

#### Validation Results

The controller receives the validation result produced by `validator.validate_dataframe()`.

This information includes:

- Valid sales records.
- Invlid sales records.
- Validation errors.
- Validation warnings.
- Total processed rows.
- Total valid rows.
- Total invalid rows.

The valid records are passe tod the analysis workflow, while validation errors and warnings are included in the generated plain-text report.

#### Sales Analysis

The controller send the validation result to `analyzer.analyze_sales()`

The analysis result contains the general sales metrics and aggregated summaries required by the reporting and file-management processes.

These results may include:

- Total income.
- Total units sold. 
- Product summary.
- Category summary.
- Best-selling products.
- Highest-income products.
- Highest-income categories.
- Top 5 product rankings.
- City analysis when `ciudad` is available.
- Payment method analysis when `metodo_pago` is available.

#### Output File Coordination

A single Dynamic base filename is generated during each controller execution.

The same base filename is used for all output files generated during that execution.

The controller generates:

- A plain-text sales report.
- A JSON file containing the complete structured analysis result.
- A product summary CSV file.
- A category summary CSV file.

When optional analysis information is available, it may also generate.

- A city summary CSV file.
- A payment method summary CSV file.

For example:

`sales_report_2026-08-29_09-30-25-125.txt` 
`sales_report_2026-08-29_09-30-25-125.json`
`sales_report_2026-08-29_09-30-25-125_products.csv` 
`sales_report_2026-08-29_09-30-25-125_categories.csv`

Optional files:

`sales_report_2026-08-29_09-30-25-125_cities.csv` 
`sales_report_2026-08-29_09-30-25-125_payment_methods.csv`

#### Controller Result

The `generate_sales_report()` function returns a dictionary containing information about the complete workflow.

The result contains:

- `total_rows`: Total number of processed sales records.
- `total_valid_rows`: Number of records that passed validation.
- `total_invalid_rows`: Number of records containing validation errors.
- `report_path_txt`: `Path` object pointing to the generated plain-text sales report.
- `report_path_json`: `Path` object pointing to the generated JSON analysis file.
- `reports_path_csv`: Dictionary containing the paths of the generated CSV analysis summary files.
- `execution_tiem`: Formatted string containing the total execution time.

#### CSV Report Paths

The `reports_path_csv` value contains a nested dictionary.

The following paths are always included:

- `product_summary`
- `category_summary`

The following paths are included only when the corresponding optional analysis is available:

- `city_summary`
- `payment_method_summary`

An example structure is:

{
    "product_summary": Path(...),
    "category_summary": Path(...),
    "city_summary": Path(...)
    "payment_method_summary": Path(...)
}

#### Execution Time

The controller uses `time.perf_counter()` to measure the duration of the complete sales-report generation workflow.

The execution time includes validation, CSV readin, data analysis, report generation, and file storage.

The result is formatted in seconds with four decimal places.

For example:

`Execution time: 0.0123 seconds`

#### Input and Output

##### `generate_sales_report()`

- **Input:** A string containing the source CSV file path and a string containing the destination output folder.
- **Output:** A dictionary containing processing totals, generated TXT, JSON, and CSV file paths, and the total execution time.

#### Error Propagation

The controller does not handle application exceptions directly.

Errors raised by the validation, reading, analyisis, reporting, or file-management modules are propagated to the caller.

The main application is responsible for catching application-specific exceptions derived from `AppError` and unexpected Python exceptions.

---

### Graphical User Interface Module

The graphical user interface module provides the main desktop window for the Sales Report application using PySide6.

It allows the user to select a source CSV file, choose an output directory, generate sales reports through the backend controller, view the current application status, and display the paths of generated TXT, JSON, and CSV files.

The interface is divided into independent sections built through helper methods. This structure keeps the graphical layer modular, maintainable, and easy to extend.

The graphical interface is displayed in Spanish, while the project documentation remains in English.

The module currently provides the following class:

* `SalesReportWindow`

#### Main Window

The `SalesReportWindow` class inherits from PySide6 `QMainWindow` and represents the main desktop window of the application.

The window is configured with:

* Title: `Generador de Reportes de Ventas`
* Width: `900`
* Height: `700`
* Default output folder: `reports/`

The main window uses a central `QWidget` and a vertical `QVBoxLayout` to organize the different interface sections.

#### Interface Sections

The main application window contains the following sections:

1. Source CSV file selection.
2. Output folder selection.
3. Report generation.
4. Application status.
5. Generated file information.

Each section is created inside an independent `QGroupBox`.

#### Source CSV File Selection

The `build_selected_file_layout()` method creates the section used to select the source CSV file.

The section contains:

* A label displaying the currently selected file.
* A `Seleccionar Archivo` button.
* A file-selection dialog restricted to `.csv` files.

The button is connected to:

`selected_file_path()`

When no file has been selected, the interface displays:

`Archivo no seleccionado.`

#### CSV File Selection Process

The `selected_file_path()` method opens a `QFileDialog` that allows the user to select a CSV file.

The dialog uses the following filter:

`Archivos CSV (*.csv)`

When a valid selection is made:

1. The selected path is stored in `file_path`.
2. The selected-file label is updated.
3. The application status is updated.
4. The status message considers whether the default or a custom output folder is currently configured.

If the dialog is canceled, the current application state remains unchanged.

#### Output Folder Selection

The `build_selected_folder_layout()` method creates the section used to configure the destination folder.

The section contains:

* A label displaying the current output directory.
* A `Seleccionar Carpeta` button.

The button is connected to:

`selected_folder_path()`

The default output directory is:

`reports/`

When no custom directory has been selected, the interface informs the user that the default folder will be used.

#### Output Folder Selection Process

The `selected_folder_path()` method opens a directory-selection dialog using `QFileDialog.getExistingDirectory()`.

When a folder is selected:

1. The selected directory is stored in `output_folder`.
2. The output-folder label is updated.
3. The application status is updated.
4. The status message considers whether a source CSV file has already been selected.

If the dialog is canceled, the previously configured output directory remains unchanged.

#### Report Generation Section

The `build_generate_report_layout()` method creates the section containing the main report-generation button.

The section contains:

`Crear Reporte`

The button is connected to:

`generate_reports()`

The report-generation button is connected to the backend workflow through the Sales Report controller.

#### Report Generation Process

The `generate_reports()` method coordinates the graphical report-generation process.

It performs the following operations:

1. Updates the application status to indicate that the process has started.
2. Verifies that a source CSV file has been selected.
3. Stops the operation and displays an error message when no file is available.
4. Removes previously displayed CSV summary paths.
5. Calls `controller.generate_sales_report()` using the selected CSV path and output folder.
6. Receives the processing results and generated file paths from the controller.
7. Displays the generated TXT report path.
8. Displays the generated JSON analysis path.
9. Creates individual labels for each generated CSV summary path.
10. Adds the CSV labels to the scrollable results area.
11. Updates the application status when the report is generated successfully.
12. Displays application-specific or unexpected errors in the status area when necessary.

#### Backend Controller Integration

The graphical interface is connected to the backend workflow through:

`controller.generate_sales_report()`

The GUI provides the controller with:

* `file_path`
* `output_folder`

The controller performs the complete validation, analysis, report-generation, and file-storage workflow.

The GUI receives the controller result and displays the generated output paths to the user.

#### Application Status

The `build_status_layout()` method creates the status section of the interface.

The `status_label` is used to provide feedback about the current state of the application.

Its initial value is:

`Seleccione un archivo CSV para comenzar.`

The status may be updated when:

* A CSV file is selected.
* An output folder is selected.
* Both a CSV file and output folder are available.
* Report generation starts.
* No CSV file has been selected.
* Report generation completes successfully.
* An application-specific error occurs.
* An unexpected error occurs.

#### Generated Files Section

The `build_generated_files_layout()` method creates the section used to display generated report information.

The interface contains dedicated areas for:

* TXT report path.
* JSON analysis path.
* CSV summary paths.

The corresponding attributes include:

* `txt_file_label`
* `json_file_label`
* `csv_title_label`
* `csv_summaries_layout`

The TXT and JSON paths are displayed directly through labels.

CSV summary paths are created dynamically after each successful report-generation process.

#### Scrollable CSV Results

CSV summary paths are displayed inside a `QScrollArea`.

The scrollable area contains a dedicated `QVBoxLayout` stored in:

`csv_summaries_layout`

Each generated CSV report is represented by an independent `QLabel`.

The scroll area is configured to resize its internal widget automatically and uses a fixed height of `200` pixels.

This allows multiple CSV output paths to be displayed without increasing the size of the main window.

#### Previous Result Cleanup

The `clean_layout()` method removes widgets previously added to a layout.

Before generating a new report, the GUI uses this method to clear the existing CSV summary labels.

This prevents CSV paths from previous report generations from remaining visible when a new report is created.

#### Window State

The `SalesReportWindow` class maintains the following primary state values:

* `file_path`: Stores the selected source CSV path. Its initial value is `None`.

* `output_folder`: Stores the destination directory for generated files. Its default value is `reports/`.

The class also maintains references to interface labels, buttons, layouts, and generated-file display controls.

#### PySide6 Components

The graphical interface currently uses the following PySide6 widgets:

* `QMainWindow`: Main application window.
* `QWidget`: Central window and internal containers.
* `QPushButton`: Interactive application buttons.
* `QVBoxLayout`: Vertical organization of interface elements.
* `QLabel`: File paths, messages, and status information.
* `QGroupBox`: Visual grouping of related controls.
* `QFileDialog`: File and directory selection dialogs.
* `QScrollArea`: Scrollable display area for generated CSV summary paths.

#### Current GUI Workflow

The current graphical workflow is:

1. Open the Sales Report window.
2. Select a source CSV file.
3. Optionally select a custom output directory.
4. Use `reports/` when no custom output folder is selected.
5. Review the current application status.
6. Press the `Crear Reporte` button.
7. Validate that a CSV file has been selected.
8. Send the selected file and output directory to `controller.generate_sales_report()`.
9. Execute the complete backend reporting workflow.
10. Display the generated TXT report path.
11. Display the generated JSON analysis path.
12. Display the generated CSV summary paths inside the scrollable area.
13. Display the final success status or an error message.

#### Error Handling

The graphical interface handles two categories of errors during report generation:

* Application-specific exceptions derived from `AppError`.
* Unexpected Python exceptions.

When an error occurs, its message is displayed through `status_label`.

This keeps backend failures visible to the user without terminating the graphical application unexpectedly.

#### Input and Output

##### `SalesReportWindow`

* **Input:** User interaction through the graphical interface.
* **Output:** A desktop window for configuring, generating, and displaying sales-report results.

##### `selected_file_path()`

* **Input:** A CSV file selected through `QFileDialog`.
* **Output:** Updates `file_path`, the selected-file label, and the application status.

##### `selected_folder_path()`

* **Input:** A directory selected through `QFileDialog`.
* **Output:** Updates `output_folder`, the output-folder label, and the application status.

##### `generate_reports()`

* **Input:** The selected CSV path and configured output folder.
* **Output:** Generates reports through the controller and updates the GUI with TXT, JSON, and CSV output paths or an error message.

##### `clean_layout()`

* **Input:** A Qt layout containing dynamically generated widgets.
* **Output:** Removes the widgets currently contained in the layout.

#### Current Development Status

The graphical interface is connected to the existing Sales Report backend workflow.

Currently available:

* Main application window.
* CSV file selection.
* Output folder selection.
* Default output folder.
* Application status messages.
* Backend controller integration.
* Report-generation button.
* TXT report path display.
* JSON analysis path display.
* Dynamic CSV summary path display.
* Scrollable CSV results area.
* Cleanup of previous CSV results.
* Application-specific error presentation.
* Unexpected error presentation.

---

### Graphical Application Entry Point Module

The graphical application entry point module initializes and launches the PySide6 desktop application.

It creates the Qt application environment, initializes the main Sales Report window, displays the graphical interface, and starts the Qt event loop.

Unlike the graphical user interface module, this module does not define the interface structure or application controls. Its responsibility is only to start the desktop application.

#### Application Initialization

The module creates a `QApplication` instance using:

`QApplication(sys.argv)`

The `QApplication` object manages the graphical application environment and receives command-line arguments provided when the program is executed.

#### Main Window Initialization

The main application window is created using:

`main_windows.SalesReportWindow()`

The `SalesReportWindow` class is provided by the graphical user interface module.

This separates the application startup logic from the graphical interface implementation and backend processing workflow.

#### Window Display

After the main window is created, the application calls:

`show()`

This displays the Sales Report graphical interface to the user.

#### Qt Event Loop

The application starts the Qt event loop using:

`app.exec()`

The event loop keeps the graphical application running and processes user interactions such as:

* Button clicks.
* File-selection dialogs.
* Folder-selection dialogs.
* Report-generation actions.
* Report-viewer windows.
* Message boxes.
* Window events.
* Application closing events.

#### Application Exit

The result returned by the Qt event loop is passed to:

`sys.exit()`

This allows the application to terminate using the exit status returned by PySide6.

#### Application Startup Workflow

The graphical application starts using the following process:

1. Imports the Python `sys` module.
2. Imports `QApplication` from PySide6.
3. Imports the graphical window module.
4. Creates the `QApplication` instance.
5. Creates an instance of `SalesReportWindow`.
6. Displays the main application window.
7. Starts the Qt event loop.
8. Processes graphical user interactions while the application remains open.
9. Returns the application exit status to the operating system when the application closes.

#### Module Coordination

The graphical application entry point interacts directly with:

* `PySide6.QtWidgets.QApplication`: Creates and manages the Qt application environment.
* `main_windows`: Provides the `SalesReportWindow` graphical interface.

The entry point does not interact directly with the sales-report backend modules.

Backend processing is initiated through `SalesReportWindow`, which communicates with the Sales Report controller when the user starts the report-generation process.

#### Input and Output

* **Input:** Command-line arguments received through `sys.argv` and subsequent user interaction with the graphical application.

* **Output:** A running PySide6 desktop application displaying the `SalesReportWindow` interface.

#### Responsibilities

This module is responsible for:

* Creating the Qt application environment.
* Creating the main Sales Report window.
* Displaying the graphical interface.
* Starting the Qt event loop.
* Keeping the graphical application responsive to user interactions.
* Managing the final application exit status.

This module is not responsible for:

* Building graphical interface layouts.
* Selecting CSV files.
* Selecting output folders.
* Displaying generated report contents.
* Validating sales data.
* Analyzing sales records.
* Generating reports.
* Saving output files.
* Handling the internal backend workflow.

These responsibilities belong to the graphical interface, controller, and specialized backend modules.

#### Application Relationship

The graphical application startup and processing relationship can be represented as:

`Graphical Application Entry Point`

→ `QApplication`

→ `SalesReportWindow`

→ Graphical user interaction

→ `controller.generate_sales_report()`

→ Sales Report backend workflow

The application entry point only initializes and runs the graphical environment. The communication with the backend controller is performed by the `SalesReportWindow` graphical interface.

---

### Report File Viewer Module

The report file viewer module provides a dedicated PySide6 window for displaying the contents of generated report files.

It is used by the main graphical interface to open TXT, JSON, and CSV reports without modifying their contents.

The viewer receives a window title and a file path, reads the selected file using UTF-8 encoding, displays its contents inside a read-only text area, and provides a button for closing the viewer.

The module currently provides the following class:

* `FileViewerWindow`

#### File Viewer Window

The `FileViewerWindow` class inherits from PySide6 `QMainWindow` and represents an independent report-viewing window.

The window is configured with:

* A dynamic title received when the window is created.
* Width: `700`
* Height: `900`
* A read-only report display area.
* A close button.

The window title allows the main graphical interface to identify the type of report being displayed, such as TXT, JSON, or CSV.

#### Window Initialization

The `FileViewerWindow` constructor receives:

* `title`: Title displayed in the viewer window.
* `name_path`: Path of the report file to read and display.

During initialization, the class:

1. Stores the window title.
2. Stores the report file path.
3. Configures the window title and fixed size.
4. Creates the central widget.
5. Creates the main vertical layout.
6. Builds the report text area.
7. Builds the close-button area.
8. Adds both sections to the main window.

#### Report Display Area

The `build_text_area()` method creates the section responsible for displaying the selected report.

The section contains a read-only `QTextEdit` widget.

The report file is read using:

`Path.read_text(encoding="utf-8")`

The complete file contents are then displayed as plain text inside the text area.

Because the `QTextEdit` widget is configured as read-only, the user can inspect the report without modifying its contents through the application.

#### Supported Report Files

The file viewer can display text-based files generated by the Sales Report application.

The main graphical interface currently uses it for:

* TXT sales reports.
* JSON analysis files.
* CSV analysis summaries.

The viewer itself does not perform format-specific parsing. It reads the selected file as UTF-8 text and displays its contents directly.

#### Close Button Area

The `build_button_area()` method creates a horizontal layout containing the:

`Cerrar reporte`

button.

The button is connected directly to the window's:

`close()`

method.

When pressed, the report viewer window is closed without affecting the main Sales Report application window.

#### PySide6 Components

The report file viewer currently uses the following PySide6 components:

* `QMainWindow`: Independent report viewer window.
* `QWidget`: Central window container.
* `QVBoxLayout`: Main vertical organization of the viewer.
* `QHBoxLayout`: Horizontal organization of the close-button area.
* `QTextEdit`: Read-only display of report contents.
* `QGroupBox`: Visual grouping of the report display area.
* `QPushButton`: Button used to close the viewer.

#### File Handling

The viewer uses Python's `pathlib.Path` to access the selected report file.

The report is read using UTF-8 encoding:

`Path(self.name_path).read_text(encoding="utf-8")`

The file is only read by this module.

The viewer does not:

* Modify the report.
* Save changes.
* Delete files.
* Rename files.
* Generate new reports.

#### Input and Output

##### `FileViewerWindow`

* **Input:** A window title and the path of a text-based report file.
* **Output:** An independent graphical window displaying the report contents.

##### `build_text_area()`

* **Input:** The report path stored in `name_path`.
* **Output:** A `QGroupBox` containing a read-only text area with the report contents.

##### `build_button_area()`

* **Input:** No external input.
* **Output:** A `QHBoxLayout` containing the button used to close the viewer.

#### Integration with the Main GUI

The report file viewer is opened from the main `SalesReportWindow`.

The graphical interface currently uses separate methods to display generated reports:

* `open_report_txt()`
* `open_report_json()`
* `open_report_csv()`

Each method creates a new `FileViewerWindow` instance using the corresponding generated report path.

The relationship can be represented as:

`SalesReportWindow`

→ User selects generated report

→ `FileViewerWindow`

→ Read report file

→ Display contents in read-only mode

#### Responsibilities

This module is responsible for:

* Creating an independent report-viewing window.
* Reading a generated report file.
* Displaying the file contents as plain text.
* Preventing modification through the viewer.
* Providing a control for closing the report window.

This module is not responsible for:

* Generating sales reports.
* Validating CSV files.
* Analyzing sales data.
* Saving report files.
* Selecting the source CSV file.
* Selecting the output folder.

Those responsibilities belong to the controller, backend modules, and main graphical interface.

---
