# Sales Report

> **Project Status:** Version 3.0.2 completed - Functional desktop application with PySide6. This project has been manually tested with a sample sales CSV file.

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
* `gui.main_window`: Provides the main PySide6 graphical interface.
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

The `validate_csv_file()` function validates the physical source file before the CSV reading stage.

It performs the following checks:

1. Verifies that the provided path is not `None` or empty.
2. Converts the string path into a `Path` object.
3. Confirms that the path exists in the file system.
4. Ensures that the path points to a regular file rather than a directory.
5. Validates that the file has a `.csv` extension.
6. Ensures that the file is not empty by checking its file size.
7. Verifies that the file can be opened and read.
8. Returns the validated `Path` object.

File readability is checked by opening the file in binary mode and reading a single byte.

This step only verifies that the file is physically accessible. It does not parse the CSV structure or decode the file contents.

CSV decoding, parsing, and conversion into a pandas `DataFrame` are handled later by the CSV reading module.

If the file cannot be opened or read because of a file-system error, the original `OSError` is converted into `FileReadError`.


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

The CSV reading module reads a previously validated CSV file and converts its contents into a pandas `DataFrame` for subsequent validation and analysis.

Its main function, `read_csv_file()`, receives a validated `Path` object and reads the source file using `pandas.read_csv()` with UTF-8 encoding.

All columns are loaded as strings, and empty cells are preserved as empty strings instead of being automatically converted into missing values.

This keeps the original CSV values available for consistent validation by later application modules.

#### CSV Reading Process

The `read_csv_file()` function performs the following operations:

1. Receives a previously validated `Path` object.
2. Reads the CSV file using `pandas.read_csv()`.
3. Uses UTF-8 encoding.
4. Loads all columns as strings through `dtype=str`.
5. Preserves empty cells through `keep_default_na=False`.
6. Converts the CSV contents into a pandas `DataFrame`.
7. Returns the raw `DataFrame` for the validation stage.
8. Converts supported file-reading, empty-data, and CSV-parsing failures into the custom `FileReadError` exception.

#### pandas Reading Configuration

The CSV file is read using the following configuration:

```python
pd.read_csv(
    file_path,
    dtype=str,
    keep_default_na=False,
    encoding="utf-8"
)
```

The configuration is intentionally designed to preserve raw input values before validation.

* `dtype=str`: Loads all columns as strings and prevents automatic numeric or date conversion.
* `keep_default_na=False`: Preserves empty CSV cells as empty strings instead of converting them into `NaN`.
* `encoding="utf-8"`: Reads the source file using UTF-8 encoding.

This behavior allows the validation module to inspect and normalize the source values consistently.

#### Input and Output

##### `read_csv_file()`

* **Input:** A validated `Path` object pointing to the source CSV file.
* **Output:** A pandas `DataFrame` containing the raw CSV data with all columns loaded as strings and empty cells preserved.

#### Error Handling

The function converts the following exceptions into:

`FileReadError`

Handled exceptions include:

* `OSError`: File-system or file-reading failure.
* `pandas.errors.EmptyDataError`: The CSV file contains no readable data.
* `pandas.errors.ParserError`: pandas cannot parse the CSV structure correctly.

The original exception is preserved through exception chaining when `FileReadError` is raised.

#### Workflow Relationship

The CSV reading module operates after source-file validation and before DataFrame validation.

The relationship can be represented as:

`validator.validate_csv_file()`

→ `csv_reader.read_csv_file()`

→ raw pandas `DataFrame`

→ `validator.validate_dataframe()`

The module is responsible only for reading the validated CSV file and converting it into the raw DataFrame expected by the validation workflow.

#### Related Exception

* `FileReadError`

---

### Sales Analysis Module

The sales analysis module processes previously validated sales records and calculates the main metrics and aggregated summaries required for report generation and file export.

Each analysis operation is implemented in an independent helper function. This modular structure keeps the analysis workflow easier to maintain, test, understand, and extend without modifying the complete analysis process.

The module calculates general sales metrics, product and category summaries, monthly sales summaries, Top 5 product rankings, maximum-value records, and optional city and payment-method analyses.

The module currently provides the following functions:

* `create_income_column()`
* `get_total_income()`
* `get_total_units_sold()`
* `get_product_summary()`
* `get_category_summary()`
* `get_city_summary()`
* `get_payment_method_summary()`
* `get_records_with_max_value()`
* `get_top_5_best_selling_products()`
* `get_top_5_highest_income_products()`
* `get_monthly_summary()`
* `analyze_sales()`

#### Income Calculation

The `create_income_column()` function calculates the income generated by each valid sales record.

It multiplies:

`precio`

by:

`cantidad`

and stores the result in:

`ingreso_fila`

The provided DataFrame is modified directly and returned with the calculated column.

#### General Sales Metrics

The module calculates the following general metrics:

* `get_total_income()`: Adds all values from the `ingreso_fila` column and returns the result as a standard Python `float`.
* `get_total_units_sold()`: Adds all values from the `cantidad` column and returns the result as a standard Python `int`.

These values are later stored in the complete analysis result.

#### Product Summary

The `get_product_summary()` function groups valid sales records by:

`producto_id`

For each product, it preserves the first associated:

* Product name.
* Product category.

It also calculates:

* Total units sold.
* Total income generated.

The resulting DataFrame contains:

* `producto_id`
* `producto`
* `categoria`
* `unidades_vendidas`
* `ingreso_total`

#### Category Summary

The `get_category_summary()` function groups valid sales records by:

`categoria`

For each category, it calculates:

* Total units sold.
* Total income generated.

The resulting DataFrame contains:

* `categoria`
* `unidades_vendidas`
* `ingreso_total`

#### Monthly Summary

The `get_monthly_summary()` function creates an aggregated sales summary grouped by month.

The `fecha` column is converted into the following format:

`YYYY-MM`

Sales records are then grouped by month.

For each month, the function calculates:

* Number of valid sales rows.
* Total units sold.
* Total income generated.

The resulting DataFrame contains:

* `mes`: Month represented in `YYYY-MM` format.
* `filas_validas`: Number of valid sales records for the month.
* `unidades_vendidas`: Total units sold during the month.
* `ingreso_total`: Total income generated during the month.

The monthly summary is sorted chronologically from the earliest month to the latest month.

#### City Summary

The `get_city_summary()` function groups valid sales records by:

`ciudad`

when the optional city column is available.

Records containing empty city values are excluded before aggregation.

For each city, the function calculates:

* Total units sold.
* Total income generated.

The resulting DataFrame contains:

* `ciudad`
* `unidades_vendidas`
* `ingreso_total`

The city summary is sorted from highest to lowest total income.

City analysis is optional and is only performed when the `ciudad` column is present.

#### Payment Method Summary

The `get_payment_method_summary()` function groups valid sales records by:

`metodo_pago`

when the optional payment-method column is available.

Records containing empty payment-method values are excluded before aggregation.

For each payment method, the function calculates:

* Total units sold.
* Total income generated.

The resulting DataFrame contains:

* `metodo_pago`
* `unidades_vendidas`
* `ingreso_total`

The payment-method summary is sorted from highest to lowest total income.

Payment-method analysis is optional and is only performed when the `metodo_pago` column is present.

#### Maximum-Value Records

The `get_records_with_max_value()` function identifies all records containing the maximum value in a specified numeric column.

The function determines the maximum value and preserves every record tied for that value.

The selected records are returned as a list of dictionaries.

This reusable function is used to determine:

* The product or products with the highest number of units sold.
* The product or products with the highest total income.
* The category or categories with the highest total income.
* The city or cities with the highest total income when city data is available.
* The payment method or payment methods with the highest total income when payment-method data is available.

If multiple records share the maximum value, all tied records are included.

#### Top Product Rankings

The module generates two Top 5 product rankings.

##### `get_top_5_best_selling_products()`

Sorts the product summary by:

1. `unidades_vendidas` in descending order.
2. `ingreso_total` in descending order as a secondary criterion.

The function returns up to five products as a list of dictionaries.

##### `get_top_5_highest_income_products()`

Sorts the product summary by:

`ingreso_total`

in descending order and returns up to five products.

The result is returned as a list of dictionaries.

#### Sales Analysis Process

The `analyze_sales()` function coordinates the complete sales-analysis workflow.

It performs the following operations:

1. Extracts valid sales rows and validation totals.
2. Creates a copy of the valid sales DataFrame.
3. Verifies that at least one valid row is available.
4. Creates the `ingreso_fila` column.
5. Calculates total income.
6. Calculates total units sold.
7. Creates the product summary.
8. Creates the category summary.
9. Creates the monthly summary.
10. Identifies the best-selling product or products.
11. Identifies the product or products with the highest income.
12. Identifies the category or categories with the highest income.
13. Creates the Top 5 best-selling products ranking.
14. Creates the Top 5 highest-income products ranking.
15. Creates the city summary when the optional `ciudad` column is available.
16. Identifies the city or cities with the highest income when city analysis is available.
17. Creates the payment-method summary when the optional `metodo_pago` column is available.
18. Identifies the payment method or methods with the highest income when payment-method analysis is available.
19. Returns the complete analysis result.

#### Analysis Result

The `analyze_sales()` function returns a dictionary containing the complete sales-analysis result.

The following entries are always included:

* `total_rows`: Total number of processed sales records.
* `total_valid_rows`: Number of records that passed validation.
* `total_invalid_rows`: Number of records containing validation errors.
* `total_income`: Total income generated by valid sales.
* `total_units_sold`: Total number of units sold.
* `product_summary`: pandas `DataFrame` containing aggregated product results.
* `category_summary`: pandas `DataFrame` containing aggregated category results.
* `monthly_summary`: pandas `DataFrame` containing aggregated monthly sales results.
* `best_selling_product`: List containing the product or products tied for the highest number of units sold.
* `highest_income_product`: List containing the product or products tied for the highest total income.
* `highest_income_category`: List containing the category or categories tied for the highest total income.
* `top_5_best_selling_products`: List containing up to five products with the highest number of units sold.
* `top_5_highest_income_products`: List containing up to five products with the highest total income.

When the optional `ciudad` column is present, the result also contains:

* `city_summary`: pandas `DataFrame` containing aggregated city results.
* `highest_income_city`: List containing the city or cities tied for the highest total income.

When the optional `metodo_pago` column is present, the result also contains:

* `payment_method_summary`: pandas `DataFrame` containing aggregated payment-method results.
* `highest_income_payment_method`: List containing the payment method or methods tied for the highest total income.

#### Monthly Analysis Result

The `monthly_summary` DataFrame follows this structure:

```text
mes | filas_validas | unidades_vendidas | ingreso_total
```

For example:

```text
2026-07 | 25 | 84 | 15420.50
2026-08 | 31 | 102 | 18750.00
2026-09 | 18 | 56 | 9320.75
```

This structure allows other application modules to use monthly information for reporting, spreadsheet export, or future visual analysis.

#### Optional Analysis

City and payment-method analyses depend on the presence of their corresponding optional columns.

If `ciudad` exists:

`analyze_sales()` adds:

* `city_summary`
* `highest_income_city`

If `metodo_pago` exists:

`analyze_sales()` adds:

* `payment_method_summary`
* `highest_income_payment_method`

The remaining core analysis results, including `monthly_summary`, are generated independently of these optional fields.

#### Input and Output

##### `create_income_column()`

* **Input:** Valid sales DataFrame containing numeric `precio` and `cantidad`.
* **Output:** The same DataFrame with `ingreso_fila` added.

##### `get_total_income()`

* **Input:** DataFrame containing `ingreso_fila`.
* **Output:** Total sales income as a Python `float`.

##### `get_total_units_sold()`

* **Input:** DataFrame containing `cantidad`.
* **Output:** Total units sold as a Python `int`.

##### `get_product_summary()`

* **Input:** Valid sales DataFrame containing `ingreso_fila`.
* **Output:** Product-summary DataFrame.

##### `get_category_summary()`

* **Input:** Valid sales DataFrame containing `ingreso_fila`.
* **Output:** Category-summary DataFrame.

##### `get_monthly_summary()`

* **Input:** Valid sales DataFrame containing a datetime `fecha` column and `ingreso_fila`.
* **Output:** Monthly-summary DataFrame containing `mes`, `filas_validas`, `unidades_vendidas`, and `ingreso_total`.

##### `get_city_summary()`

* **Input:** Valid sales DataFrame containing `ciudad` and `ingreso_fila`.
* **Output:** City-summary DataFrame.

##### `get_payment_method_summary()`

* **Input:** Valid sales DataFrame containing `metodo_pago` and `ingreso_fila`.
* **Output:** Payment-method-summary DataFrame.

##### `get_records_with_max_value()`

* **Input:** DataFrame and numeric column name.
* **Output:** List of dictionaries containing all records tied for the maximum value.

##### `get_top_5_best_selling_products()`

* **Input:** Product-summary DataFrame.
* **Output:** List containing up to five best-selling products.

##### `get_top_5_highest_income_products()`

* **Input:** Product-summary DataFrame.
* **Output:** List containing up to five highest-income products.

##### `analyze_sales()`

* **Input:** Dictionary containing validated sales rows and validation totals.
* **Output:** Dictionary containing general sales metrics, product, category, and monthly summaries, Top 5 rankings, highest-performing records, and optional city and payment-method analysis.

#### Error Handling

The analysis workflow verifies that valid sales records are available before calculating metrics.

If the validated DataFrame contains no valid rows:

`NoValidRowsError`

is raised.

This prevents the remaining analysis operations from being performed on an empty sales dataset.

#### Related Exception

* `NoValidRowsError`

---

### Sales Report Generation Module

The sales report generation module converts sales analysis results, validation errors, and warnings into a structured plain-text sales report.

Each report section is generated by an independent helper function. This modular structure keeps the reporting workflow easier to maintain, test, modify, and extend.

The generated report includes general sales metrics, highest-performing records, Top 5 product rankings, product, category, and monthly summaries, validation errors, and validation warnings.

Optional city-based and payment-method-based sections are also included when the corresponding analysis information is available.

The module currently provides the following functions:

* `get_general_summary()`
* `get_best_selling_product()`
* `get_highest_income_product()`
* `get_highest_income_category()`
* `get_highest_income_city()`
* `get_highest_income_payment_method()`
* `get_top_5_best_selling_products()`
* `get_top_5_highest_income_products()`
* `get_product_summary()`
* `get_category_summary()`
* `get_city_summary()`
* `get_payment_method_summary()`
* `get_monthly_summary()`
* `get_errors()`
* `get_warnings()`
* `generate_report()`

#### General Summary

The `get_general_summary()` function generates the main sales-metrics section.

It includes:

* Total processed rows.
* Total valid rows.
* Total invalid rows.
* Total income.
* Total units sold.

The total income is formatted with thousands separators and two decimal places.

The generated section begins with:

`RESUMEN GENERAL`

#### Best-Selling Product

The `get_best_selling_product()` function formats the product or products with the highest number of units sold.

For each product, the section includes:

* `producto_id`
* `producto`
* `unidades_vendidas`

If multiple products share the highest number of units sold, all tied products are included.

The generated section begins with:

`PRODUCTO MÁS VENDIDO`

#### Highest-Income Product

The `get_highest_income_product()` function formats the product or products that generated the highest total income.

For each product, the section includes:

* `producto_id`
* `producto`
* `ingreso_total`

The income value is formatted as currency.

If multiple products share the highest income, all tied products are included.

The generated section begins with:

`PRODUCTO CON MAYOR INGRESO`

#### Highest-Income Category

The `get_highest_income_category()` function formats the category or categories that generated the highest total income.

For each category, the section includes:

* `categoria`
* `ingreso_total`

The income value is formatted as currency.

If multiple categories share the highest income, all tied categories are included.

The generated section begins with:

`CATEGORÍA CON MAYOR INGRESO`

#### Highest-Income City

The `get_highest_income_city()` function formats the city or cities that generated the highest total income.

For each city, the section includes:

* `ciudad`
* `ingreso_total`
* `unidades_vendidas`

If multiple cities share the highest income, all tied cities are included.

This section is generated only when city analysis is available.

The generated section begins with:

`CIUDAD CON MAYOR INGRESO`

#### Highest-Income Payment Method

The `get_highest_income_payment_method()` function formats the payment method or payment methods that generated the highest total income.

For each payment method, the section includes:

* `metodo_pago`
* `ingreso_total`
* `unidades_vendidas`

If multiple payment methods share the highest income, all tied payment methods are included.

This section is generated only when payment-method analysis is available.

The generated section begins with:

`MÉTODO DE PAGO CON MAYOR INGRESO`

#### Top Product Rankings

The module generates two Top 5 product-ranking sections.

##### `get_top_5_best_selling_products()`

Formats up to five products with the highest number of units sold.

Each ranking entry includes:

* Ranking position.
* `producto_id`
* `producto`
* `unidades_vendidas`
* `ingreso_total`

The generated section begins with:

`TOP 5 PRODUCTOS MÁS VENDIDOS`

##### `get_top_5_highest_income_products()`

Formats up to five products with the highest total income.

Each ranking entry includes:

* Ranking position.
* `producto_id`
* `producto`
* `ingreso_total`
* `unidades_vendidas`

The generated section begins with:

`TOP 5 PRODUCTOS CON MAYOR INGRESO`

#### Product Summary

The `get_product_summary()` function converts the aggregated `product_summary` DataFrame into a plain-text table.

Before conversion, a copy of the DataFrame is created so that display formatting does not modify the original analysis result.

The `ingreso_total` column is formatted as currency.

The pandas index is excluded from the generated table.

The generated section begins with:

`RESUMEN POR PRODUCTO`

#### Category Summary

The `get_category_summary()` function converts the aggregated `category_summary` DataFrame into a plain-text table.

A display copy of the DataFrame is created and the `ingreso_total` column is formatted as currency.

The pandas index is excluded.

The generated section begins with:

`RESUMEN POR CATEGORÍA`

#### City Summary

The `get_city_summary()` function converts the optional `city_summary` DataFrame into a plain-text table.

A display copy is created and `ingreso_total` values are formatted as currency.

The city summary is included only when `city_summary` is available in the analysis result.

The pandas index is excluded.

The generated section begins with:

`RESUMEN POR CIUDAD`

#### Payment-Method Summary

The `get_payment_method_summary()` function converts the optional `payment_method_summary` DataFrame into a plain-text table.

A display copy is created and `ingreso_total` values are formatted as currency.

The payment-method summary is included only when `payment_method_summary` is available in the analysis result.

The pandas index is excluded.

The generated section begins with:

`RESUMEN POR MÉTODO DE PAGO`

#### Monthly Summary

The `get_monthly_summary()` function converts the `monthly_summary` DataFrame into a plain-text table.

A display copy of the DataFrame is created before formatting.

The `ingreso_total` column is formatted as currency before the DataFrame is converted into plain text.

The monthly summary contains the aggregated monthly analysis produced by the sales-analysis module, including:

* `mes`
* `filas_validas`
* `unidades_vendidas`
* `ingreso_total`

The pandas index is excluded from the generated table.

The generated section begins with:

`RESUMEN POR MES`

Unlike city and payment-method summaries, the monthly summary is part of the standard report-generation workflow.

#### Validation Errors

The `get_errors()` function generates the validation-errors section.

It performs the following operations:

1. Adds the validation-errors section title.
2. Detects when no validation errors are available.
3. Sorts errors by CSV line number.
4. Includes the affected column.
5. Includes the error type.
6. Includes the descriptive error message.
7. Includes the original value when one is available.

Each validation error may contain:

* `line_number`
* `column`
* `error_type`
* `message`
* `original_value`

When no errors are available, the report indicates:

`No se encontraron errores de validación.`

The generated section begins with:

`ERRORES DE VALIDACIÓN`

#### Validation Warnings

The `get_warnings()` function generates the non-critical warnings section.

It performs the following operations:

1. Adds the warning section title.
2. Detects when no warnings are available.
3. Sorts warnings by `affected_value`.
4. Includes the affected value.
5. Includes the warning type.
6. Includes the warning message.
7. Includes the warning details.

Each warning may contain:

* `affected_value`
* `warning_type`
* `message`
* `details`

When `details` contains multiple values, they are joined into comma-separated text for display.

When no warnings are available, the report indicates:

`No se encontraron advertencias.`

Warnings are included without automatically invalidating the corresponding sales records.

The generated section begins with:

`ADVERTENCIAS`

#### Report Header

The `generate_report()` function begins the report with:

`REPORTE DE VENTAS`

The report header also includes:

* The original source CSV filename.
* The report generation date.

The source filename is obtained from:

`source_filename.name`

The generation date is obtained using:

`date.today()`

#### Report Generation Process

The `generate_report()` function coordinates the complete plain-text report-generation workflow.

It performs the following operations:

1. Creates the `REPORTE DE VENTAS` title.
2. Adds the source CSV filename.
3. Adds the report generation date.
4. Adds the general sales summary.
5. Adds the best-selling product section.
6. Adds the highest-income product section.
7. Adds the highest-income category section.
8. Adds the highest-income city section when city analysis is available.
9. Adds the highest-income payment-method section when payment-method analysis is available.
10. Adds the Top 5 best-selling products section.
11. Adds the Top 5 highest-income products section.
12. Adds the complete product summary.
13. Adds the complete category summary.
14. Adds the complete city summary when city analysis is available.
15. Adds the complete payment-method summary when payment-method analysis is available.
16. Adds the monthly sales summary.
17. Adds the validation-errors section.
18. Adds the validation-warnings section.
19. Combines all generated sections into a single plain-text report.

#### Optional Report Sections

City and payment-method sections depend on optional analysis results.

When `highest_income_city` is available, the report includes:

`CIUDAD CON MAYOR INGRESO`

When `city_summary` is available, the report includes:

`RESUMEN POR CIUDAD`

When `highest_income_payment_method` is available, the report includes:

`MÉTODO DE PAGO CON MAYOR INGRESO`

When `payment_method_summary` is available, the report includes:

`RESUMEN POR MÉTODO DE PAGO`

These sections are omitted when their corresponding analysis results are unavailable.

#### Report Structure

The complete report follows this general order:

1. `REPORTE DE VENTAS`
2. Source filename and generation date.
3. `RESUMEN GENERAL`
4. `PRODUCTO MÁS VENDIDO`
5. `PRODUCTO CON MAYOR INGRESO`
6. `CATEGORÍA CON MAYOR INGRESO`
7. `CIUDAD CON MAYOR INGRESO` when city analysis is available.
8. `MÉTODO DE PAGO CON MAYOR INGRESO` when payment-method analysis is available.
9. `TOP 5 PRODUCTOS MÁS VENDIDOS`
10. `TOP 5 PRODUCTOS CON MAYOR INGRESO`
11. `RESUMEN POR PRODUCTO`
12. `RESUMEN POR CATEGORÍA`
13. `RESUMEN POR CIUDAD` when city analysis is available.
14. `RESUMEN POR MÉTODO DE PAGO` when payment-method analysis is available.
15. `RESUMEN POR MES`
16. `ERRORES DE VALIDACIÓN`
17. `ADVERTENCIAS`

#### Display Formatting

The reporter does not modify the original analysis DataFrames when preparing summary tables for display.

For product, category, city, payment-method, and monthly summaries, a copy of the corresponding DataFrame is created.

The `ingreso_total` column is then formatted using currency notation.

For example:

`$12,450.75`

The resulting DataFrame is converted into plain text using:

`DataFrame.to_string(index=False)`

This preserves the tabular structure while excluding pandas indexes.

#### Input and Output

##### Report Helper Functions

* **Input:** Sales-analysis results, rankings, summary DataFrames, validation errors, or validation warnings.
* **Output:** A formatted string representing a specific plain-text report section.

##### `get_general_summary()`

* **Input:** Analysis-result dictionary.
* **Output:** General sales metrics section.

##### `get_best_selling_product()`

* **Input:** Analysis-result dictionary.
* **Output:** Best-selling product section.

##### `get_highest_income_product()`

* **Input:** Analysis-result dictionary.
* **Output:** Highest-income product section.

##### `get_highest_income_category()`

* **Input:** Analysis-result dictionary.
* **Output:** Highest-income category section.

##### `get_highest_income_city()`

* **Input:** Analysis-result dictionary containing city analysis.
* **Output:** Highest-income city section.

##### `get_highest_income_payment_method()`

* **Input:** Analysis-result dictionary containing payment-method analysis.
* **Output:** Highest-income payment-method section.

##### `get_top_5_best_selling_products()`

* **Input:** Analysis-result dictionary.
* **Output:** Top 5 best-selling products section.

##### `get_top_5_highest_income_products()`

* **Input:** Analysis-result dictionary.
* **Output:** Top 5 highest-income products section.

##### `get_product_summary()`

* **Input:** Analysis-result dictionary containing `product_summary`.
* **Output:** Formatted product-summary table.

##### `get_category_summary()`

* **Input:** Analysis-result dictionary containing `category_summary`.
* **Output:** Formatted category-summary table.

##### `get_city_summary()`

* **Input:** Analysis-result dictionary containing `city_summary`.
* **Output:** Formatted city-summary table.

##### `get_payment_method_summary()`

* **Input:** Analysis-result dictionary containing `payment_method_summary`.
* **Output:** Formatted payment-method-summary table.

##### `get_monthly_summary()`

* **Input:** Analysis-result dictionary containing `monthly_summary`.
* **Output:** Formatted monthly-summary table.

##### `get_errors()`

* **Input:** List containing validation-error dictionaries.
* **Output:** Formatted validation-errors section.

##### `get_warnings()`

* **Input:** List containing validation-warning dictionaries.
* **Output:** Formatted validation-warnings section.

##### `generate_report()`

* **Input:** Analysis-result dictionary, validation-error list, validation-warning list, and source CSV `Path`.
* **Output:** Complete plain-text sales report ready to be displayed or saved.

#### Module Responsibility

The report-generation module is responsible for presentation formatting only.

It receives already calculated analysis results and converts them into human-readable text.

It does not:

* Validate the source CSV file.
* Read the source CSV file.
* Validate individual sales records.
* Calculate sales metrics.
* Save report files directly.

Those responsibilities belong to the validation, reading, analysis, and file-management modules.

---

### Report File Management Module

The report file management module handles the storage and export of generated sales reports and structured analysis results.

The module creates destination directories when necessary, generates a shared timestamp-based base filename, saves the human-readable report as TXT, exports the complete structured analysis as JSON, generates independent CSV analysis summaries, and creates a multi-sheet Excel workbook containing sales analysis and validation information.

The exported analysis may include product, category, monthly, city, and payment-method summaries, together with general metrics, Top 5 product rankings, validation errors, and validation warnings.

The module uses:

* `pathlib.Path` for file-system paths.
* `datetime` for dynamic report filenames.
* `json` for JSON serialization.
* `pandas` for DataFrame-based analysis results.
* `openpyxl` for XLSX workbook and worksheet generation.

The module currently provides the following functions:

* `save_report()`
* `create_report_base_name()`
* `save_analysis_json()`
* `save_analysis_result_csv_files()`
* `create_save_analysis_result_csv_files_and_path()`
* `build_sheet_general_summary()`
* `build_sheet_products()`
* `build_sheet_categories()`
* `build_sheet_bestselling()`
* `build_sheet_top_income()`
* `build_sheet_city_summary()`
* `build_sheet_payment_method_summary()`
* `build_sheet_monthly_summary()`
* `build_sheet_validation_errors()`
* `build_sheet_warnings()`
* `save_report_xlsx()`

#### Supported Output Formats

The module currently supports four output formats:

* TXT
* JSON
* CSV
* XLSX

Files generated during the same report-generation process use the same shared base filename.

#### Report Saving Process

The `save_report()` function saves the human-readable sales report as a TXT file.

It performs the following operations:

1. Receives the generated report text.
2. Receives the destination folder.
3. Receives a previously generated shared base filename.
4. Adds the `.txt` extension.
5. Converts the destination directory into a `Path` object.
6. Creates the destination directory and missing parent directories when necessary.
7. Builds the complete output path.
8. Opens the destination file using UTF-8 encoding.
9. Writes the report content.
10. Returns the `Path` pointing to the generated TXT file.

File-system `OSError` exceptions are converted into `ReportSaveError`.

#### Dynamic Base Filename Generation

The `create_report_base_name()` function generates a shared base filename using the current local date and time.

The generated filename follows this format:

`sales_report_YYYY-MM-DD_HH-MM-SS-fff`

For example:

`sales_report_2026-08-23_13-45-30-125`

The same base filename is reused across all supported output formats.

For example:

`sales_report_2026-08-23_13-45-30-125.txt`

`sales_report_2026-08-23_13-45-30-125.json`

`sales_report_2026-08-23_13-45-30-125.xlsx`

CSV summaries use the same base filename followed by a descriptive suffix:

`sales_report_2026-08-23_13-45-30-125_products.csv`

`sales_report_2026-08-23_13-45-30-125_categories.csv`

`sales_report_2026-08-23_13-45-30-125_months.csv`

Optional CSV files may also be generated:

`sales_report_2026-08-23_13-45-30-125_cities.csv`

`sales_report_2026-08-23_13-45-30-125_payment_methods.csv`

#### JSON Analysis Saving Process

The `save_analysis_json()` function saves the complete structured sales analysis as a JSON file.

Before serialization, the function creates a shallow copy of the original `analysis_result` dictionary.

pandas `DataFrame` summaries are converted into lists of dictionaries so that they can be serialized correctly.

The following summaries are always converted:

* `product_summary`
* `category_summary`
* `monthly_summary`

The following summaries are converted when available:

* `city_summary`
* `payment_method_summary`

The function:

1. Creates a copy of the analysis result.
2. Converts required DataFrames into JSON-compatible records.
3. Converts optional DataFrames when available.
4. Adds the `.json` extension to the shared base filename.
5. Creates the destination directory when necessary.
6. Writes the JSON file using UTF-8 encoding.
7. Uses formatted indentation.
8. Preserves non-ASCII characters through `ensure_ascii=False`.
9. Returns the generated file path.

The original `analysis_result` dictionary is not modified directly.

#### CSV Analysis Summary Saving Process

The `save_analysis_result_csv_files()` function saves aggregated analysis summaries as independent CSV files.

The following summaries are always exported:

* `product_summary`
* `category_summary`
* `monthly_summary`

The following summaries are exported when available:

* `city_summary`
* `payment_method_summary`

Each generated CSV file uses the shared report base filename followed by a descriptive suffix.

The individual file-creation process is delegated to:

`create_save_analysis_result_csv_files_and_path()`

The function returns a dictionary containing the generated CSV paths.

#### CSV Result Dictionary

The dictionary returned by `save_analysis_result_csv_files()` uses Spanish keys to identify the generated summaries.

It follows this structure:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "resumen_mensual": Path(...),
    "ciudad_resumen": Path(...),
    "metodo_de_pago_resumen": Path(...)
}
```

The following entries are always included:

* `resumen_producto`: Product summary CSV path.
* `resumen_categoria`: Category summary CSV path.
* `resumen_mensual`: Monthly summary CSV path.

The following entries are optional:

* `ciudad_resumen`: City summary CSV path.
* `metodo_de_pago_resumen`: Payment-method summary CSV path.

These dictionary keys identify generated files inside the application and do not modify the physical CSV filenames.

The internal analysis dictionary continues to use the following keys:

* `product_summary`
* `category_summary`
* `monthly_summary`
* `city_summary`
* `payment_method_summary`

#### Individual CSV File Creation

The `create_save_analysis_result_csv_files_and_path()` function creates and saves one analysis summary as a CSV file.

It receives:

* A pandas `DataFrame`.
* The destination directory.
* The shared base filename.
* A descriptive filename suffix.

The function:

1. Builds the filename using the shared base filename and suffix.
2. Adds the `.csv` extension.
3. Converts the destination directory into a `Path`.
4. Creates the destination directory and missing parent directories when necessary.
5. Builds the complete output path.
6. Saves the DataFrame without its pandas index.
7. Returns the generated CSV path.

The descriptive suffixes currently used are:

* `products`
* `categories`
* `months`
* `cities`
* `payment_methods`

The first three correspond to summaries generated during the standard analysis workflow.

The final two correspond to optional city and payment-method analyses.

File-system `OSError` exceptions are converted into `ReportSaveError`.

#### Excel Report Generation

The `save_report_xlsx()` function generates a complete Excel workbook containing sales-analysis and validation information.

The function:

1. Receives the complete `analysis_result`.
2. Receives validation errors.
3. Receives validation warnings.
4. Receives the destination folder.
5. Receives the shared report base filename.
6. Adds the `.xlsx` extension.
7. Creates the destination directory when necessary.
8. Creates a new openpyxl `Workbook`.
9. Removes the default worksheet created by openpyxl.
10. Builds the general summary worksheet.
11. Builds the product summary worksheet.
12. Builds the category summary worksheet.
13. Builds the monthly summary worksheet.
14. Builds optional city and payment-method worksheets when available.
15. Builds the Top 5 best-selling products worksheet.
16. Builds the Top 5 highest-income products worksheet.
17. Builds validation error and warning worksheets.
18. Saves the completed workbook.
19. Returns the resulting XLSX path.

The Excel file uses the same shared base filename as the TXT, JSON, and CSV outputs.

For example:

`sales_report_2026-08-23_13-45-30-125.xlsx`

#### Excel Workbook Structure

The XLSX workbook can contain the following worksheets:

* `Resumen General`
* `Productos`
* `Categorías`
* `Resumen por mes`
* `Productos mejor vendidos`
* `Productos con mejor ingreso`
* `Resumen por ciudad`
* `Resumen por método de pago`
* `Validación de errores`
* `Advertencias`

The following worksheets are always generated:

* General summary.
* Product summary.
* Category summary.
* Monthly summary.
* Best-selling product ranking.
* Highest-income product ranking.
* Validation errors.
* Validation warnings.

The city and payment-method worksheets are generated only when the corresponding analysis results are available.

#### General Summary Worksheet

The `build_sheet_general_summary()` function creates:

`Resumen General`

The worksheet contains two columns:

* `Métrica`
* `Valor`

The following general metrics are added:

* Total rows.
* Valid rows.
* Invalid rows.
* Total income.
* Total units sold.

The values are obtained from:

* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`
* `total_income`
* `total_units_sold`

The function returns the generated openpyxl `Worksheet`.

#### Product Summary Worksheet

The `build_sheet_products()` function creates:

`Productos`

It receives the `product_summary` pandas `DataFrame` and converts its contents into Excel rows using:

`dataframe_to_rows()`

The DataFrame headers are included and the pandas index is excluded.

The function returns the generated worksheet.

#### Category Summary Worksheet

The `build_sheet_categories()` function creates:

`Categorías`

It receives the `category_summary` pandas `DataFrame` and converts its contents into worksheet rows using:

`dataframe_to_rows()`

The DataFrame headers are included and the pandas index is excluded.

The function returns the generated worksheet.

#### Monthly Summary Worksheet

The `build_sheet_monthly_summary()` function creates:

`Resumen por mes`

It receives the `monthly_summary` pandas `DataFrame` generated by the analysis module.

The worksheet contains the monthly analysis data, including:

* `mes`
* `filas_validas`
* `unidades_vendidas`
* `ingreso_total`

The DataFrame headers are included and the pandas index is excluded.

The function returns the generated worksheet.

#### Best-Selling Products Worksheet

The `build_sheet_bestselling()` function creates:

`Productos mejor vendidos`

It receives the Top 5 best-selling product records, converts them into a pandas `DataFrame`, and writes the resulting rows into the worksheet.

The DataFrame headers are included and the pandas index is excluded.

#### Highest-Income Products Worksheet

The `build_sheet_top_income()` function creates:

`Productos con mejor ingreso`

It receives the Top 5 products ranked by generated income, converts them into a pandas `DataFrame`, and writes the resulting rows into the worksheet.

The DataFrame headers are included and the pandas index is excluded.

#### City Summary Worksheet

The `build_sheet_city_summary()` function creates:

`Resumen por ciudad`

The worksheet is generated from the `city_summary` DataFrame.

It is included only when city analysis information is available.

The DataFrame headers are included and the pandas index is excluded.

#### Payment-Method Summary Worksheet

The `build_sheet_payment_method_summary()` function creates:

`Resumen por método de pago`

The worksheet is generated from the `payment_method_summary` DataFrame.

It is included only when payment-method analysis information is available.

The DataFrame headers are included and the pandas index is excluded.

#### Validation Errors Worksheet

The `build_sheet_validation_errors()` function creates:

`Validación de errores`

The worksheet contains validation errors detected while processing the source sales records.

Internal dictionary keys are mapped to Spanish worksheet headers.

The columns are:

* `línea`
* `columna`
* `tipo_error`
* `mensaje`
* `valor_original`

Each validation error is added as an independent worksheet row.

Missing values are represented by empty strings.

#### Validation Warnings Worksheet

The `build_sheet_warnings()` function creates:

`Advertencias`

The worksheet contains warnings detected while validating and normalizing sales records.

Internal dictionary keys are mapped to Spanish worksheet headers.

The columns are:

* `tipo_advertencia`
* `campo`
* `mensaje`
* `valor_afectado`
* `detalles`

Missing values are represented by empty strings.

When a warning value contains a list, its values are converted into comma-separated text before being written to the worksheet.

#### DataFrame to Excel Conversion

Analysis DataFrames are converted into Excel-compatible rows using:

`openpyxl.utils.dataframe.dataframe_to_rows`

The module uses:

```python
dataframe_to_rows(
    df,
    index=False,
    header=True
)
```

This causes:

* DataFrame column names to become worksheet headers.
* DataFrame rows to become worksheet rows.
* pandas indexes to be excluded from the generated workbook.

#### Workbook Creation

The Excel report is created using:

`openpyxl.Workbook`

A new workbook initially contains a default worksheet.

The module removes this worksheet using:

```python
wb.remove(wb.active)
```

The application then builds the report-specific worksheets before saving the workbook.

#### Input and Output

##### `save_report()`

* **Input:** Complete report text, destination folder, and shared base filename.
* **Output:** `Path` pointing to the generated TXT report.

##### `create_report_base_name()`

* **Input:** None.
* **Output:** Shared timestamp-based report filename.

##### `save_analysis_json()`

* **Input:** Analysis-result dictionary, destination folder, and shared base filename.
* **Output:** `Path` pointing to the generated JSON analysis file.

##### `save_analysis_result_csv_files()`

* **Input:** Analysis-result dictionary, destination folder, and shared base filename.
* **Output:** Dictionary containing product, category, monthly, and optional city/payment-method CSV paths.

##### `create_save_analysis_result_csv_files_and_path()`

* **Input:** DataFrame, destination folder, shared base filename, and descriptive suffix.
* **Output:** `Path` pointing to the generated CSV file.

##### `build_sheet_general_summary()`

* **Input:** Workbook and analysis-result dictionary.
* **Output:** `Worksheet` containing the general sales summary.

##### `build_sheet_products()`

* **Input:** Workbook and product-summary DataFrame.
* **Output:** `Worksheet` containing the product summary.

##### `build_sheet_categories()`

* **Input:** Workbook and category-summary DataFrame.
* **Output:** `Worksheet` containing the category summary.

##### `build_sheet_monthly_summary()`

* **Input:** Workbook and monthly-summary DataFrame.
* **Output:** `Worksheet` containing the monthly sales summary.

##### `build_sheet_bestselling()`

* **Input:** Workbook and Top 5 best-selling product records.
* **Output:** `Worksheet` containing the best-selling product ranking.

##### `build_sheet_top_income()`

* **Input:** Workbook and Top 5 highest-income product records.
* **Output:** `Worksheet` containing the highest-income product ranking.

##### `build_sheet_city_summary()`

* **Input:** Workbook and city-summary DataFrame.
* **Output:** `Worksheet` containing the city analysis.

##### `build_sheet_payment_method_summary()`

* **Input:** Workbook and payment-method-summary DataFrame.
* **Output:** `Worksheet` containing the payment-method analysis.

##### `build_sheet_validation_errors()`

* **Input:** Workbook and validation error records.
* **Output:** `Worksheet` containing validation error information.

##### `build_sheet_warnings()`

* **Input:** Workbook and validation warning records.
* **Output:** `Worksheet` containing validation warning information.

##### `save_report_xlsx()`

* **Input:** Analysis-result dictionary, validation errors, validation warnings, destination folder, and shared base filename.
* **Output:** `Path` pointing to the generated XLSX workbook.

#### Error Handling

The module uses the custom:

`ReportSaveError`

exception for supported file-system failures during report storage.

The following operations explicitly catch `OSError` and convert it into `ReportSaveError`:

* TXT report creation.
* JSON analysis creation.
* Individual CSV file creation.
* XLSX workbook storage.

This provides a consistent application-specific error mechanism for common file-system failures.

Errors that are not represented by `OSError`, including invalid data structures or other library-specific failures, are propagated unless explicitly handled elsewhere in the application.

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

It acts as the orchestration layer between the graphical interface and the specialized modules responsible for file validation, CSV reading, data validation, sales analysis, report generation, and file storage.

The controller receives the source CSV file path and output folder, executes the complete processing workflow, generates all supported output files, measures the total execution time, and returns a structured dictionary containing processing totals, generated file paths, and execution information.

The module currently provides the following function:

* `generate_sales_report()`

#### Controller Workflow

The `generate_sales_report()` function performs the following operations:

1. Starts the execution timer.
2. Validates the source CSV file using `validator.validate_csv_file()`.
3. Reads the validated CSV file using `csv_reader.read_csv_file()`.
4. Normalizes and validates the sales records using `validator.validate_dataframe()`.
5. Analyzes the valid sales records using `analyzer.analyze_sales()`.
6. Generates the complete plain-text sales report using `reporter.generate_report()`.
7. Stores the total number of processed, valid, and invalid rows in the controller result.
8. Generates a shared timestamp-based filename using `file_manager.create_report_base_name()`.
9. Saves the plain-text sales report using `file_manager.save_report()`.
10. Saves the complete structured analysis as a JSON file using `file_manager.save_analysis_json()`.
11. Saves the available analysis summaries as independent CSV files using `file_manager.save_analysis_result_csv_files()`.
12. Generates the complete XLSX workbook using `file_manager.save_report_xlsx()`.
13. Calculates the total execution time.
14. Adds the execution time to the controller result.
15. Returns the complete result dictionary to the caller.

#### Module Coordination

The controller coordinates the following modules:

* `validator`: Validates the source file path, normalizes sales data, validates records, detects warnings, and separates valid and invalid rows.
* `csv_reader`: Reads the validated CSV file and converts its contents into a pandas `DataFrame`.
* `analyzer`: Calculates sales metrics, aggregated summaries, rankings, and optional analyses.
* `reporter`: Converts analysis results, validation errors, and warnings into a structured plain-text sales report.
* `file_manager`: Generates the shared base filename and saves TXT, JSON, CSV, and XLSX output files.

#### Validation Results

The controller receives the validation result produced by:

`validator.validate_dataframe()`

This structure includes:

* Valid sales records.
* Invalid sales records.
* Validation errors.
* Validation warnings.
* Total processed rows.
* Total valid rows.
* Total invalid rows.

The validation result is passed to the analysis workflow.

Validation errors and warnings are also passed to the report-generation and XLSX-generation workflows.

#### Sales Analysis

The controller sends the validation result to:

`analyzer.analyze_sales()`

The resulting analysis structure contains the metrics and aggregated summaries required by the reporting and file-management modules.

These results may include:

* Total processed rows.
* Total valid rows.
* Total invalid rows.
* Total income.
* Total units sold.
* Product summary.
* Category summary.
* Best-selling product.
* Highest-income product.
* Highest-income category.
* Top 5 best-selling products.
* Top 5 highest-income products.
* City summary and highest-income city when `ciudad` is available.
* Payment-method summary and highest-income payment method when `metodo_pago` is available.

#### Report Generation

The controller passes the analysis result, validation errors, validation warnings, and source file path to:

`reporter.generate_report()`

The reporter generates the human-readable plain-text sales report.

The resulting report text is later saved as a TXT file through the file-management module.

#### Output File Coordination

A single shared dynamic base filename is generated during each controller execution.

The same base filename is reused for all files generated during that execution.

The controller generates:

* A TXT sales report.
* A JSON analysis file.
* Product and category CSV summary files.
* An XLSX workbook containing the sales analysis and validation information.

When optional analysis information is available, the CSV export may also generate:

* A city summary CSV file.
* A payment-method summary CSV file.

For example:

`sales_report_2026-08-29_09-30-25-125.txt`

`sales_report_2026-08-29_09-30-25-125.json`

`sales_report_2026-08-29_09-30-25-125.xlsx`

`sales_report_2026-08-29_09-30-25-125_products.csv`

`sales_report_2026-08-29_09-30-25-125_categories.csv`

Optional CSV files:

`sales_report_2026-08-29_09-30-25-125_cities.csv`

`sales_report_2026-08-29_09-30-25-125_payment_methods.csv`

#### XLSX Report Coordination

The controller generates the Excel report using:

`file_manager.save_report_xlsx()`

The function receives:

* The complete `analysis_result`.
* Validation errors.
* Validation warnings.
* The configured output folder.
* The shared base filename.

The resulting workbook path is stored in the controller result as:

`report_path_xlsx`

The workbook may contain general sales metrics, product and category summaries, Top 5 rankings, optional city and payment-method summaries, validation errors, and validation warnings.

#### Controller Result

The `generate_sales_report()` function returns a dictionary containing information about the complete workflow.

The result contains:

* `total_rows`: Total number of processed sales records.
* `total_valid_rows`: Number of records that passed validation.
* `total_invalid_rows`: Number of records containing validation errors.
* `report_path_txt`: `Path` pointing to the generated TXT report.
* `report_path_json`: `Path` pointing to the generated JSON analysis.
* `reports_path_csv`: Dictionary containing the generated CSV summary paths.
* `report_path_xlsx`: `Path` pointing to the generated XLSX workbook.
* `execution_time`: Formatted string containing the total workflow execution time.

#### Controller Result Structure

A simplified controller result follows this structure:

```python
{
    "total_rows": ...,
    "total_valid_rows": ...,
    "total_invalid_rows": ...,
    "report_path_txt": Path(...),
    "report_path_json": Path(...),
    "reports_path_csv": {
        "resumen_producto": Path(...),
        "resumen_categoria": Path(...),
        "ciudad_resumen": Path(...),
        "metodo_de_pago_resumen": Path(...)
    },
    "report_path_xlsx": Path(...),
    "execution_time": "Execution time: 0.0123 seconds"
}
```

The city and payment-method CSV entries are optional.

#### CSV Report Paths

The `reports_path_csv` value contains a nested dictionary identifying each generated CSV summary.

The following entries are always included:

* `resumen_producto`
* `resumen_categoria`

The following entries are included only when the corresponding optional analysis is available:

* `ciudad_resumen`
* `metodo_de_pago_resumen`

An example structure is:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "ciudad_resumen": Path(...),
    "metodo_de_pago_resumen": Path(...)
}
```

The final two entries are optional.

These keys identify the generated CSV reports inside the application.

The physical filenames continue to use the English suffixes:

* `_products.csv`
* `_categories.csv`
* `_cities.csv`
* `_payment_methods.csv`

#### Execution Time

The controller uses:

`time.perf_counter()`

to measure the duration of the complete sales-report generation workflow.

The measurement begins before source-file validation and finishes after all supported output files have been generated.

The execution time therefore includes:

* Source-file validation.
* CSV reading.
* Data normalization and validation.
* Sales analysis.
* Plain-text report generation.
* TXT file storage.
* JSON file storage.
* CSV summary storage.
* XLSX workbook generation and storage.

The result is formatted in seconds with four decimal places.

For example:

`Execution time: 0.0123 seconds`

#### Input and Output

##### `generate_sales_report()`

* **Input:** A string containing the source CSV file path and a string containing the destination output folder.
* **Output:** A dictionary containing processing totals, TXT, JSON, CSV, and XLSX file paths, and the total execution time.

#### Error Propagation

The controller does not directly handle application exceptions.

Errors raised by the validation, CSV reading, analysis, reporting, or file-management modules are propagated to the caller.

Application-specific exceptions derived from `AppError` are handled by the graphical interface.

Unexpected Python exceptions may also propagate to the graphical layer, where they can be presented to the user through the application's error-handling workflow.

#### Responsibilities

The controller is responsible for:

* Coordinating the complete backend workflow.
* Passing information between specialized modules.
* Maintaining the correct processing order.
* Generating a shared base filename.
* Coordinating TXT generation.
* Coordinating JSON generation.
* Coordinating CSV summary generation.
* Coordinating XLSX workbook generation.
* Measuring the total workflow execution time.
* Returning generated-file paths and processing information to the caller.

The controller is not responsible for:

* Implementing CSV parsing logic.
* Performing individual validation rules.
* Calculating sales metrics directly.
* Formatting the plain-text report directly.
* Creating individual TXT, JSON, CSV, or XLSX files directly.
* Displaying graphical interface elements.
* Handling user interaction.

These responsibilities belong to the specialized backend and graphical interface modules.

---

### Graphical User Interface Module

The graphical user interface module provides the main desktop window for the Sales Report application using PySide6.

It allows the user to select a source CSV file, choose an output directory, generate sales reports through the backend controller, inspect generated TXT, JSON, CSV, and XLSX files, and open the configured output directory directly from the application.

TXT, JSON, and CSV files are displayed through dedicated read-only `FileViewerWindow` instances. XLSX files are opened using the operating system's associated application.

The graphical layer separates widget creation, signal connection, layout construction, event handling, and generated-report state management into independent methods.

This structure reduces duplicated interface code and keeps the module modular, maintainable, and easier to extend.

The graphical interface and user-facing messages are displayed in Spanish, while the project source code and technical documentation are maintained in English.

The module currently provides the following class:

* `SalesReportWindow`

#### Main Window

The `SalesReportWindow` class inherits from PySide6 `QMainWindow` and represents the main desktop window of the application.

The window is configured with:

* Title: `Generador de Reportes de Ventas`
* Width: `900`
* Height: `900`
* Default output folder: `reports/`

The main window uses a central `QWidget` and a vertical `QVBoxLayout` to organize the application sections.

#### Window Initialization

During initialization, the class creates the initial application state:

* `file_path`: `None`
* `output_folder`: `reports/`
* `txt_path`: `None`
* `json_path`: `None`
* `csv_paths`: Empty dictionary.
* `xlsx_path`: `None`

The initialization process also:

1. Configures the window title.
2. Configures the fixed window size.
3. Creates the central widget.
4. Creates interface labels through `create_labels()`.
5. Creates interface buttons through `create_buttons()`.
6. Connects button signals through `connect_buttons()`.
7. Creates the main vertical layout.
8. Builds the interface sections.
9. Assigns the completed layout to the central widget.

#### Interface Organization

The graphical interface is organized through several categories of helper methods.

Widget creation:

* `create_labels()`
* `create_buttons()`

Signal configuration:

* `connect_buttons()`

Layout construction:

* `build_selected_file_layout()`
* `build_selected_folder_layout()`
* `build_generate_report_layout()`
* `build_status_layout()`
* `build_generated_files_layout()`

User actions:

* `selected_file_path()`
* `selected_folder_path()`
* `generate_reports()`
* `open_report_txt()`
* `open_report_json()`
* `open_report_csv()`
* `open_report_xlsx()`
* `open_output_folder()`

Interface-state management:

* `on_buttons()`
* `off_buttons()`
* `clean_labels()`
* `clean_paths()`
* `clean_layout()`

#### Label Creation

The `create_labels()` method centralizes creation of the labels used throughout the interface.

It creates labels for:

* Source CSV selection.
* Output-folder information.
* Application status.
* TXT report information.
* JSON analysis information.
* CSV summary information.
* XLSX report information.

Generated TXT, JSON, and XLSX path labels are initially empty and are populated after successful report generation.

Centralizing label creation keeps widget initialization separate from layout construction.

#### Button Creation

The `create_buttons()` method centralizes creation of the application buttons.

The interface currently provides buttons for:

* Selecting the source CSV file.
* Selecting the output directory.
* Generating reports.
* Opening the TXT report.
* Opening the JSON analysis.
* Opening the selected CSV summary.
* Opening the XLSX analysis.
* Opening the output directory.

The method creates the buttons and applies fixed sizes where required.

Signal connections are handled separately by `connect_buttons()`.

#### Button Signal Connections

The `connect_buttons()` method connects each button's `clicked` signal to its corresponding event handler.

The current connections are:

* `button_selected_file` → `selected_file_path()`
* `button_output_folder` → `selected_folder_path()`
* `button_create_report` → `generate_reports()`
* `button_txt_show_report` → `open_report_txt()`
* `button_json_show_report` → `open_report_json()`
* `button_csv_show_report` → `open_report_csv()`
* `button_open_output_folder` → `open_output_folder()`
* `button_xlsx_show_report` → `open_report_xlsx()`

Separating widget creation from signal connection keeps interface initialization easier to understand and maintain.

#### Interface Sections

The main application window contains the following primary sections:

1. Source CSV file selection.
2. Output folder selection.
3. Report generation.
4. Application status.
5. Generated file information and navigation.

Each primary section is created inside an independent `QGroupBox`.

#### Source CSV File Selection

The `build_selected_file_layout()` method creates the section used to select the source CSV file.

The section contains:

* The source-file label.
* The `Seleccionar archivo` button.

The button is connected to:

`selected_file_path()`

#### CSV File Selection Process

The `selected_file_path()` method opens a `QFileDialog` restricted to CSV files.

The dialog uses:

`Archivos CSV (*.csv)`

When a new source file is selected:

1. Generated-report controls are disabled.
2. Previously stored TXT, JSON, CSV, and XLSX paths are cleared.
3. Previously displayed generated-file information is cleared.
4. The selected path is stored in `file_path`.
5. The selected-file label is updated.
6. The application status is updated according to the currently configured output directory.

If the dialog is canceled, the existing application state remains unchanged.

#### Output Folder Selection

The `build_selected_folder_layout()` method creates the section used to configure the destination folder.

The section contains:

* The output-folder label.
* The `Seleccionar carpeta` button.

The button is connected to:

`selected_folder_path()`

The default destination is:

`reports/`

#### Output Folder Selection Process

The `selected_folder_path()` method opens a directory-selection dialog using:

`QFileDialog.getExistingDirectory()`

When a new output folder is selected:

1. Generated-report controls are disabled.
2. Previously stored TXT, JSON, CSV, and XLSX paths are cleared.
3. Previously displayed generated-file information is removed.
4. The selected directory is stored in `output_folder`.
5. The output-folder label is updated.
6. The application status is updated according to whether a source CSV file has already been selected.

If the dialog is canceled, the existing output-folder configuration remains unchanged.

#### Report Generation Section

The `build_generate_report_layout()` method creates the section containing the:

`Crear reporte`

button.

The button is connected to:

`generate_reports()`

The button starts the complete backend workflow through the Sales Report controller.

#### Report Generation Process

The `generate_reports()` method coordinates report generation from the graphical interface.

It performs the following operations:

1. Temporarily disables the report-generation button.
2. Updates the application status to indicate that processing has started.
3. Verifies that a source CSV file has been selected.
4. Stops the process and displays a message when no source file is available.
5. Disables controls associated with previously generated reports.
6. Clears stored TXT, JSON, CSV, and XLSX paths.
7. Clears previously displayed report information.
8. Calls `controller.generate_sales_report()`.
9. Receives the generated report information from the controller.
10. Stores and displays the TXT report path.
11. Stores and displays the JSON analysis path.
12. Stores and displays the XLSX report path.
13. Adds generated CSV summary names to the CSV selector.
14. Creates labels containing generated CSV paths.
15. Stores CSV summary names and paths in `csv_paths`.
16. Updates the application status after successful generation.
17. Enables generated-report controls.
18. Displays application-specific or unexpected errors when necessary.
19. Re-enables the report-generation button after processing.

#### Backend Controller Integration

The GUI delegates the complete backend processing workflow to:

`controller.generate_sales_report()`

The graphical interface provides:

* `file_path`
* `output_folder`

The controller returns processing information and generated output paths.

The GUI currently uses:

* `report_path_txt`
* `report_path_json`
* `reports_path_csv`
* `report_path_xlsx`

The backend remains responsible for validation, reading, analysis, report generation, and file storage.

#### Application Status

The `build_status_layout()` method creates the interface status section.

The initial message is:

`Seleccione un archivo CSV para comenzar.`

The status can change when:

* A CSV file is selected.
* An output folder is selected.
* Both input and output selections are configured.
* Report generation starts.
* No CSV file has been selected.
* Report generation completes successfully.
* An application-specific error occurs.
* An unexpected error occurs.

#### Generated Files Section

The `build_generated_files_layout()` method creates the section used to display and access generated report files.

The section provides controls for:

* TXT reports.
* JSON analysis.
* XLSX analysis.
* CSV summaries.
* Output-directory access.

Generated-report controls are initially disabled through:

`off_buttons()`

They become available after successful report generation through:

`on_buttons()`

#### TXT Report Access

The generated TXT path is stored in:

`txt_path`

and displayed through:

`txt_file_path_label`

The:

`Reporte TXT`

button calls:

`open_report_txt()`

This creates a `FileViewerWindow` and displays the generated TXT report in read-only mode.

#### JSON Analysis Access

The generated JSON path is stored in:

`json_path`

and displayed through:

`json_file_path_label`

The:

`Análisis JSON`

button calls:

`open_report_json()`

This creates a `FileViewerWindow` and displays the JSON analysis in read-only mode.

#### CSV Summary Selection and Access

Generated CSV summary paths are stored in:

`csv_paths`

Generated summary names are also added to:

`csv_combobox`

The:

`Ver resumen CSV`

button calls:

`open_report_csv()`

The method reads the currently selected summary name, obtains its corresponding path from `csv_paths`, and creates a `FileViewerWindow` to display the CSV contents.

#### Scrollable CSV Results

Generated CSV paths are also displayed inside a `QScrollArea`.

The scrollable area contains:

`csv_summaries_layout`

Each generated CSV path is represented by an independent `QLabel`.

The scroll area is configured with a fixed height of:

`150`

pixels.

This allows multiple CSV summary paths to be displayed without increasing the size of the main window.

#### XLSX Report Access

The generated Excel workbook path is stored in:

`xlsx_path`

and displayed through the XLSX path label.

The:

`Análisis Excel`

button calls:

`open_report_xlsx()`

Unlike TXT, JSON, and CSV reports, XLSX files are not displayed through `FileViewerWindow`.

The method first verifies that the generated file exists.

If the file cannot be found, the interface displays a warning message:

`Archivo no encontrado`

If the file exists, the local path is converted into a `QUrl` and opened through:

`QDesktopServices.openUrl()`

This allows the operating system to open the workbook using the application associated with XLSX files.

#### Output Folder Access

The:

`Abrir carpeta de salida`

button calls:

`open_output_folder()`

The method converts the configured output folder into an absolute path and opens it through the operating-system file manager.

The platform-specific mechanisms are:

* Windows: `os.startfile()`
* macOS: `open`
* Linux and compatible systems: `xdg-open`

#### Generated-Report Control Management

The GUI centralizes enabling and disabling generated-report controls.

##### `on_buttons()`

Enables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.

This method is called after successful report generation.

##### `off_buttons()`

Disables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.

This method is used when:

* A new source CSV is selected.
* A new output folder is selected.
* A new report-generation process begins.
* Previously generated results should no longer be treated as current.

#### Generated-Report State Cleanup

The GUI also separates internal path cleanup from visual cleanup.

##### `clean_paths()`

Resets internal generated-file references:

* `txt_path` → `None`
* `json_path` → `None`
* `csv_paths` → `{}`
* `xlsx_path` → `None`

This prevents previously generated reports from remaining associated with a new source file, output directory, or report-generation process.

##### `clean_labels()`

Clears generated-file information displayed in the interface.

It:

* Clears the TXT path label.
* Clears the JSON path label.
* Clears the XLSX path label.
* Clears the CSV selector.
* Removes dynamically generated CSV path labels.

##### `clean_layout()`

Removes dynamically generated widgets from a provided Qt layout.

The method iterates through the layout in reverse order and schedules each contained widget for deletion.

It is primarily used to clear CSV summary labels before new results are displayed.

#### Window State

The `SalesReportWindow` class maintains the following primary state values:

* `file_path`: Selected source CSV path.
* `output_folder`: Destination directory. Defaults to `reports/`.
* `txt_path`: Generated TXT report path.
* `json_path`: Generated JSON analysis path.
* `csv_paths`: Mapping between CSV summary names and their generated paths.
* `xlsx_path`: Generated XLSX workbook path.

The class also maintains interface widgets, layouts, buttons, selectors, and report-viewer window references.

#### PySide6 Components

The graphical interface currently uses:

* `QMainWindow`: Main desktop window.
* `QWidget`: Central window and internal containers.
* `QPushButton`: Interactive application controls.
* `QVBoxLayout`: Vertical organization.
* `QHBoxLayout`: Horizontal CSV selection controls.
* `QLabel`: Paths, titles, and status information.
* `QGroupBox`: Visual grouping of interface sections.
* `QFileDialog`: Source-file and output-directory selection.
* `QScrollArea`: Scrollable CSV path display.
* `QComboBox`: CSV summary selection.
* `QMessageBox`: Critical and warning messages.
* `QDesktopServices`: Opening generated XLSX files through the operating system.
* `QUrl`: Conversion of local XLSX paths for `QDesktopServices`.

#### Current GUI Workflow

The current graphical workflow is:

1. Launch `SalesReportWindow`.
2. Select a source CSV file.
3. Optionally select a custom output directory.
4. Use `reports/` when no custom directory is selected.
5. Press `Crear reporte`.
6. Verify that a source CSV file exists in the interface state.
7. Disable previous report controls.
8. Clear previous generated-file state.
9. Send the source CSV and output folder to `controller.generate_sales_report()`.
10. Execute the complete backend workflow.
11. Receive TXT, JSON, CSV, and XLSX output paths.
12. Display the generated TXT path.
13. Display the generated JSON path.
14. Display the generated XLSX path.
15. Populate the CSV selector.
16. Display CSV paths in the scrollable area.
17. Enable generated-report controls.
18. Allow TXT, JSON, and CSV reports to be inspected through `FileViewerWindow`.
19. Allow the XLSX workbook to be opened with the operating system's associated application.
20. Allow the output folder to be opened.
21. Display the final success status or an error message.

#### Error Handling

The graphical interface handles:

* Application-specific exceptions derived from `AppError`.
* Unexpected Python exceptions.

During report generation, errors update the status to:

`Error en el proceso`

and are displayed through a critical `QMessageBox`.

The `open_report_xlsx()` method also handles a missing generated Excel file by displaying a warning message box.

The graphical application remains open after handled errors so the user can correct the configuration or try again.

#### Input and Output

##### `SalesReportWindow`

* **Input:** User interaction through the graphical interface.
* **Output:** Main desktop interface for configuring, generating, displaying, and accessing sales-report outputs.

##### `create_labels()`

* **Input:** None.
* **Output:** Creates the labels required by the main interface.

##### `create_buttons()`

* **Input:** None.
* **Output:** Creates the buttons required by the main interface.

##### `connect_buttons()`

* **Input:** None.
* **Output:** Connects button signals to their corresponding event handlers.

##### `selected_file_path()`

* **Input:** CSV file selected through `QFileDialog`.
* **Output:** Updates the source-file state and resets previous generated-report state.

##### `selected_folder_path()`

* **Input:** Directory selected through `QFileDialog`.
* **Output:** Updates the output-folder state and resets previous generated-report state.

##### `generate_reports()`

* **Input:** Selected CSV path and configured output directory.
* **Output:** Generates reports through the controller and updates the GUI with TXT, JSON, CSV, and XLSX results.

##### `open_report_txt()`

* **Input:** Generated TXT path.
* **Output:** Opens the TXT report in a `FileViewerWindow`.

##### `open_report_json()`

* **Input:** Generated JSON path.
* **Output:** Opens the JSON analysis in a `FileViewerWindow`.

##### `open_report_csv()`

* **Input:** CSV summary selected through `csv_combobox`.
* **Output:** Opens the selected CSV summary in a `FileViewerWindow`.

##### `open_report_xlsx()`

* **Input:** Generated XLSX path stored in `xlsx_path`.
* **Output:** Opens the workbook using the operating system's associated application or displays a warning if the file does not exist.

##### `open_output_folder()`

* **Input:** Configured output directory.
* **Output:** Opens the directory using the operating-system file manager.

##### `clean_layout()`

* **Input:** Qt layout containing dynamically generated widgets.
* **Output:** Removes its dynamically generated widgets.

##### `clean_labels()`

* **Input:** None.
* **Output:** Clears TXT, JSON, CSV, and XLSX information displayed in the interface.

##### `clean_paths()`

* **Input:** None.
* **Output:** Resets stored TXT, JSON, CSV, and XLSX paths.

##### `on_buttons()`

* **Input:** None.
* **Output:** Enables controls associated with generated reports.

##### `off_buttons()`

* **Input:** None.
* **Output:** Disables controls associated with generated reports.

#### Current Development Status

The graphical interface is fully connected to the Sales Report backend workflow.

Currently available:

* Main PySide6 desktop window.
* Source CSV selection.
* Output-folder selection.
* Default output directory.
* Application status messages.
* Backend controller integration.
* TXT report generation and access.
* JSON analysis generation and access.
* CSV summary generation and selection.
* Scrollable CSV results.
* XLSX report generation and access.
* Read-only TXT, JSON, and CSV viewer integration.
* Operating-system XLSX opening.
* Output-directory access.
* Centralized label creation.
* Centralized button creation.
* Centralized signal connection.
* Generated-report state cleanup.
* Generated-report control management.
* Application-specific error presentation.
* Unexpected error presentation.
* Missing-XLSX warning presentation.

---

### Graphical Application Entry Point Module

The graphical application entry point module initializes and launches the PySide6 desktop application.

It provides a dedicated `main()` function responsible for creating the Qt application environment, initializing the main Sales Report window, displaying the graphical interface, starting the Qt event loop, and returning the final application exit status to the operating system.

Unlike the graphical user interface module, this module does not define interface layouts, controls, or backend processing logic. Its responsibility is to initialize and run the desktop application.

#### Main Function

The module currently provides the following function:

* `main()`

The `main()` function coordinates the graphical application startup process.

It creates the `QApplication` instance, initializes `SalesReportWindow`, displays the main window, and starts the Qt event loop.

#### Application Initialization

The `main()` function creates a `QApplication` instance using:

`QApplication(sys.argv)`

The `QApplication` object manages the graphical application environment and receives command-line arguments provided when the program is executed.

#### Main Window Initialization

The main application window is created using:

`main_window.SalesReportWindow()`

The graphical window module is imported from:

`src.gui.main_window`

The `SalesReportWindow` class provides the main desktop interface.

This keeps application startup logic separated from the graphical interface implementation and backend processing workflow.

#### Window Display

After the main window is created, the application calls:

`window.show()`

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

#### Application Entry Point

The module uses the standard Python application entry-point pattern:

```python
if __name__ == "__main__":
    main()
```

This ensures that the graphical application starts when the module is executed directly.

The startup logic itself remains contained inside `main()` instead of being executed directly at module level.

#### Application Startup Workflow

The graphical application starts using the following process:

1. Imports the Python `sys` module.
2. Imports `QApplication` from PySide6.
3. Imports `main_window` from `src.gui`.
4. Reaches the `if __name__ == "__main__":` application entry point.
5. Calls `main()`.
6. Creates the `QApplication` instance.
7. Creates an instance of `SalesReportWindow`.
8. Displays the main application window.
9. Starts the Qt event loop.
10. Processes graphical user interactions while the application remains open.
11. Returns the Qt exit status to the operating system when the application closes.

#### Module Coordination

The graphical application entry point interacts directly with:

* `PySide6.QtWidgets.QApplication`: Creates and manages the Qt application environment.
* `src.gui.main_window`: Provides the `SalesReportWindow` graphical interface.

The entry point does not interact directly with the sales-report backend modules.

Backend processing is initiated through `SalesReportWindow`, which communicates with the Sales Report controller when the user starts the report-generation process.

#### Input and Output

##### `main()`

* **Input:** Command-line arguments received through `sys.argv`.
* **Output:** Launches the PySide6 desktop application and passes the final Qt exit status to the operating system through `sys.exit()`.

Subsequent application input is provided through user interaction with `SalesReportWindow`.

#### Responsibilities

This module is responsible for:

* Providing the graphical application `main()` function.
* Creating the Qt application environment.
* Creating the main Sales Report window.
* Displaying the graphical interface.
* Starting the Qt event loop.
* Keeping the graphical application active while events are processed.
* Passing the final Qt exit status to the operating system.
* Providing the direct execution entry point for the desktop application.

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

→ `main()`

→ `QApplication`

→ `src.gui.main_window.SalesReportWindow`

→ Graphical user interaction

→ `controller.generate_sales_report()`

→ Sales Report backend workflow

The application entry point only initializes and runs the graphical environment.

The communication with the backend controller is performed by the `SalesReportWindow` graphical interface.

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
* `file_path`: Path of the report file to read and display.

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

`Path(self.file_path).read_text(encoding="utf-8")`

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

* **Input:** The report path stored in `file_path`.
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
