# Sales Report

> **Project Status:** Version **3.0.3 completed** — Functional desktop application with PySide6, multi-format report export, monthly analysis, and automatic chart generation. This project has been manually tested with sample sales CSV files.

Sales Report is a modular Python desktop application for validating sales data, analyzing valid records, generating structured reports, exporting analysis results in multiple formats, and producing automatic sales charts.

The application includes a PySide6 graphical interface that allows users to select a source CSV file, choose an output directory, generate reports and charts, inspect generated TXT, JSON, and CSV files, open XLSX reports, open generated PNG charts, and access the output directory directly from the application.

The application interface and user-facing messages are displayed in Spanish, while the project source code and technical documentation are maintained in English.

---

## Project Architecture (Current State)

The project follows a modular architecture in which each module is responsible for a specific part of the application workflow.

The application separates graphical presentation, workflow orchestration, validation, CSV reading, sales analysis, report formatting, file management, chart generation, and custom error handling.

The current application relationship can be represented as:

```text
Graphical Application Entry Point
        ↓
SalesReportWindow
        ↓
controller.generate_sales_report()
        ↓
validator
        ↓
csv_reader
        ↓
validator.validate_dataframe()
        ↓
analyzer
        ↓
reporter
        ↓
├── file_manager
│   ├── TXT
│   ├── JSON
│   ├── CSV
│   └── XLSX
│
└── chart_manager
    └── PNG charts
        ↓
Controller Result
        ↓
SalesReportWindow
```

Generated TXT, JSON, and CSV files can be inspected through:

`FileViewerWindow`

Generated XLSX reports and PNG charts are opened using the operating system's associated applications.

The main modules include:

* `controller`: Coordinates the complete sales-report and chart-generation workflow.
* `validator`: Validates the source file, normalizes records, validates sales data, detects warnings, and separates valid and invalid rows.
* `csv_reader`: Reads the validated CSV file into a pandas `DataFrame`.
* `analyzer`: Calculates general metrics, aggregated summaries, rankings, monthly growth, and monthly performance results.
* `reporter`: Generates the structured human-readable plain-text sales report.
* `file_manager`: Saves TXT, JSON, CSV, and XLSX output files.
* `chart_manager`: Generates PNG chart images from sales-analysis results.
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

The application uses libraries including:

* `PySide6`
* `pandas`
* `numpy`
* `openpyxl`
* `matplotlib`

The complete dependency list is maintained in:

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

These columns are not required for the core validation workflow.

When present, they are normalized and used to generate additional analysis summaries, report sections, exported files, and charts.

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
4. Start the complete report-generation process.
5. View the current application status.
6. View generated TXT, JSON, XLSX, and CSV paths.
7. Select generated CSV summaries from a combo box.
8. Open TXT, JSON, and CSV files through read-only viewer windows.
9. Open the generated XLSX workbook through the operating system.
10. Select generated charts from a combo box.
11. Open generated PNG charts through the operating system.
12. Open the configured output directory.

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
9. Verifies that valid records are available for analysis.
10. Calculates row-level income.
11. Calculates total income and total units sold.
12. Generates the product summary.
13. Generates the category summary.
14. Generates the monthly summary.
15. Calculates monthly income growth.
16. Calculates monthly income percentage growth.
17. Calculates monthly unit-sales growth.
18. Calculates monthly unit-sales percentage growth.
19. Determines overall highest-performing records.
20. Generates Top 5 product rankings.
21. Determines the best-selling product or tied products for each month.
22. Determines the highest-income category or tied categories for each month.
23. Generates city analysis when `ciudad` is available.
24. Generates payment-method analysis when `metodo_pago` is available.
25. Generates the structured plain-text report.
26. Creates a shared base filename using the source CSV filename and current timestamp.
27. Saves the plain-text report as TXT.
28. Saves the complete structured analysis as JSON.
29. Saves five standard CSV analysis summaries.
30. Saves optional city and payment-method CSV summaries when available.
31. Generates the XLSX workbook.
32. Generates ten standard PNG charts.
33. Generates optional city and payment-method charts when available.
34. Calculates total execution time.
35. Returns processing results and generated output paths to the graphical interface.
36. Displays generated file and chart paths.
37. Enables controls used to inspect generated outputs.

---

## Generated Output Files

Generated outputs are stored in the selected output directory.

If no custom directory is selected, the default directory is:

```text
reports/
```

If the destination directory does not exist, the application creates it when necessary.

All files generated during the same execution share a base filename containing:

* The original source CSV filename without its extension.
* The current local date.
* The current local time.
* Milliseconds.

The base filename follows this format:

```text
<source_filename>_YYYY-MM-DD_HH-MM-SS-fff
```

For example, when the source file is:

```text
ventas_agosto.csv
```

a generated base filename may be:

```text
ventas_agosto_2026-09-19_07-45-30-125
```

A normal execution generates TXT, JSON, XLSX, CSV, and PNG files that reuse this base filename.

Each execution generates a new timestamp, allowing outputs from different processing runs to coexist independently.

---

## Generated TXT Report

The TXT file contains the human-readable sales report.

Depending on the available data, it includes:

* General sales summary.
* Total processed rows.
* Valid and invalid row totals.
* Total income.
* Total units sold.
* Best-selling product or tied products.
* Highest-income product or tied products.
* Highest-income category or tied categories.
* Highest-income city when available.
* Highest-income payment method when available.
* Top 5 best-selling products.
* Top 5 highest-income products.
* Product summary.
* Category summary.
* City summary when available.
* Payment-method summary when available.
* Monthly sales summary.
* Monthly income variation.
* Monthly income percentage variation.
* Monthly unit-sales variation.
* Monthly unit-sales percentage variation.
* Best-selling product or tied products for each month.
* Highest-income category or tied categories for each month.
* Validation errors.
* Validation warnings.

Monthly growth values that cannot be calculated, such as those for the first available month, are displayed as:

`N/D`

The report is saved using UTF-8 encoding.

---

## Generated JSON Analysis

The JSON file contains the complete structured sales-analysis result.

Before serialization, pandas DataFrames are converted into lists of dictionaries.

The following analysis DataFrames are always converted:

* `product_summary`
* `category_summary`
* `monthly_summary`
* `monthly_best_selling_product`
* `monthly_highest_income_category`

The following are included when available:

* `city_summary`
* `payment_method_summary`

pandas `NaN` values are replaced with Python `None` before serialization so missing values are represented as:

`null`

inside JSON.

The file is written using:

* UTF-8 encoding.
* Formatted indentation.
* `ensure_ascii=False`.

---

## Generated CSV Summaries

The application generates five standard CSV analysis files.

The standard summaries are:

* Product summary.
* Category summary.
* Monthly summary.
* Monthly best-selling products.
* Monthly highest-income categories.

The CSV-path dictionary uses the following keys:

```text
resumen_producto
resumen_categoria
resumen_mensual
resumen_mejores_vendidos_por_mes
resumen_categoria_mayor_ingreso_por_mes
```

When optional data is available, the application may also generate:

```text
ciudad_resumen
metodo_de_pago_resumen
```

The physical filename suffixes are:

```text
_productos.csv
_categorias.csv
_meses.csv
_producto_top_mensual.csv
_categoria_top_ingreso_mensual.csv
_ciudades.csv
_metodos_pago.csv
```

The city and payment-method CSV files are optional.

---

## Generated XLSX Workbook

The application generates a structured Excel workbook using `openpyxl`.

The workbook always contains:

* `Resumen General`
* `Productos`
* `Categorías`
* `Resumen por mes`
* `Productos mejor vendidos`
* `Productos con mejor Ingreso`
* `Producto más vendido por mes`
* `Categoría mayor ingreso por mes`
* `Validación de errores`
* `Advertencias`

When optional analyses are available, the workbook can also contain:

* `Resumen por ciudad`
* `Resumen por método de pago`

The default worksheet created by openpyxl is removed before the report worksheets are created.

Most DataFrame-based worksheets are generated through a reusable worksheet-building helper.

The XLSX file is opened from the graphical interface through the operating system's associated application.

---

## Generated PNG Charts

Version 3.0.3 includes automatic chart generation through:

`chart_manager`

All charts are generated as bar charts using pandas and Matplotlib.

Generated images use:

* PNG format.
* 150 DPI.
* Custom titles.
* Custom axis labels.
* 90-degree x-axis label rotation.
* Automatic layout adjustment through `tight_layout()`.

The standard workflow generates ten charts.

### Standard Charts

The standard chart identifiers are:

```text
grafica_de_ingresos_mensuales
grafica_de_unidades_vendidas_mensualmente
grafica_crecimiento_porcentaje_mensual
grafica_crecimiento_porcentaje_unidades
grafica_producto_top_mensual
grafica_categoria_top_ingreso
grafica_producto_top_ingreso
grafica_unidades_producto_top
grafica_ingreso_categoria
grafica_unidades_categoria
```

These charts represent:

* Monthly income.
* Monthly units sold.
* Monthly income percentage variation.
* Monthly unit-sales percentage variation.
* Best-selling products by month.
* Highest-income categories by month.
* Top 5 highest-income products.
* Top 5 products by units sold.
* Income by category.
* Units sold by category.

### Optional City Charts

When `city_summary` is available and contains data, the application also generates:

```text
grafica_ingreso_ciudad
grafica_unidades_ciudad
```

These represent:

* Income by city.
* Units sold by city.

### Optional Payment-Method Charts

When `payment_method_summary` is available and contains data, the application also generates:

```text
grafica_ingreso_metodo_pago
grafica_unidades_metodo_pago
```

These represent:

* Income by payment method.
* Units sold by payment method.

The application therefore generates:

* 10 charts without optional analysis.
* 12 charts when either city or payment-method analysis is available.
* 14 charts when both optional analyses are available.

Generated PNG paths are returned by the controller under:

`reports_path_charts`

---

## Graphical Report and Chart Access

After a successful processing workflow, the graphical interface displays the generated output information.

TXT, JSON, and CSV files are displayed through independent read-only:

`FileViewerWindow`

instances.

The viewer reads text-based report files using UTF-8 encoding without modifying their contents.

CSV summaries can be selected through:

`csv_combobox`

Generated CSV paths are displayed inside a scrollable area.

The XLSX workbook is opened through:

`QDesktopServices`

using the operating system's associated application.

Generated chart names are added to:

`chart_combobox`

Their paths are stored in:

`charts_paths`

The selected PNG chart is also opened through:

`QDesktopServices`

using the operating system's associated application.

The graphical interface additionally provides direct access to the configured output directory.

---

## Analysis Features

The analysis module provides the data structures used by reports, exported files, and generated charts.

Current analysis functionality includes:

* Row-level income calculation.
* Total income.
* Total units sold.
* Product aggregation.
* Category aggregation.
* Optional city aggregation.
* Optional payment-method aggregation.
* Maximum-value record detection with tie preservation.
* Generic Top 5 product ranking.
* Monthly sales aggregation.
* Absolute monthly income growth.
* Percentage monthly income growth.
* Absolute monthly unit-sales growth.
* Percentage monthly unit-sales growth.
* Monthly best-selling-product identification.
* Monthly highest-income-category identification.

The analysis module calculates these values before they are passed to presentation and export modules.

---

## Monthly Analysis

The monthly summary contains:

```text
mes
filas_validas
unidades_vendidas
ingreso_total
crecimiento_ingreso
crecimiento_ingreso_porcentaje
crecimiento_unidades
crecimiento_unidades_porcentaje
```

Monthly records are sorted chronologically.

Growth values compare each month against the immediately preceding month.

The application also generates two additional monthly analysis structures:

`monthly_best_selling_product`

and:

`monthly_highest_income_category`

These structures preserve ties when more than one product or category shares the corresponding monthly maximum.

---

## Application Status and Errors

The graphical interface provides status messages throughout the application workflow.

The status area informs the user about events such as:

* CSV file selection.
* Output-folder selection.
* Start of processing.
* Missing source-file selection.
* Successful report and chart generation.
* Processing errors.

Application-specific exceptions inherit from:

`AppError`

Expected application errors use Spanish default messages because they are intended to be displayed directly to users.

The custom exception hierarchy currently covers:

* File-path validation failures.
* CSV file-reading failures.
* CSV structure failures.
* Data-validation failures.
* Absence of valid sales rows.
* Report-generation failures.
* Report-storage failures.
* Chart-generation and chart-storage failures.

Chart-specific generation failures use:

`ChartGenerationError`

When an application-specific or unexpected exception occurs during the generation workflow, the graphical interface updates the application status and displays the corresponding error through a critical message box.

The graphical application remains open so the user can correct the problem and try again.

---

## Version 3.0.3

Version **3.0.3** represents the current completed state of the Sales Report application.

This version includes:

* PySide6 graphical desktop interface.
* Modular backend architecture.
* CSV source-file validation.
* Data normalization and record validation.
* Validation errors and non-critical warnings.
* General sales metrics.
* Product and category summaries.
* Optional city and payment-method analysis.
* Generic Top 5 ranking logic.
* Monthly sales analysis.
* Monthly income and unit-sales growth.
* Monthly percentage growth.
* Monthly best-selling products.
* Monthly highest-income categories.
* Human-readable TXT reporting.
* Structured JSON export.
* Five standard CSV exports.
* Optional city and payment-method CSV exports.
* Multi-sheet XLSX workbook generation.
* Automatic PNG chart generation.
* Ten standard charts.
* Four optional charts.
* Read-only TXT, JSON, and CSV viewing.
* Operating-system XLSX opening.
* Operating-system PNG opening.
* Dynamic source-based filenames.
* Custom application-specific exception hierarchy.
* Dedicated `ChartGenerationError`.
* Output-directory access from the graphical interface.
* Cross-platform output-folder opening.
* Execution-time measurement.

The project remains organized so validation, analysis, presentation, storage, chart generation, graphical interaction, and workflow orchestration are handled by independent modules.

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

Its purpose is to make expected application failures easier to identify, propagate, handle, and present consistently across the backend and graphical interface.

All custom exceptions inherit from `AppError`, which acts as the common base class for application-specific errors.

The default exception messages are written in Spanish because they are intended to be displayed directly to users through the graphical interface.

The module currently covers errors related to:

* Empty, missing, or invalid file paths.
* Unsupported file extensions.
* Empty or unreadable CSV files.
* Missing or invalid CSV headers.
* Missing required columns.
* Invalid CSV structures.
* Empty or unusable DataFrames.
* Data-validation failures.
* Absence of valid rows for analysis.
* Report-generation failures.
* Report-file storage failures.
* Chart-generation or chart-storage failures.

#### Base Exception

`AppError` is the base class for all application-specific exceptions.

It stores the error message received during initialization in:

`message`

and passes that message to Python's built-in `Exception` class.

Its `__str__()` implementation returns the stored message directly.

This allows the application to handle all expected project-specific errors through a common exception type while preserving specialized subclasses for individual failure conditions.

#### User-Facing Error Messages

Each specialized exception provides a default error message in Spanish.

These messages are designed to be presented directly to the user when an expected application error occurs.

Examples include:

`La ruta del archivo está vacía.`

`La ruta del archivo no existe.`

`La extensión del archivo no es compatible.`

`El archivo no se pudo leer correctamente.`

`No hay filas válidas disponibles para el análisis.`

`No se pudo guardar el archivo del reporte.`

`No se pudo generar la gráfica.`

A custom message may also be provided when creating an exception, replacing its default message.

#### Exception Hierarchy

The current application-specific exception hierarchy is:

* `AppError`: Base class for all application-specific exceptions.
* `EmptyPathError`: Raised when the provided file path is empty.
* `FileNotFoundAppError`: Raised when the provided file path does not exist.
* `InvalidFilePathError`: Raised when the provided path does not point to a valid file.
* `InvalidFileExtensionError`: Raised when the file extension is not supported.
* `EmptyFileError`: Raised when the CSV file exists but contains zero bytes.
* `FileReadError`: Raised when the CSV file cannot be read correctly.
* `MissingColumnsError`: Raised when the CSV file does not contain all required columns.
* `EmptyHeadersError`: Raised when the CSV file has no valid headers.
* `InvalidCSVStructureError`: Raised when the CSV structure is invalid.
* `EmptyDataFrameError`: Raised when the DataFrame contains no rows or usable data.
* `DataValidationError`: Raised when the DataFrame-validation process fails.
* `NoValidRowsError`: Raised when no valid rows are available for sales analysis.
* `ReportGenerationError`: Raised when the plain-text report cannot be generated.
* `ReportSaveError`: Raised when a generated report file cannot be saved.
* `ChartGenerationError`: Raised when a chart image cannot be generated or saved.

#### Exception Categories

The custom exceptions can be grouped according to their primary responsibility.

##### File and Path Validation

The following exceptions are related to source-file validation:

* `EmptyPathError`
* `FileNotFoundAppError`
* `InvalidFilePathError`
* `InvalidFileExtensionError`
* `EmptyFileError`
* `FileReadError`

##### CSV Structure and Data Validation

The following exceptions represent CSV-structure or DataFrame-validation failures:

* `MissingColumnsError`
* `EmptyHeadersError`
* `InvalidCSVStructureError`
* `EmptyDataFrameError`
* `DataValidationError`

##### Sales Analysis

The analysis layer uses:

* `NoValidRowsError`

This exception prevents sales-analysis operations from continuing when no valid records are available.

##### Report Generation and Storage

Report-related failures can be represented by:

* `ReportGenerationError`
* `ReportSaveError`

`ReportGenerationError` represents failures while producing the human-readable report content.

`ReportSaveError` represents failures while storing generated report files such as TXT, JSON, CSV, or XLSX outputs.

##### Chart Generation and Storage

Chart-related failures are represented by:

* `ChartGenerationError`

This exception is used when a chart image cannot be generated or saved successfully.

Chart errors remain separate from `ReportSaveError`, allowing the application to distinguish report-file failures from chart-generation failures.

#### Error Propagation

Specialized backend modules raise application-specific exceptions when an expected failure occurs.

These exceptions can propagate through the controller until they reach the graphical interface.

Because all custom exceptions inherit from:

`AppError`

the GUI can handle expected project errors through a common exception block.

The general propagation model is:

`Specialized backend module`

→ `AppError` subclass

→ `Controller`

→ `Graphical interface`

→ User-facing message

The controller does not need to convert every specialized exception into another type because the shared `AppError` hierarchy already provides a consistent application-level contract.

#### Graphical Interface Integration

The main graphical interface catches application-specific exceptions using:

```python
except AppError as error:
```

When an `AppError` occurs during report or chart generation, the GUI can display its Spanish error message directly to the user.

This keeps backend exception detection separate from graphical error presentation.

The graphical interface remains responsible for deciding how the error is presented, such as through:

* Status messages.
* Critical `QMessageBox` dialogs.
* Warning dialogs when handled directly by graphical operations.

#### Custom Error Messages

Each specialized exception accepts an optional:

`message`

argument.

When no custom message is supplied, the exception uses its predefined Spanish message.

For example:

```python
raise ChartGenerationError()
```

uses:

`No se pudo generar la gráfica.`

A custom message can also be provided when additional context is required:

```python
raise ChartGenerationError("No se pudo guardar la gráfica mensual.")
```

The exception type remains unchanged while the displayed information becomes more specific.

#### Common Exception Contract

All specialized exceptions follow the same basic structure:

1. Inherit from `AppError`.
2. Accept an optional `message` argument.
3. Provide a predefined Spanish message by default.
4. Pass the selected message to `AppError`.
5. Can be handled through the common `AppError` type.

This shared structure keeps error handling predictable across the project.

#### Current Exception Structure

The application-specific hierarchy can be represented as:

```text
AppError
├── EmptyPathError
├── FileNotFoundAppError
├── InvalidFilePathError
├── InvalidFileExtensionError
├── EmptyFileError
├── FileReadError
├── MissingColumnsError
├── EmptyHeadersError
├── InvalidCSVStructureError
├── EmptyDataFrameError
├── DataValidationError
├── NoValidRowsError
├── ReportGenerationError
├── ReportSaveError
└── ChartGenerationError
```

#### Input and Output

##### `AppError`

* **Input:** Error message as a string.
* **Output:** Application-specific exception object whose string representation returns the supplied message.

##### Specialized Exceptions

* **Input:** Optional custom error message.
* **Output:** Specialized `AppError` subclass representing a specific expected application failure.

When no custom message is supplied, the predefined Spanish message is used.

#### Responsibilities

This module is responsible for:

* Defining the common `AppError` base exception.
* Defining specialized exceptions for expected application failures.
* Providing default user-facing messages in Spanish.
* Maintaining a common exception hierarchy across the project.
* Supporting consistent exception propagation.
* Allowing custom messages when additional error context is required.
* Representing report-generation and report-storage failures.
* Representing chart-generation and chart-storage failures.

This module is not responsible for:

* Detecting every error condition directly.
* Displaying graphical error dialogs.
* Logging errors.
* Recovering automatically from failed operations.
* Validating source files directly.
* Generating reports.
* Generating charts.

Those responsibilities belong to the modules that detect, raise, catch, or present the corresponding exceptions.

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

The sales analysis module processes previously validated sales records and calculates the main metrics, aggregated summaries, rankings, monthly performance indicators, and optional analyses required by the rest of the application.

Each analysis operation is implemented in an independent helper function. This modular structure keeps the analysis workflow easier to maintain, test, understand, reuse, and extend without modifying the complete analysis process.

The module calculates general sales metrics, product and category summaries, monthly sales summaries, Top 5 product rankings, maximum-value records, monthly growth indicators, monthly best-selling products, monthly highest-income categories, and optional city and payment-method analyses.

The resulting structures are used by report generation, file export, and chart-generation components.

The module currently provides the following functions:

* `create_income_column()`
* `get_total_income()`
* `get_total_units_sold()`
* `get_product_summary()`
* `get_category_summary()`
* `get_city_summary()`
* `get_payment_method_summary()`
* `get_records_with_max_value()`
* `get_top_5()`
* `get_income_growth_units()`
* `get_income_percentage_growth()`
* `get_monthly_summary()`
* `get_monthly_best_selling_product()`
* `get_monthly_highest_income_category()`
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

The final product summary is sorted from highest to lowest:

`ingreso_total`

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

The final category summary is sorted from highest to lowest:

`ingreso_total`

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

City analysis is optional and is performed only when the `ciudad` column is present.

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

Payment-method analysis is optional and is performed only when the `metodo_pago` column is present.

#### Maximum-Value Records

The `get_records_with_max_value()` function identifies every record containing the maximum value in a specified numeric column.

The function determines the maximum value and preserves all records tied for that value.

The selected records are returned as a list of dictionaries.

This reusable function is used to determine:

* The product or products with the highest number of units sold.
* The product or products with the highest total income.
* The category or categories with the highest total income.
* The city or cities with the highest total income when city data is available.
* The payment method or payment methods with the highest total income when payment-method data is available.

If multiple records share the maximum value, all tied records are preserved.

#### Generic Top 5 Ranking

The `get_top_5()` function generates reusable Top 5 product rankings.

It receives:

* A product-summary DataFrame.
* A column name or list of column names used for sorting.
* A Boolean value or list of Boolean values defining the sort direction.

The function:

1. Sorts the product summary according to the supplied criteria.
2. Selects the first five rows.
3. Resets the resulting index.
4. Converts the selected records into a list of dictionaries.

This generic implementation is used to generate different product rankings without duplicating sorting logic.

#### Top 5 Best-Selling Products

The best-selling ranking is generated through:

`get_top_5()`

using:

* `unidades_vendidas` in descending order.
* `ingreso_total` in descending order as a secondary sorting criterion.

The result is stored in:

`top_5_best_selling_products`

and contains up to five product records.

#### Top 5 Highest-Income Products

The highest-income ranking is also generated through:

`get_top_5()`

using:

`ingreso_total`

in descending order.

The result is stored in:

`top_5_highest_income_products`

and contains up to five product records.

#### Absolute Growth Calculation

The `get_income_growth_units()` function calculates the absolute difference between consecutive values in a numeric column.

The operation follows the general form:

`current_value - previous_value`

The calculated values are stored in a new column whose name is provided to the function.

The first row contains a missing value because no previous record exists for comparison.

Although the function is used for income growth, it is also reused for unit-sales growth.

The current monthly analysis uses it to calculate:

* `crecimiento_ingreso`
* `crecimiento_unidades`

#### Percentage Growth Calculation

The `get_income_percentage_growth()` function calculates the percentage change between consecutive values.

The calculation is based on:

`pandas.Series.pct_change()`

and the resulting value is multiplied by:

`100`

to represent percentage growth.

The function also:

1. Replaces positive infinity with `NaN`.
2. Replaces negative infinity with `NaN`.
3. Rounds percentage values to two decimal places.

The current monthly analysis uses it to calculate:

* `crecimiento_ingreso_porcentaje`
* `crecimiento_unidades_porcentaje`

#### Monthly Summary

The `get_monthly_summary()` function creates the main aggregated monthly sales analysis.

A copy of the original sales DataFrame is created before monthly transformations are performed.

The `fecha` column is converted into month identifiers using:

`YYYY-MM`

The resulting value is stored in:

`mes`

Sales records are then grouped by month.

For each month, the function calculates:

* Number of valid sales rows.
* Total units sold.
* Total income generated.

The resulting records are sorted chronologically from the earliest month to the latest month.

After aggregation, the function calculates growth metrics for both income and units sold.

The resulting DataFrame contains:

* `mes`: Month represented in `YYYY-MM` format.
* `filas_validas`: Number of valid sales records for the month.
* `unidades_vendidas`: Total units sold during the month.
* `ingreso_total`: Total income generated during the month.
* `crecimiento_ingreso`: Absolute income difference from the previous month.
* `crecimiento_ingreso_porcentaje`: Percentage income change from the previous month.
* `crecimiento_unidades`: Absolute units-sold difference from the previous month.
* `crecimiento_unidades_porcentaje`: Percentage units-sold change from the previous month.

The first month does not have previous-period growth values because no earlier month is available for comparison.

#### Monthly Best-Selling Product

The `get_monthly_best_selling_product()` function identifies the product or products with the highest number of units sold for each month.

A copy of the valid sales DataFrame is created and the `fecha` values are converted into:

`YYYY-MM`

The records are grouped by:

* `mes`
* `producto_id`

For each monthly product group, the function preserves:

* Product name.
* Product category.

and calculates:

* Total units sold.
* Total income.

The resulting structure contains:

* `mes`
* `producto_id`
* `producto`
* `categoria`
* `unidades_vendidas`
* `ingreso_total`

The maximum number of units sold is calculated independently for each month.

All products tied for the monthly maximum are preserved.

The result is stored in:

`monthly_best_selling_product`

#### Monthly Highest-Income Category

The `get_monthly_highest_income_category()` function identifies the category or categories that generated the highest total income for each month.

A copy of the valid sales DataFrame is created and the `fecha` values are converted into:

`YYYY-MM`

Records are grouped by:

* `mes`
* `categoria`

For every monthly category group, the function calculates:

* Total units sold.
* Total income.

The resulting DataFrame contains:

* `mes`
* `categoria`
* `unidades_vendidas`
* `ingreso_total`

The maximum income is calculated independently for each month.

All categories tied for the monthly maximum are preserved.

The result is stored in:

`monthly_highest_income_category`

#### Sales Analysis Process

The `analyze_sales()` function coordinates the complete sales-analysis workflow.

It performs the following operations:

1. Extracts valid sales rows and validation totals.
2. Creates a copy of the valid sales DataFrame.
3. Verifies that at least one valid sales row is available.
4. Creates the `ingreso_fila` column.
5. Calculates total income.
6. Calculates total units sold.
7. Creates the product summary.
8. Creates the category summary.
9. Creates the monthly summary.
10. Identifies the overall best-selling product or products.
11. Identifies the overall highest-income product or products.
12. Identifies the overall highest-income category or categories.
13. Creates the Top 5 best-selling product ranking through `get_top_5()`.
14. Creates the Top 5 highest-income product ranking through `get_top_5()`.
15. Calculates the best-selling product or products for each month.
16. Calculates the highest-income category or categories for each month.
17. Creates the city summary when the optional `ciudad` column is available.
18. Identifies the highest-income city or cities when city analysis is available.
19. Creates the payment-method summary when the optional `metodo_pago` column is available.
20. Identifies the highest-income payment method or methods when payment-method analysis is available.
21. Returns the complete analysis result.

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
* `monthly_summary`: pandas `DataFrame` containing monthly totals and growth metrics.
* `best_selling_product`: List containing the product or products tied for the highest number of units sold.
* `highest_income_product`: List containing the product or products tied for the highest total income.
* `highest_income_category`: List containing the category or categories tied for the highest total income.
* `top_5_best_selling_products`: List containing up to five products ranked by units sold and total income.
* `top_5_highest_income_products`: List containing up to five products ranked by total income.
* `monthly_best_selling_product`: pandas `DataFrame` containing the best-selling product or products for each month.
* `monthly_highest_income_category`: pandas `DataFrame` containing the highest-income category or categories for each month.

When the optional `ciudad` column is present, the result also contains:

* `city_summary`: pandas `DataFrame` containing aggregated city results.
* `highest_income_city`: List containing the city or cities tied for the highest total income.

When the optional `metodo_pago` column is present, the result also contains:

* `payment_method_summary`: pandas `DataFrame` containing aggregated payment-method results.
* `highest_income_payment_method`: List containing the payment method or methods tied for the highest total income.

#### Monthly Analysis Result

The `monthly_summary` DataFrame follows this structure:

```text
mes
| filas_validas
| unidades_vendidas
| ingreso_total
| crecimiento_ingreso
| crecimiento_ingreso_porcentaje
| crecimiento_unidades
| crecimiento_unidades_porcentaje
```

For example, conceptually:

```text
2026-07 | 25 | 84  | 15420.50 | NaN      | NaN   | NaN | NaN
2026-08 | 31 | 102 | 18750.00 | 3329.50  | 21.59 | 18  | 21.43
2026-09 | 18 | 56  | 9320.75  | -9429.25 | -50.29| -46 | -45.10
```

Growth values compare each month against the immediately preceding month.

The first month contains missing growth values because no previous month is available.

#### Monthly Best-Selling Product Result

The `monthly_best_selling_product` DataFrame follows this structure:

```text
mes
| producto_id
| producto
| categoria
| unidades_vendidas
| ingreso_total
```

More than one row may exist for the same month when multiple products share the highest number of units sold.

#### Monthly Highest-Income Category Result

The `monthly_highest_income_category` DataFrame follows this structure:

```text
mes
| categoria
| unidades_vendidas
| ingreso_total
```

More than one row may exist for the same month when multiple categories share the highest monthly income.

#### Optional Analysis

City and payment-method analyses depend on the presence of their corresponding optional columns.

If `ciudad` exists, `analyze_sales()` adds:

* `city_summary`
* `highest_income_city`

If `metodo_pago` exists, `analyze_sales()` adds:

* `payment_method_summary`
* `highest_income_payment_method`

The remaining core analyses, including monthly totals, growth metrics, monthly best-selling products, and monthly highest-income categories, are generated independently of these optional fields.

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
* **Output:** Product-summary DataFrame sorted by total income.

##### `get_category_summary()`

* **Input:** Valid sales DataFrame containing `ingreso_fila`.
* **Output:** Category-summary DataFrame sorted by total income.

##### `get_city_summary()`

* **Input:** Valid sales DataFrame containing `ciudad` and `ingreso_fila`.
* **Output:** City-summary DataFrame.

##### `get_payment_method_summary()`

* **Input:** Valid sales DataFrame containing `metodo_pago` and `ingreso_fila`.
* **Output:** Payment-method-summary DataFrame.

##### `get_records_with_max_value()`

* **Input:** DataFrame and numeric column name.
* **Output:** List of dictionaries containing all records tied for the maximum value.

##### `get_top_5()`

* **Input:** Product-summary DataFrame, sorting column or columns, and sort direction or directions.
* **Output:** List containing up to five sorted product records.

##### `get_income_growth_units()`

* **Input:** DataFrame, destination column name, and numeric source column.
* **Output:** DataFrame containing a new absolute-growth column.

##### `get_income_percentage_growth()`

* **Input:** DataFrame, destination column name, and numeric source column.
* **Output:** DataFrame containing a new percentage-growth column.

##### `get_monthly_summary()`

* **Input:** Valid sales DataFrame containing a datetime `fecha` column and `ingreso_fila`.
* **Output:** Monthly-summary DataFrame containing totals, absolute growth, and percentage growth.

##### `get_monthly_best_selling_product()`

* **Input:** Valid sales DataFrame containing a datetime `fecha` column and `ingreso_fila`.
* **Output:** DataFrame containing the best-selling product or tied products for each month.

##### `get_monthly_highest_income_category()`

* **Input:** Valid sales DataFrame containing a datetime `fecha` column and `ingreso_fila`.
* **Output:** DataFrame containing the highest-income category or tied categories for each month.

##### `analyze_sales()`

* **Input:** Dictionary containing validated sales rows and validation totals.
* **Output:** Dictionary containing general sales metrics, global summaries, Top 5 rankings, maximum-value records, monthly totals, growth metrics, monthly rankings, and optional city and payment-method analysis.

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

The sales report generation module converts previously calculated sales-analysis results, validation errors, and validation warnings into a structured human-readable plain-text report.

Each report section is generated by an independent helper function. Several helpers are designed to be reusable across different analysis structures, reducing duplicated formatting logic and keeping the reporting workflow easier to maintain, test, modify, and extend.

The generated report includes:

* General sales metrics.
* Overall best-selling products.
* Highest-income products.
* Highest-income categories.
* Top 5 product rankings.
* Product and category summaries.
* Detailed monthly sales information.
* Monthly income and unit-sales variations.
* Monthly best-selling products.
* Monthly highest-income categories.
* Validation errors.
* Validation warnings.

Optional city-based and payment-method-based sections are included when their corresponding analysis results are available.

The module currently provides the following functions:

* `get_general_summary()`
* `get_best_selling_product()`
* `get_highest_income()`
* `get_top_5()`
* `get_summary()`
* `get_errors()`
* `get_warnings()`
* `get_sign()`
* `get_monthly_summary()`
* `get_monthly_best_selling_product()`
* `get_monthly_highest_income_category()`
* `generate_report()`

#### General Summary

The `get_general_summary()` function generates the primary sales-metrics section.

It includes:

* Total processed rows.
* Total valid rows.
* Total invalid rows.
* Total income.
* Total units sold.

The total income is formatted using:

* Thousands separators.
* Two decimal places.
* Currency notation.

The generated section begins with:

`RESUMEN GENERAL`

#### Best-Selling Product

The `get_best_selling_product()` function formats the product or products with the highest number of units sold.

It reads the records stored in:

`best_selling_product`

For each record, the section displays:

* `producto_id`
* `producto`
* `unidades_vendidas`

If multiple products share the highest number of units sold, all tied products are included.

The generated section begins with:

`PRODUCTO MÁS VENDIDO`

#### Generic Highest-Income Formatter

The `get_highest_income()` function generates highest-income sections from a supplied list of records.

Instead of maintaining separate formatting functions for products, categories, cities, and payment methods, this reusable helper receives:

* The list of highest-income records.
* The section title.
* A primary dictionary key.
* An optional secondary dictionary key.

When a secondary key is supplied, both descriptive values are displayed.

For example, product records can use:

* `producto_id`
* `producto`

When no secondary key is provided, only the primary descriptive field is displayed.

Each formatted record also includes:

* `ingreso_total`
* `unidades_vendidas`

The helper is currently reused for:

* Highest-income products.
* Highest-income categories.
* Highest-income cities.
* Highest-income payment methods.

All tied records provided by the analysis layer are preserved.

#### Highest-Income Product

The highest-income product section is created through:

`get_highest_income()`

using:

* `highest_income_product`
* `producto_id`
* `producto`

The section begins with:

`PRODUCTO CON MAYOR INGRESO`

Each record includes:

* Product identifier.
* Product name.
* Total income.
* Units sold.

#### Highest-Income Category

The highest-income category section is created through:

`get_highest_income()`

using:

* `highest_income_category`
* `categoria`

The section begins with:

`CATEGORÍA CON MAYOR INGRESO`

Each record includes:

* Category.
* Total income.
* Units sold.

#### Highest-Income City

When city analysis is available, the report uses:

`get_highest_income()`

with:

* `highest_income_city`
* `ciudad`

The section begins with:

`CIUDAD CON MAYOR INGRESO`

Each record includes:

* City.
* Total income.
* Units sold.

This section is optional.

#### Highest-Income Payment Method

When payment-method analysis is available, the report uses:

`get_highest_income()`

with:

* `highest_income_payment_method`
* `metodo_pago`

The section begins with:

`MÉTODO DE PAGO CON MAYOR INGRESO`

Each record includes:

* Payment method.
* Total income.
* Units sold.

This section is optional.

#### Generic Top 5 Formatter

The `get_top_5()` function formats product-ranking records.

It receives:

* A list containing up to five product records.
* The title used for the ranking section.

For every product, it displays:

* Ranking position.
* `producto_id`
* `producto`
* `unidades_vendidas`
* `ingreso_total`

The same helper is reused for both supported Top 5 rankings.

#### Top 5 Best-Selling Products

The best-selling ranking uses:

`top_5_best_selling_products`

and the title:

`TOP 5 PRODUCTOS MÁS VENDIDOS`

The ranking contains up to five products and preserves the order previously calculated by the analysis module.

#### Top 5 Highest-Income Products

The highest-income ranking uses:

`top_5_highest_income_products`

and the title:

`TOP 5 PRODUCTOS CON MAYOR INGRESO`

The ranking contains up to five products and preserves the order previously calculated by the analysis module.

#### Generic Summary Formatter

The `get_summary()` function converts an analysis DataFrame into a human-readable plain-text table.

It receives:

* A pandas `DataFrame`.
* The section title.

The function first creates a copy of the supplied DataFrame.

This prevents display formatting from modifying the original analysis structure.

The copied:

`ingreso_total`

column is formatted as currency using:

* Thousands separators.
* Two decimal places.
* `$` prefix.

The DataFrame is then converted into plain text through:

`DataFrame.to_string(index=False)`

The pandas index is therefore excluded.

This generic helper is currently reused for:

* Product summary.
* Category summary.
* City summary.
* Payment-method summary.

#### Product Summary

The product summary is generated through:

`get_summary()`

using:

`product_summary`

and the title:

`RESUMEN POR PRODUCTO`

#### Category Summary

The category summary is generated through:

`get_summary()`

using:

`category_summary`

and the title:

`RESUMEN POR CATEGORÍA`

#### City Summary

When:

`city_summary`

is available, it is formatted through:

`get_summary()`

using the title:

`RESUMEN POR CIUDAD`

This section is omitted when city analysis is unavailable.

#### Payment-Method Summary

When:

`payment_method_summary`

is available, it is formatted through:

`get_summary()`

using the title:

`RESUMEN POR MÉTODO DE PAGO`

This section is omitted when payment-method analysis is unavailable.

#### Variation Sign Formatting

The `get_sign()` function returns the sign used when displaying numeric monthly variations.

Its behavior is:

* Negative value → `-`
* Positive value → `+`
* Zero → empty string
* `None` → empty string

This helper is used by the monthly-summary formatter for:

* Income variation.
* Income percentage variation.
* Unit-sales variation.
* Unit-sales percentage variation.

#### Monthly Summary

The `get_monthly_summary()` function generates a detailed month-by-month sales section.

Unlike earlier versions, the monthly information is not displayed as a direct pandas table.

The DataFrame is first processed using:

`replace({np.nan: None})`

and converted into individual records.

This allows missing growth values to be handled explicitly during text formatting.

For every month, the section displays:

* `mes`
* `filas_validas`
* `unidades_vendidas`
* `ingreso_total`
* `crecimiento_ingreso`
* `crecimiento_ingreso_porcentaje`
* `crecimiento_unidades`
* `crecimiento_unidades_porcentaje`

The generated section begins with:

`RESUMEN POR MES`

#### Monthly Income Variation

The absolute income difference from the previous month is displayed as:

`Variación de ingreso`

Positive values use:

`+$`

Negative values use:

`-$`

For example:

`+$2,450.75`

or:

`-$1,200.00`

The absolute numeric value is used during formatting while the sign is provided by `get_sign()`.

#### Monthly Income Percentage Variation

The percentage income difference is displayed as:

`Variación porcentual de ingreso`

For example:

`+12.45%`

or:

`-8.30%`

Percentage values are displayed with two decimal places.

#### Monthly Unit Variation

The absolute difference in units sold is displayed as:

`Variación de unidades`

For example:

`+25`

or:

`-14`

#### Monthly Unit Percentage Variation

The percentage change in units sold is displayed as:

`Variación porcentual de unidades`

For example:

`+10.50%`

or:

`-6.75%`

#### Missing Monthly Growth Values

The first available month has no previous month against which growth can be calculated.

When a monthly growth value is unavailable, the report displays:

`N/D`

This applies independently to:

* Income variation.
* Income percentage variation.
* Unit variation.
* Unit percentage variation.

#### Monthly Best-Selling Product

The `get_monthly_best_selling_product()` function generates the section containing the best-selling product or products for every month.

The supplied DataFrame is processed by replacing pandas `NaN` values with:

`None`

and converting the records into dictionaries.

The generated section begins with:

`PRODUCTO MÁS VENDIDO POR MES`

Records are visually grouped by month.

A month heading is displayed only when the current record belongs to a different month from the previously processed record.

For each monthly product record, the report displays:

* Product identifier.
* Product name.
* Category.
* Units sold.
* Income generated.

The displayed fields are based on:

* `mes`
* `producto_id`
* `producto`
* `categoria`
* `unidades_vendidas`
* `ingreso_total`

Multiple products can be displayed under the same month when the analysis layer identifies a tie for highest units sold.

#### Monthly Highest-Income Category

The `get_monthly_highest_income_category()` function generates the highest-income category or categories for every month.

The generated section begins with:

`CATEGORÍA CON MAYOR INGRESO POR MES`

Records are visually grouped by month.

For each monthly category record, the report displays:

* Category.
* Units sold.
* Income generated.

The section uses:

* `mes`
* `categoria`
* `unidades_vendidas`
* `ingreso_total`

Multiple categories can appear under the same month when they are tied for the highest monthly income.

#### Validation Errors

The `get_errors()` function generates the validation-errors section.

It performs the following operations:

1. Adds the validation-errors section title.
2. Detects when no validation errors are available.
3. Sorts errors by CSV line number.
4. Displays the affected column.
5. Displays the error type.
6. Displays the descriptive message.
7. Displays the original value when available.

Each validation-error record may contain:

* `line_number`
* `column`
* `error_type`
* `message`
* `original_value`

When:

`original_value`

is empty, the original-value line is omitted.

When no errors are available, the report displays:

`No se encontraron errores de validación.`

The section begins with:

`ERRORES DE VALIDACIÓN`

#### Validation Warnings

The `get_warnings()` function generates the non-critical warning section.

It performs the following operations:

1. Adds the warning section title.
2. Detects when no warnings are available.
3. Sorts warnings by `affected_value`.
4. Displays the affected product identifier.
5. Displays the warning type.
6. Displays the warning message.
7. Displays warning details.

Each warning can contain:

* `affected_value`
* `warning_type`
* `message`
* `details`

When `details` contains multiple values, they are joined using comma-separated text.

When no warnings are available, the report displays:

`No se encontraron advertencias.`

The section begins with:

`ADVERTENCIAS`

#### Report Header

The `generate_report()` function starts the complete report with:

`REPORTE DE VENTAS`

The report header also includes:

* Original source CSV filename.
* Generation date.

The source filename is obtained from:

`source_filename.name`

The generation date is obtained through:

`date.today()`

#### Report Generation Process

The `generate_report()` function coordinates the complete plain-text report-generation workflow.

It performs the following operations:

1. Creates the `REPORTE DE VENTAS` title.
2. Adds the original source CSV filename.
3. Adds the report-generation date.
4. Adds the general sales summary.
5. Adds the overall best-selling-product section.
6. Adds the highest-income-product section through `get_highest_income()`.
7. Adds the highest-income-category section through `get_highest_income()`.
8. Adds the highest-income-city section when city analysis is available.
9. Adds the highest-income-payment-method section when payment-method analysis is available.
10. Adds the Top 5 best-selling-products section through `get_top_5()`.
11. Adds the Top 5 highest-income-products section through `get_top_5()`.
12. Adds the product summary through `get_summary()`.
13. Adds the category summary through `get_summary()`.
14. Adds the city summary when city analysis is available.
15. Adds the payment-method summary when payment-method analysis is available.
16. Adds the detailed monthly summary.
17. Adds the monthly best-selling-product section.
18. Adds the monthly highest-income-category section.
19. Adds validation errors.
20. Adds validation warnings.
21. Combines all generated sections into a single plain-text report.

#### Optional Report Sections

City and payment-method sections depend on optional analysis results.

When:

`highest_income_city`

is available, the report includes:

`CIUDAD CON MAYOR INGRESO`

When:

`city_summary`

is available, the report includes:

`RESUMEN POR CIUDAD`

When:

`highest_income_payment_method`

is available, the report includes:

`MÉTODO DE PAGO CON MAYOR INGRESO`

When:

`payment_method_summary`

is available, the report includes:

`RESUMEN POR MÉTODO DE PAGO`

These sections are omitted when their corresponding analysis results are unavailable.

#### Report Structure

The complete report currently follows this order:

1. `REPORTE DE VENTAS`
2. Source filename and generation date.
3. `RESUMEN GENERAL`
4. `PRODUCTO MÁS VENDIDO`
5. `PRODUCTO CON MAYOR INGRESO`
6. `CATEGORÍA CON MAYOR INGRESO`
7. `CIUDAD CON MAYOR INGRESO` when available.
8. `MÉTODO DE PAGO CON MAYOR INGRESO` when available.
9. `TOP 5 PRODUCTOS MÁS VENDIDOS`
10. `TOP 5 PRODUCTOS CON MAYOR INGRESO`
11. `RESUMEN POR PRODUCTO`
12. `RESUMEN POR CATEGORÍA`
13. `RESUMEN POR CIUDAD` when available.
14. `RESUMEN POR MÉTODO DE PAGO` when available.
15. `RESUMEN POR MES`
16. `PRODUCTO MÁS VENDIDO POR MES`
17. `CATEGORÍA CON MAYOR INGRESO POR MES`
18. `ERRORES DE VALIDACIÓN`
19. `ADVERTENCIAS`

#### Display Formatting

The reporter receives already calculated analysis data and applies only presentation formatting.

General and highest-income monetary values are displayed using currency formatting such as:

`$12,450.75`

Product, category, city, and payment-method DataFrames are copied before their `ingreso_total` values are converted into formatted strings.

This prevents the reporter from modifying the original analysis DataFrames.

Monthly information follows a different presentation model.

Instead of using:

`DataFrame.to_string()`

the monthly DataFrames are converted into individual records so that:

* Growth values can be formatted independently.
* Positive and negative signs can be displayed explicitly.
* Missing growth values can be represented as `N/D`.
* Records can be visually grouped by month.

#### Reusable Formatting Helpers

The reporter now centralizes several previously duplicated responsibilities.

`get_highest_income()` replaces separate highest-income formatting functions for:

* Products.
* Categories.
* Cities.
* Payment methods.

`get_top_5()` replaces separate Top 5 formatting functions.

`get_summary()` replaces separate DataFrame-summary formatting functions for:

* Products.
* Categories.
* Cities.
* Payment methods.

This design keeps formatting rules consistent and reduces duplicated code.

#### Input and Output

##### `get_general_summary()`

* **Input:** Analysis-result dictionary.
* **Output:** Formatted general-sales summary.

##### `get_best_selling_product()`

* **Input:** Analysis-result dictionary containing `best_selling_product`.
* **Output:** Formatted overall best-selling-product section.

##### `get_highest_income()`

* **Input:** List of highest-income records, section title, primary field, and optional secondary field.
* **Output:** Formatted highest-income section.

##### `get_top_5()`

* **Input:** List containing ranked product records and section title.
* **Output:** Formatted Top 5 product-ranking section.

##### `get_summary()`

* **Input:** Analysis-summary DataFrame and section title.
* **Output:** Formatted plain-text DataFrame summary.

##### `get_sign()`

* **Input:** Numeric value or `None`.
* **Output:** `+`, `-`, or an empty string depending on the supplied value.

##### `get_monthly_summary()`

* **Input:** `monthly_summary` DataFrame.
* **Output:** Detailed formatted monthly totals and growth information.

##### `get_monthly_best_selling_product()`

* **Input:** `monthly_best_selling_product` DataFrame.
* **Output:** Formatted best-selling-product information grouped by month.

##### `get_monthly_highest_income_category()`

* **Input:** `monthly_highest_income_category` DataFrame.
* **Output:** Formatted highest-income-category information grouped by month.

##### `get_errors()`

* **Input:** List containing validation-error dictionaries.
* **Output:** Formatted validation-errors section.

##### `get_warnings()`

* **Input:** List containing validation-warning dictionaries.
* **Output:** Formatted validation-warnings section.

##### `generate_report()`

* **Input:** Analysis-result dictionary, validation-error list, validation-warning list, and source CSV `Path`.
* **Output:** Complete human-readable plain-text sales report ready to be displayed or saved.

#### Module Responsibility

The report-generation module is responsible for presentation formatting.

It receives already calculated analysis results and converts them into human-readable text.

It is responsible for:

* Creating report-section text.
* Formatting monetary values.
* Formatting monthly growth values.
* Formatting Top 5 rankings.
* Formatting highest-income records.
* Formatting DataFrame summaries.
* Organizing monthly records.
* Formatting validation errors.
* Formatting validation warnings.
* Combining report sections in the required order.

It does not:

* Validate the source CSV file.
* Read the source CSV file.
* Validate individual sales records.
* Calculate sales metrics.
* Calculate monthly growth.
* Determine rankings.
* Save report files directly.
* Generate charts.

Those responsibilities belong to the validation, reading, analysis, file-management, and chart-management modules.

---

### Report File Management Module

The report file management module handles the storage and export of generated sales reports and structured analysis results.

The module creates destination directories when necessary, generates a shared base filename using the source CSV filename and a timestamp, saves the human-readable report as TXT, exports the structured sales analysis as JSON, generates independent CSV analysis summaries, and creates a multi-sheet Excel workbook containing sales analysis and validation information.

Exported analysis data may include product, category, monthly, city, and payment-method summaries, monthly growth metrics, monthly best-selling products, monthly highest-income categories, Top 5 product rankings, validation errors, and validation warnings.

The module uses:

* `pathlib.Path` for file-system paths.
* `datetime` for timestamp-based filenames.
* `numpy` for missing-value handling before JSON serialization.
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
* `build_sheet()`
* `build_sheet_validation_errors()`
* `build_sheet_warnings()`
* `save_report_xlsx()`

#### Supported Output Formats

The module currently supports four report-file formats:

* TXT
* JSON
* CSV
* XLSX

Files generated during the same processing workflow use the same shared base filename.

Chart-image generation is handled separately by the chart-management module.

#### Report Saving Process

The `save_report()` function saves the human-readable sales report as a TXT file.

It performs the following operations:

1. Receives the generated report text.
2. Receives the destination folder as `str` or `Path`.
3. Receives a previously generated shared base filename.
4. Adds the `.txt` extension.
5. Converts the destination directory into a `Path`.
6. Creates the destination directory and missing parent directories when necessary.
7. Builds the complete output path.
8. Opens the destination file using UTF-8 encoding.
9. Writes the report contents.
10. Returns the `Path` pointing to the generated TXT file.

File-system `OSError` exceptions are converted into `ReportSaveError`.

#### Dynamic Base Filename Generation

The `create_report_base_name()` function generates the shared filename prefix used by generated outputs.

Unlike earlier versions, the base filename is derived from the original source CSV filename.

The function receives:

`input_file_path`

as either:

* `str`
* `Path`

It extracts the source filename without its extension using:

`Path(input_file_path).stem`

The source filename is then combined with the current local date and time.

The generated base filename follows this format:

`<source_filename>_YYYY-MM-DD_HH-MM-SS-fff`

For example, if the source file is:

`ventas_agosto.csv`

the generated base filename may be:

`ventas_agosto_2026-09-19_07-45-30-125`

The same base filename is reused across the generated report outputs.

For example:

`ventas_agosto_2026-09-19_07-45-30-125.txt`

`ventas_agosto_2026-09-19_07-45-30-125.json`

`ventas_agosto_2026-09-19_07-45-30-125.xlsx`

CSV files use the same base filename followed by a descriptive analysis suffix.

#### JSON Analysis Saving Process

The `save_analysis_json()` function saves the complete structured sales-analysis result as a JSON file.

Before serialization, the function creates a shallow copy of the original:

`analysis_result`

pandas DataFrames cannot be serialized directly to JSON through the standard `json` module, so the required DataFrames are converted into lists of dictionaries.

Before conversion, pandas `NaN` values are replaced with:

`None`

This causes missing analysis values to be represented as:

`null`

inside the generated JSON file.

The following DataFrames are always converted:

* `product_summary`
* `category_summary`
* `monthly_summary`
* `monthly_best_selling_product`
* `monthly_highest_income_category`

The following DataFrames are converted when available:

* `city_summary`
* `payment_method_summary`

The function:

1. Creates a shallow copy of the analysis result.
2. Replaces `NaN` values with `None` in DataFrame structures.
3. Converts required DataFrames into JSON-compatible records.
4. Converts optional DataFrames when available.
5. Adds the `.json` extension to the shared base filename.
6. Creates the destination directory when necessary.
7. Writes the JSON file using UTF-8 encoding.
8. Uses indentation for readable formatting.
9. Preserves non-ASCII characters through `ensure_ascii=False`.
10. Returns the generated JSON path.

The original `analysis_result` dictionary is not modified directly.

#### Missing Values in JSON

Monthly growth calculations can produce missing values when no previous month is available for comparison.

For example, the first monthly record may contain missing values for:

* `crecimiento_ingreso`
* `crecimiento_ingreso_porcentaje`
* `crecimiento_unidades`
* `crecimiento_unidades_porcentaje`

Before JSON serialization, these pandas `NaN` values are converted into Python `None`.

This produces valid JSON values such as:

```json
{
    "crecimiento_ingreso": null,
    "crecimiento_ingreso_porcentaje": null
}
```

#### CSV Analysis Summary Saving Process

The `save_analysis_result_csv_files()` function saves analysis DataFrames as independent CSV files.

The following summaries are always exported:

* `product_summary`
* `category_summary`
* `monthly_summary`
* `monthly_best_selling_product`
* `monthly_highest_income_category`

The following summaries are exported when available:

* `city_summary`
* `payment_method_summary`

Each generated CSV uses the shared base filename followed by a descriptive suffix.

Individual file creation is delegated to:

`create_save_analysis_result_csv_files_and_path()`

The function returns a dictionary containing the generated CSV paths.

#### CSV Result Dictionary

The dictionary returned by `save_analysis_result_csv_files()` uses Spanish keys to identify generated analysis summaries.

The standard entries are:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "resumen_mensual": Path(...),
    "resumen_mejores_vendidos_por_mes": Path(...),
    "resumen_categoria_mayor_ingreso_por_mes": Path(...)
}
```

When optional analyses are available, the dictionary may also contain:

```python
{
    "ciudad_resumen": Path(...),
    "metodo_de_pago_resumen": Path(...)
}
```

The following entries are always generated:

* `resumen_producto`: Product-summary CSV.
* `resumen_categoria`: Category-summary CSV.
* `resumen_mensual`: Monthly-summary CSV.
* `resumen_mejores_vendidos_por_mes`: Monthly best-selling-products CSV.
* `resumen_categoria_mayor_ingreso_por_mes`: Monthly highest-income-categories CSV.

The following entries are optional:

* `ciudad_resumen`: City-summary CSV.
* `metodo_de_pago_resumen`: Payment-method-summary CSV.

These dictionary keys identify generated CSV files inside the application.

They are independent from the physical filename suffixes.

#### CSV Physical Filenames

The current CSV filename suffixes are written in Spanish.

The standard CSV outputs use:

* `_productos.csv`
* `_categorias.csv`
* `_meses.csv`
* `_producto_top_mensual.csv`
* `_categoria_top_ingreso_mensual.csv`

Optional analyses use:

* `_ciudades.csv`
* `_metodos_pago.csv`

For a source file named:

`ventas_agosto.csv`

generated filenames may follow this structure:

`ventas_agosto_2026-09-19_07-45-30-125_productos.csv`

`ventas_agosto_2026-09-19_07-45-30-125_categorias.csv`

`ventas_agosto_2026-09-19_07-45-30-125_meses.csv`

`ventas_agosto_2026-09-19_07-45-30-125_producto_top_mensual.csv`

`ventas_agosto_2026-09-19_07-45-30-125_categoria_top_ingreso_mensual.csv`

Optional examples:

`ventas_agosto_2026-09-19_07-45-30-125_ciudades.csv`

`ventas_agosto_2026-09-19_07-45-30-125_metodos_pago.csv`

#### Individual CSV File Creation

The `create_save_analysis_result_csv_files_and_path()` function creates and saves one analysis DataFrame as a CSV file.

It receives:

* A pandas `DataFrame`.
* The destination directory as `str` or `Path`.
* The shared base filename.
* A descriptive filename suffix.

The function:

1. Combines the shared base filename with the descriptive suffix.
2. Adds the `.csv` extension.
3. Converts the destination directory into a `Path`.
4. Creates the destination directory and missing parent directories when necessary.
5. Builds the complete output path.
6. Saves the DataFrame without its pandas index.
7. Returns the generated CSV path.

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
10. Creates the general sales summary.
11. Creates the product summary.
12. Creates the category summary.
13. Creates the monthly summary.
14. Creates optional city and payment-method summaries when available.
15. Converts Top 5 product rankings into DataFrames.
16. Creates the Top 5 best-selling-product worksheet.
17. Creates the Top 5 highest-income-product worksheet.
18. Creates the monthly best-selling-product worksheet.
19. Creates the monthly highest-income-category worksheet.
20. Creates the validation-errors worksheet.
21. Creates the validation-warnings worksheet.
22. Saves the completed workbook.
23. Returns the resulting XLSX path.

#### Excel Workbook Structure

The XLSX workbook always includes:

* `Resumen General`
* `Productos`
* `Categorías`
* `Resumen por mes`
* `Productos mejor vendidos`
* `Productos con mejor Ingreso`
* `Producto más vendido por mes`
* `Categoría mayor ingreso por mes`
* `Validación de errores`
* `Advertencias`

The following worksheets are optional:

* `Resumen por ciudad`
* `Resumen por método de pago`

Optional worksheets are created only when their corresponding analysis results are available.

#### General Summary Worksheet

The `build_sheet_general_summary()` function creates:

`Resumen General`

The worksheet contains two columns:

* `Métrica`
* `Valor`

The following metrics are written:

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

#### Generic DataFrame Worksheet Builder

The `build_sheet()` function creates a worksheet from a pandas DataFrame.

It receives:

* The target `Workbook`.
* The DataFrame to export.
* The worksheet title.

The function creates the worksheet using:

`wb.create_sheet(title_str)`

It then converts the DataFrame into Excel-compatible rows using:

`dataframe_to_rows()`

with:

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
* pandas indexes to be excluded.

The generic helper replaces multiple specialized worksheet-building functions used in earlier versions.

It is currently reused for:

* Product summary.
* Category summary.
* Monthly summary.
* Optional city summary.
* Optional payment-method summary.
* Top 5 best-selling products.
* Top 5 highest-income products.
* Monthly best-selling products.
* Monthly highest-income categories.

#### Product Summary Worksheet

The product-summary worksheet is created through:

`build_sheet()`

using:

`product_summary`

and the title:

`Productos`

#### Category Summary Worksheet

The category-summary worksheet is created through:

`build_sheet()`

using:

`category_summary`

and the title:

`Categorías`

#### Monthly Summary Worksheet

The monthly-summary worksheet is created through:

`build_sheet()`

using:

`monthly_summary`

and the title:

`Resumen por mes`

The monthly DataFrame may contain:

* `mes`
* `filas_validas`
* `unidades_vendidas`
* `ingreso_total`
* `crecimiento_ingreso`
* `crecimiento_ingreso_porcentaje`
* `crecimiento_unidades`
* `crecimiento_unidades_porcentaje`

#### Best-Selling Products Worksheet

The `top_5_best_selling_products` list is first converted into a pandas DataFrame.

The resulting DataFrame is passed to:

`build_sheet()`

using the title:

`Productos mejor vendidos`

#### Highest-Income Products Worksheet

The `top_5_highest_income_products` list is first converted into a pandas DataFrame.

The resulting DataFrame is passed to:

`build_sheet()`

using the title:

`Productos con mejor Ingreso`

#### Monthly Best-Selling Product Worksheet

The `monthly_best_selling_product` DataFrame is exported through:

`build_sheet()`

using the title:

`Producto más vendido por mes`

The worksheet may contain multiple records for the same month when products are tied for the highest number of units sold.

#### Monthly Highest-Income Category Worksheet

The `monthly_highest_income_category` DataFrame is exported through:

`build_sheet()`

using the title:

`Categoría mayor ingreso por mes`

The worksheet may contain multiple records for the same month when categories are tied for the highest monthly income.

#### City Summary Worksheet

When `city_summary` is available, it is exported through:

`build_sheet()`

using the title:

`Resumen por ciudad`

The worksheet is omitted when city analysis is unavailable.

#### Payment-Method Summary Worksheet

When `payment_method_summary` is available, it is exported through:

`build_sheet()`

using the title:

`Resumen por método de pago`

The worksheet is omitted when payment-method analysis is unavailable.

#### Validation Errors Worksheet

The `build_sheet_validation_errors()` function creates:

`Validación de errores`

The worksheet contains validation errors detected while processing source sales records.

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

The worksheet contains warnings detected while validating sales records.

Internal warning dictionary keys are mapped to Spanish worksheet headers.

The columns are:

* `tipo_advertencia`
* `campo`
* `mensaje`
* `valor_afectado`
* `detalles`

Missing values are represented by empty strings.

When a warning value contains a list, its values are converted into comma-separated text before being written to the worksheet.

#### Workbook Creation

The Excel report is created using:

`openpyxl.Workbook`

A new workbook initially contains a default worksheet.

The module removes this worksheet using:

```python
wb.remove(wb.active)
```

The application then creates its report-specific worksheets before saving the workbook.

#### Input and Output

##### `save_report()`

* **Input:** Complete report text, destination folder as `str | Path`, and shared base filename.
* **Output:** `Path` pointing to the generated TXT report.

##### `create_report_base_name()`

* **Input:** Source CSV path as `str | Path`.
* **Output:** Shared base filename containing the source filename and timestamp.

##### `save_analysis_json()`

* **Input:** Analysis-result dictionary, destination folder as `str | Path`, and shared base filename.
* **Output:** `Path` pointing to the generated JSON analysis file.

##### `save_analysis_result_csv_files()`

* **Input:** Analysis-result dictionary, destination folder as `str | Path`, and shared base filename.
* **Output:** Dictionary containing five standard CSV paths and optional city/payment-method CSV paths.

##### `create_save_analysis_result_csv_files_and_path()`

* **Input:** DataFrame, destination folder, shared base filename, and descriptive suffix.
* **Output:** `Path` pointing to the generated CSV file.

##### `build_sheet_general_summary()`

* **Input:** Workbook and analysis-result dictionary.
* **Output:** `Worksheet` containing general sales metrics.

##### `build_sheet()`

* **Input:** Workbook, pandas DataFrame, and worksheet title.
* **Output:** `Worksheet` containing the supplied DataFrame.

##### `build_sheet_validation_errors()`

* **Input:** Workbook and validation-error records.
* **Output:** `Worksheet` containing validation-error information.

##### `build_sheet_warnings()`

* **Input:** Workbook and validation-warning records.
* **Output:** `Worksheet` containing validation-warning information.

##### `save_report_xlsx()`

* **Input:** Analysis-result dictionary, validation errors, validation warnings, destination folder as `str | Path`, and shared base filename.
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

Errors that are not represented by `OSError`, including invalid analysis structures and other library-specific exceptions, are propagated unless explicitly handled elsewhere in the application.

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

The sales report controller module coordinates the complete Sales Report processing workflow.

It acts as the orchestration layer between the graphical interface and the specialized modules responsible for file validation, CSV reading, DataFrame validation, sales analysis, plain-text report generation, file export, and chart generation.

The controller receives the source CSV file path and output directory, executes the complete processing pipeline, generates all supported report files and chart images, measures the total execution time, and returns a structured dictionary containing processing totals, generated output paths, and execution information.

The generated outputs currently include:

* TXT reports.
* JSON analysis files.
* CSV summary files.
* XLSX workbooks.
* PNG chart images.

The module currently provides the following function:

* `generate_sales_report()`

#### Controller Workflow

The `generate_sales_report()` function performs the following operations:

1. Starts the execution timer.
2. Validates the source CSV file using `validator.validate_csv_file()`.
3. Reads the validated CSV file using `csv_reader.read_csv_file()`.
4. Normalizes and validates the sales records using `validator.validate_dataframe()`.
5. Analyzes valid sales records using `analyzer.analyze_sales()`.
6. Generates the complete plain-text report using `reporter.generate_report()`.
7. Stores the processed, valid, and invalid row totals in the controller result.
8. Generates a shared report base filename using `file_manager.create_report_base_name(file_path)`.
9. Saves the TXT report using `file_manager.save_report()`.
10. Saves the structured analysis as JSON using `file_manager.save_analysis_json()`.
11. Saves available analysis summaries as independent CSV files using `file_manager.save_analysis_result_csv_files()`.
12. Generates the XLSX workbook using `file_manager.save_report_xlsx()`.
13. Generates chart images using `chart_manager.save_chart_images()`.
14. Stops the execution timer.
15. Calculates the total execution time.
16. Adds the execution time to the controller result.
17. Returns the complete result dictionary to the caller.

#### Module Coordination

The controller coordinates the following modules:

* `validator`: Validates the source file path, normalizes sales data, validates records, detects warnings, and separates valid and invalid rows.
* `csv_reader`: Reads the validated CSV file and converts its contents into a pandas `DataFrame`.
* `analyzer`: Calculates sales metrics, aggregated summaries, rankings, monthly analysis, growth indicators, and optional analyses.
* `reporter`: Converts analysis results, validation errors, and warnings into a structured plain-text sales report.
* `file_manager`: Generates the shared report base filename and saves TXT, JSON, CSV, and XLSX output files.
* `chart_manager`: Generates chart images from the calculated sales-analysis results.

The controller itself does not implement the internal processing logic of these modules. Its responsibility is to call them in the correct order and transfer their results between workflow stages.

#### Input Configuration

The `generate_sales_report()` function receives:

* `input_file_path`: Source CSV file path represented as a string.
* `output_folder`: Destination directory represented as either `str` or `Path`.

The source path is first validated before being passed to the CSV-reading module.

The output directory is passed to the file and chart generation functions responsible for storing generated outputs.

#### File Validation

The controller begins the backend workflow using:

`validator.validate_csv_file(input_file_path)`

The validation module verifies the physical source CSV file and returns a validated:

`Path`

This validated path is stored in:

`file_path`

and is reused by later workflow stages.

#### CSV Reading

The validated source path is passed to:

`csv_reader.read_csv_file(file_path)`

The resulting raw pandas DataFrame is stored in:

`df_raw`

This DataFrame is then sent to the DataFrame-validation workflow.

#### DataFrame Validation

The controller sends the raw sales DataFrame to:

`validator.validate_dataframe(df_raw)`

The returned validation structure contains:

* `df_valid_rows`
* `df_invalid_rows`
* `errors`
* `warnings`
* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`

The complete validation result is passed to the analysis module.

Validation errors and warnings are later reused by the plain-text reporter and XLSX export workflow.

#### Sales Analysis

The controller sends the validation result to:

`analyzer.analyze_sales()`

The resulting `analysis_result` contains the calculated structures required by reporting, file export, and chart generation.

Core analysis information includes:

* Total processed rows.
* Total valid rows.
* Total invalid rows.
* Total income.
* Total units sold.
* Product summary.
* Category summary.
* Monthly summary.
* Best-selling product records.
* Highest-income product records.
* Highest-income category records.
* Top 5 best-selling products.
* Top 5 highest-income products.
* Monthly best-selling products.
* Monthly highest-income categories.

The monthly summary can also contain:

* Absolute income growth.
* Percentage income growth.
* Absolute unit-sales growth.
* Percentage unit-sales growth.

When the optional `ciudad` column is available, the analysis may also contain:

* `city_summary`
* `highest_income_city`

When the optional `metodo_pago` column is available, the analysis may also contain:

* `payment_method_summary`
* `highest_income_payment_method`

#### Plain-Text Report Generation

The controller passes:

* `analysis_result`
* Validation errors.
* Validation warnings.
* Validated source-file path.

to:

`reporter.generate_report()`

The returned plain-text report is stored in:

`report_text`

This text is later passed to the file-management module for TXT storage.

#### Shared Base Filename

A single base filename is generated during each controller execution using:

`file_manager.create_report_base_name(file_path)`

The validated source `Path` is passed to the filename-generation function.

The returned base filename is reused by the output-generation functions so related files produced during the same workflow share a consistent naming convention.

The exact filename construction rules are defined by the file-management module.

#### Output File Coordination

The controller coordinates generation of the following report files:

* TXT sales report.
* JSON structured analysis.
* CSV analysis summaries.
* XLSX workbook.

The controller also coordinates:

* PNG chart generation.

All generated paths are collected inside the final controller result.

#### TXT Report Coordination

The human-readable report is saved through:

`file_manager.save_report()`

The function receives:

* `report_text`
* `output_folder`
* Shared base filename.

The generated path is stored as:

`report_path_txt`

#### JSON Analysis Coordination

The complete structured sales analysis is exported through:

`file_manager.save_analysis_json()`

The function receives:

* `analysis_result`
* `output_folder`
* Shared base filename.

The generated path is stored as:

`report_path_json`

#### CSV Summary Coordination

Independent analysis summaries are exported using:

`file_manager.save_analysis_result_csv_files()`

The function receives:

* `analysis_result`
* `output_folder`
* Shared base filename.

The resulting dictionary is stored as:

`reports_path_csv`

The standard CSV export currently includes:

* Product summary.
* Category summary.
* Monthly summary.

Optional CSV summaries may also include:

* City summary.
* Payment-method summary.

#### CSV Report Paths

The `reports_path_csv` dictionary uses internal Spanish identifiers for generated summary files.

The standard entries are:

* `resumen_producto`
* `resumen_categoria`
* `resumen_mensual`

Optional entries are:

* `ciudad_resumen`
* `metodo_de_pago_resumen`

A conceptual structure is:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "resumen_mensual": Path(...),
    "ciudad_resumen": Path(...),
    "metodo_de_pago_resumen": Path(...)
}
```

The city and payment-method entries are included only when their corresponding analysis data is available.

Physical CSV filenames and suffixes are defined by the file-management module.

#### XLSX Report Coordination

The controller generates the Excel workbook using:

`file_manager.save_report_xlsx()`

The function receives:

* Complete `analysis_result`.
* Validation errors.
* Validation warnings.
* Configured output folder.
* Shared base filename.

The resulting workbook path is stored as:

`report_path_xlsx`

The workbook can contain general metrics, product and category summaries, monthly analysis, rankings, optional city and payment-method summaries, validation errors, and validation warnings.

#### Chart Generation Coordination

Generated chart images are created using:

`chart_manager.save_chart_images()`

The function receives:

* Complete `analysis_result`.
* Configured output folder.
* Shared base filename.

The resulting dictionary of generated chart paths is stored as:

`reports_path_charts`

This dictionary is returned to the graphical interface, which uses it to populate the generated-chart selector and allow individual PNG files to be opened.

Chart-generation logic remains inside the dedicated `chart_manager` module rather than the controller.

#### Controller Result

The `generate_sales_report()` function returns a dictionary containing information about the complete workflow.

The result contains:

* `total_rows`: Total number of processed sales records.
* `total_valid_rows`: Number of records that passed validation.
* `total_invalid_rows`: Number of records containing validation errors.
* `report_path_txt`: Path pointing to the generated TXT report.
* `report_path_json`: Path pointing to the generated JSON analysis.
* `reports_path_csv`: Dictionary containing generated CSV summary paths.
* `report_path_xlsx`: Path pointing to the generated XLSX workbook.
* `reports_path_charts`: Dictionary containing generated chart-image paths.
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
        "resumen_mensual": Path(...),
        "ciudad_resumen": Path(...),
        "metodo_de_pago_resumen": Path(...)
    },

    "report_path_xlsx": Path(...),

    "reports_path_charts": {
        "...": Path(...),
        "...": Path(...)
    },

    "execution_time": "Execution time: 0.0123 seconds"
}
```

The city and payment-method CSV entries are optional.

The exact chart keys are determined by the chart-generation module.

#### GUI Integration

The controller acts as the primary backend entry point used by the graphical interface.

The GUI calls:

`controller.generate_sales_report()`

and provides:

* Selected source CSV path.
* Configured output directory.

After processing, the GUI receives the controller-result dictionary.

It uses:

* `report_path_txt` to display and open the TXT report.
* `report_path_json` to display and open the JSON analysis.
* `reports_path_csv` to populate the CSV selector.
* `report_path_xlsx` to display and open the Excel workbook.
* `reports_path_charts` to populate the generated-chart selector.
* Processing totals and execution information when required by other application components.

This keeps the graphical interface separated from backend processing details.

#### Execution Time

The controller uses:

`time.perf_counter()`

to measure the duration of the complete workflow.

Timing begins before source-file validation and ends after report files and chart images have been generated.

The measurement therefore includes:

* Source-file validation.
* CSV reading.
* Data normalization and validation.
* Sales analysis.
* Plain-text report generation.
* TXT file storage.
* JSON file storage.
* CSV summary storage.
* XLSX workbook generation and storage.
* Chart generation and storage.

The final duration is calculated as:

`end - start`

and formatted in seconds with four decimal places.

For example:

`Execution time: 0.0123 seconds`

#### Error Propagation

The controller does not directly handle application-specific exceptions.

Errors raised by:

* File validation.
* CSV reading.
* DataFrame validation.
* Sales analysis.
* Report generation.
* File management.
* Chart generation.

are propagated to the caller.

Application-specific exceptions can then be handled by the graphical interface.

Unexpected Python exceptions may also propagate to the GUI, where they can be presented through the application's error-handling workflow.

#### Input and Output

##### `generate_sales_report()`

* **Input:** Source CSV path as `str` and destination output directory as `str | Path`.
* **Output:** Dictionary containing processing totals, TXT, JSON, CSV, XLSX, and PNG chart paths, together with total execution time.

#### Responsibilities

The controller is responsible for:

* Coordinating the complete backend workflow.
* Passing information between specialized modules.
* Maintaining the correct processing order.
* Coordinating source-file validation.
* Coordinating CSV reading and DataFrame validation.
* Coordinating sales analysis.
* Coordinating plain-text report generation.
* Requesting the shared base filename.
* Coordinating TXT generation.
* Coordinating JSON generation.
* Coordinating CSV summary generation.
* Coordinating XLSX workbook generation.
* Coordinating chart generation.
* Measuring the total workflow execution time.
* Returning generated-output paths and processing information to the caller.

The controller is not responsible for:

* Implementing CSV parsing logic.
* Performing individual validation rules.
* Calculating sales metrics directly.
* Formatting the plain-text report directly.
* Creating report files directly.
* Drawing chart images directly.
* Displaying graphical interface elements.
* Handling user interaction.

Those responsibilities belong to the specialized backend modules and graphical interface.

---

### Graphical User Interface Module

The graphical user interface module provides the main desktop window for the Sales Report application using PySide6.

It allows the user to select a source CSV file, choose an output directory, generate sales reports and charts through the backend controller, inspect generated TXT, JSON, CSV, and XLSX files, open generated PNG charts, and access the configured output directory directly from the application.

TXT, JSON, and CSV files are displayed through dedicated read-only `FileViewerWindow` instances.

XLSX files and generated PNG charts are opened through the operating system's associated applications using `QDesktopServices`.

The graphical layer separates widget creation, signal connection, layout construction, event handling, output access, and generated-result state management into independent methods.

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
* `charts_paths`: Empty dictionary.

The initialization process also:

1. Configures the window title.
2. Configures the fixed window size.
3. Creates the central widget.
4. Creates interface labels through `create_labels()`.
5. Creates interface buttons through `create_buttons()`.
6. Connects button signals through `connect_buttons()`.
7. Creates the main vertical layout.
8. Builds the source-file section.
9. Builds the output-folder section.
10. Builds the report-generation section.
11. Builds the application-status section.
12. Builds the generated-files section.
13. Builds the generated-charts section.
14. Adds the output-folder access button.
15. Disables generated-output controls through `off_buttons()`.
16. Assigns the completed layout to the central widget.

#### Interface Organization

The graphical interface is organized through several categories of helper methods.

Widget creation:

* `create_labels()`
* `create_buttons()`

Signal configuration:

* `connect_buttons()`

Main layout construction:

* `build_selected_file_layout()`
* `build_selected_folder_layout()`
* `build_generate_report_layout()`
* `build_status_layout()`
* `build_generated_files_layout()`
* `build_generated_charts_layout()`

Generated-file sub-layouts:

* `build_txt_layout()`
* `build_json_layout()`
* `build_xlsx_layout()`
* `build_csv_layout()`
* `build_scroll_area_csv()`

Generated-chart sub-layouts:

* `build_chart_layout()`
* `build_scroll_area_chart()`

User actions:

* `selected_file_path()`
* `selected_folder_path()`
* `generate_reports()`
* `open_report_txt()`
* `open_report_json()`
* `open_report_csv()`
* `open_report_xlsx()`
* `open_chart_graphic()`
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

Generated CSV and chart paths are displayed dynamically through labels created during the report-generation process.

#### Button Creation

The `create_buttons()` method centralizes creation of the application buttons.

The interface currently provides buttons for:

* Selecting the source CSV file.
* Selecting the output directory.
* Generating reports and charts.
* Opening the TXT report.
* Opening the JSON analysis.
* Opening the selected CSV summary.
* Opening the XLSX analysis.
* Opening the selected generated chart.
* Opening the output directory.

The method creates the buttons and applies fixed sizes where required.

Signal connections are configured separately through `connect_buttons()`.

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
* `button_see_chart` → `open_chart_graphic()`

Separating widget creation from signal connection keeps interface initialization easier to understand and maintain.

#### Interface Sections

The main application window contains the following primary sections:

1. Source CSV file selection.
2. Output folder selection.
3. Report generation.
4. Application status.
5. Generated report files.
6. Generated charts.
7. Output-folder access.

The first six interface areas are organized using dedicated layouts and group boxes.

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

1. Generated-output controls are disabled.
2. Previously stored TXT, JSON, CSV, XLSX, and chart paths are cleared.
3. Previously displayed generated-report and chart information is removed.
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

1. Generated-output controls are disabled.
2. Previously stored TXT, JSON, CSV, XLSX, and chart paths are cleared.
3. Previously displayed generated-report and chart information is removed.
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

The `generate_reports()` method coordinates report and chart generation from the graphical interface.

It performs the following operations:

1. Temporarily disables the report-generation button.
2. Updates the application status to indicate that processing has started.
3. Verifies that a source CSV file has been selected.
4. Stops the process and displays a message when no source file is available.
5. Disables controls associated with previously generated outputs.
6. Clears stored TXT, JSON, CSV, XLSX, and chart paths.
7. Clears previously displayed output information.
8. Calls `controller.generate_sales_report()`.
9. Receives generated report and chart information from the controller.
10. Stores and displays the generated TXT report path.
11. Stores and displays the generated JSON analysis path.
12. Stores and displays the generated XLSX report path.
13. Adds generated CSV summary names to the CSV selector.
14. Creates labels containing generated CSV paths.
15. Stores CSV summary names and paths in `csv_paths`.
16. Adds generated chart names to the chart selector.
17. Creates labels containing generated chart paths.
18. Stores chart names and paths in `charts_paths`.
19. Updates the application status after successful generation.
20. Enables generated-output controls.
21. Displays application-specific or unexpected errors when necessary.
22. Re-enables the report-generation button after processing.

#### Backend Controller Integration

The GUI delegates the complete backend workflow to:

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
* `reports_path_charts`

The backend remains responsible for validation, reading, analysis, report generation, chart generation, and file storage.

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
* Reports and charts are generated successfully.
* An application-specific error occurs.
* An unexpected error occurs.

After successful processing, the interface indicates that files were saved and charts were generated successfully.

#### Generated Files Section

The `build_generated_files_layout()` method creates the group box used to display and access generated report files.

The section contains independent layouts for:

* TXT reports.
* JSON analysis.
* XLSX analysis.
* CSV summaries.
* Scrollable CSV path information.

The output-directory button is no longer part of this group box. It is added separately to the main application layout.

#### TXT Report Layout

The `build_txt_layout()` method creates the TXT report controls.

It contains:

* TXT section label.
* Generated TXT path.
* `Reporte TXT` button.

The button opens the generated report through `FileViewerWindow`.

#### JSON Report Layout

The `build_json_layout()` method creates the JSON analysis controls.

It contains:

* JSON section label.
* Generated JSON path.
* `Análisis JSON` button.

The button opens the generated file through `FileViewerWindow`.

#### XLSX Report Layout

The `build_xlsx_layout()` method creates the Excel report controls.

It contains:

* XLSX section label.
* Generated XLSX path.
* `Análisis Excel` button.

The XLSX workbook is opened externally through the operating system.

#### CSV Summary Layout

The `build_csv_layout()` method creates the CSV selection controls.

It contains:

* CSV section label.
* `csv_combobox`
* `Ver resumen CSV` button.

The combo box is populated dynamically after successful report generation.

#### Scrollable CSV Results

The `build_scroll_area_csv()` method creates a `QScrollArea` for generated CSV paths.

The internal layout is stored in:

`csv_summaries_layout`

Each generated CSV path is represented by a dynamically created `QLabel`.

The scroll area has a fixed height of:

`80`

pixels.

This allows multiple CSV paths to be displayed without excessively increasing the size of the main application window.

#### TXT Report Access

The generated TXT path is stored in:

`txt_path`

The:

`Reporte TXT`

button calls:

`open_report_txt()`

The method creates a `FileViewerWindow` and displays the generated TXT report in read-only mode.

#### JSON Analysis Access

The generated JSON path is stored in:

`json_path`

The:

`Análisis JSON`

button calls:

`open_report_json()`

The method creates a `FileViewerWindow` and displays the JSON analysis in read-only mode.

#### CSV Summary Access

Generated CSV summary paths are stored in:

`csv_paths`

Generated summary names are added to:

`csv_combobox`

The:

`Ver resumen CSV`

button calls:

`open_report_csv()`

The method retrieves the selected summary path and opens it through `FileViewerWindow`.

#### XLSX Report Access

The generated Excel workbook path is stored in:

`xlsx_path`

The:

`Análisis Excel`

button calls:

`open_report_xlsx()`

Unlike TXT, JSON, and CSV files, XLSX reports are not displayed through `FileViewerWindow`.

The method first verifies that the file exists.

If the file does not exist, a warning `QMessageBox` is displayed.

If the file exists, its path is converted into a local `QUrl` and opened through:

`QDesktopServices.openUrl()`

This allows the operating system to launch the application associated with XLSX files.

#### Generated Charts Section

The `build_generated_charts_layout()` method creates the section used to display and access generated charts.

The section is represented by the group box:

`Gráficas Generadas`

It contains:

* A chart-selection combo box.
* A `Ver Gráfica` button.
* A scrollable area displaying generated chart paths.

The section combines:

* `build_chart_layout()`
* `build_scroll_area_chart()`

#### Chart Selection Layout

The `build_chart_layout()` method creates the controls used to select a generated chart.

It creates:

`chart_combobox`

and places it beside:

`button_see_chart`

The combo box is populated dynamically using chart identifiers returned by the backend controller.

#### Scrollable Chart Results

The `build_scroll_area_chart()` method creates a scrollable area containing generated chart paths.

The internal dynamic layout is stored in:

`chart_graphics_layout`

Each generated chart is represented by an independent `QLabel`.

The scroll area has a fixed height of:

`80`

pixels.

#### Generated Chart State

Generated chart paths are stored in:

`charts_paths`

This dictionary maps chart identifiers to their corresponding generated PNG paths.

For each entry returned through `reports_path_charts`:

1. The chart identifier is added to `chart_combobox`.
2. A label displaying the chart identifier and path is created.
3. The label is added to `chart_graphics_layout`.
4. The chart path is stored in `charts_paths`.

#### Generated Chart Access

The `open_chart_graphic()` method opens the chart currently selected in:

`chart_combobox`

The method:

1. Reads the selected chart identifier.
2. Verifies that a selection is available.
3. Retrieves the corresponding PNG path from `charts_paths`.
4. Verifies that the PNG file exists.
5. Converts the local path into a `QUrl`.
6. Opens the chart through `QDesktopServices.openUrl()`.

If no chart has been selected, the interface displays an informational message:

`Debes seleccionar un archivo png primero`

If the selected PNG file does not exist, a warning message is displayed:

`El archivo png no existe`

Generated charts are therefore opened through the operating system rather than inside `FileViewerWindow`.

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

The button is positioned directly in the main application layout, outside the generated-files group box.

#### Generated-Output Control Management

The GUI centralizes enabling and disabling controls associated with generated reports and charts.

##### `on_buttons()`

Enables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.
* Chart selector.
* Chart access button.

This method is called after successful report and chart generation.

##### `off_buttons()`

Disables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.
* Chart selector.
* Chart access button.

This method is used when:

* A new source CSV file is selected.
* A new output folder is selected.
* A new report-generation process begins.
* Previously generated results should no longer be considered current.

#### Generated-Output State Cleanup

The GUI separates internal path cleanup from visual cleanup.

##### `clean_paths()`

Resets internal generated-output references:

* `txt_path` → `None`
* `json_path` → `None`
* `csv_paths` → `{}`
* `xlsx_path` → `None`
* `charts_paths` → `{}`

This prevents previously generated reports or charts from remaining associated with a new source file, output directory, or generation process.

##### `clean_labels()`

Clears generated-output information displayed in the interface.

It:

* Clears the TXT path label.
* Clears the JSON path label.
* Clears the XLSX path label.
* Clears the CSV selector.
* Clears the chart selector.
* Removes dynamically generated CSV path labels.
* Removes dynamically generated chart path labels.

##### `clean_layout()`

Removes dynamically generated widgets from a provided Qt layout.

The method iterates through the layout in reverse order and schedules each contained widget for deletion.

It is used to clear both:

* CSV summary path labels.
* Generated chart path labels.

#### Window State

The `SalesReportWindow` class maintains the following primary state values:

* `file_path`: Selected source CSV path.
* `output_folder`: Destination directory. Defaults to `reports/`.
* `txt_path`: Generated TXT report path.
* `json_path`: Generated JSON analysis path.
* `csv_paths`: Mapping between CSV summary names and generated paths.
* `xlsx_path`: Generated XLSX workbook path.
* `charts_paths`: Mapping between chart identifiers and generated PNG paths.

The class also maintains interface widgets, layouts, buttons, selectors, report-viewer windows, and generated-output controls.

#### PySide6 Components

The graphical interface currently uses:

* `QMainWindow`: Main desktop window.
* `QWidget`: Central window and internal containers.
* `QPushButton`: Interactive application controls.
* `QVBoxLayout`: Vertical organization.
* `QHBoxLayout`: Horizontal organization of report and chart controls.
* `QLabel`: Paths, titles, and status information.
* `QGroupBox`: Visual grouping of interface sections.
* `QFileDialog`: Source-file and output-directory selection.
* `QScrollArea`: Scrollable CSV and chart path displays.
* `QComboBox`: CSV-summary and generated-chart selection.
* `QMessageBox`: Critical, warning, and informational messages.
* `QDesktopServices`: Opening XLSX reports and PNG charts through the operating system.
* `QUrl`: Conversion of local XLSX and PNG paths for `QDesktopServices`.

#### Current GUI Workflow

The current graphical workflow is:

1. Launch `SalesReportWindow`.
2. Select a source CSV file.
3. Optionally select a custom output directory.
4. Use `reports/` when no custom directory is selected.
5. Press `Crear reporte`.
6. Verify that a source CSV file exists in the interface state.
7. Disable previous generated-output controls.
8. Clear previous report and chart state.
9. Send the source CSV and output folder to `controller.generate_sales_report()`.
10. Execute the complete backend workflow.
11. Receive TXT, JSON, CSV, XLSX, and chart output paths.
12. Display the generated TXT path.
13. Display the generated JSON path.
14. Display the generated XLSX path.
15. Populate the CSV selector.
16. Display CSV paths inside the CSV scroll area.
17. Populate the chart selector.
18. Display generated chart paths inside the chart scroll area.
19. Enable generated-output controls.
20. Allow TXT, JSON, and CSV reports to be inspected through `FileViewerWindow`.
21. Allow the XLSX workbook to be opened through the operating system.
22. Allow generated PNG charts to be opened through the operating system.
23. Allow the configured output directory to be opened.
24. Display the final success status or an error message.

#### Error Handling

The graphical interface handles:

* Application-specific exceptions derived from `AppError`.
* Unexpected Python exceptions.

During report generation, errors update the status to:

`Error en el proceso`

and are displayed through a critical `QMessageBox`.

The `open_report_xlsx()` method also handles a missing XLSX file by displaying a warning message.

The `open_chart_graphic()` method handles:

* Empty chart selection through an informational message.
* Missing PNG files through a warning message.

The graphical application remains open after handled errors so the user can correct the configuration or try again.

#### Input and Output

##### `SalesReportWindow`

* **Input:** User interaction through the graphical interface.
* **Output:** Main desktop interface for configuring, generating, displaying, and accessing sales reports and charts.

##### `create_labels()`

* **Input:** None.
* **Output:** Creates the labels required by the main interface.

##### `create_buttons()`

* **Input:** None.
* **Output:** Creates report, chart, file-selection, folder-selection, and output-access buttons.

##### `connect_buttons()`

* **Input:** None.
* **Output:** Connects button signals to their corresponding event handlers.

##### `build_generated_files_layout()`

* **Input:** None.
* **Output:** `QGroupBox` containing generated report-file controls.

##### `build_txt_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing TXT report controls.

##### `build_json_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing JSON report controls.

##### `build_xlsx_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing XLSX report controls.

##### `build_csv_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing CSV selection controls.

##### `build_scroll_area_csv()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing the CSV-path scroll area.

##### `build_generated_charts_layout()`

* **Input:** None.
* **Output:** `QGroupBox` containing generated-chart controls.

##### `build_chart_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing the chart selector and access button.

##### `build_scroll_area_chart()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing the generated-chart path scroll area.

##### `selected_file_path()`

* **Input:** CSV file selected through `QFileDialog`.
* **Output:** Updates the source-file state and resets previous generated-report and chart state.

##### `selected_folder_path()`

* **Input:** Directory selected through `QFileDialog`.
* **Output:** Updates the output-folder state and resets previous generated-output state.

##### `generate_reports()`

* **Input:** Selected CSV path and configured output directory.
* **Output:** Generates reports and charts through the controller and updates the GUI with TXT, JSON, CSV, XLSX, and PNG chart information.

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
* **Output:** Opens the workbook using the operating system's associated application or displays a warning when the file does not exist.

##### `open_chart_graphic()`

* **Input:** Chart selected through `chart_combobox`.
* **Output:** Opens the corresponding PNG chart through the operating system or displays an informational/warning message when necessary.

##### `open_output_folder()`

* **Input:** Configured output directory.
* **Output:** Opens the directory through the operating-system file manager.

##### `clean_layout()`

* **Input:** Qt layout containing dynamically generated widgets.
* **Output:** Removes the dynamically generated widgets.

##### `clean_labels()`

* **Input:** None.
* **Output:** Clears TXT, JSON, CSV, XLSX, and chart information displayed in the interface.

##### `clean_paths()`

* **Input:** None.
* **Output:** Resets stored TXT, JSON, CSV, XLSX, and chart paths.

##### `on_buttons()`

* **Input:** None.
* **Output:** Enables controls associated with generated reports and charts.

##### `off_buttons()`

* **Input:** None.
* **Output:** Disables controls associated with generated reports and charts.

#### Current Development Status

The graphical interface is connected to the Sales Report backend workflow and supports both report and chart access.

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
* Scrollable CSV path display.
* XLSX report generation and access.
* Generated PNG chart selection.
* Scrollable chart path display.
* Generated PNG chart opening.
* Read-only TXT, JSON, and CSV viewer integration.
* Operating-system XLSX opening.
* Operating-system PNG opening.
* Output-directory access.
* Centralized label creation.
* Centralized button creation.
* Centralized signal connection.
* Dedicated file sub-layouts.
* Dedicated chart sub-layouts.
* Generated-output state cleanup.
* Generated-output control management.
* Application-specific error presentation.
* Unexpected error presentation.
* Missing-XLSX warning presentation.
* Missing-PNG warning presentation.
* Empty-chart-selection information presentation.

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

The report file viewer module provides a dedicated PySide6 window for displaying the contents of generated text-based report files.

It is used by the main graphical interface to open TXT, JSON, and CSV reports without modifying their contents.

The viewer receives a window title and a file path, reads the selected file using UTF-8 encoding, displays its contents inside a read-only text area, and provides a button for closing the viewer.

The module currently provides the following class:

* `FileViewerWindow`

#### File Viewer Window

The `FileViewerWindow` class inherits from PySide6 `QMainWindow` and represents an independent read-only report-viewing window.

The window is configured with:

* A dynamic title received when the window is created.
* Width: `900`
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
3. Configures the window title.
4. Configures the fixed window size to `900 x 900`.
5. Creates the central widget.
6. Creates the main vertical layout.
7. Builds the report text area.
8. Builds the close-button area.
9. Adds both sections to the main window.

#### Report Display Area

The `build_text_area()` method creates the section responsible for displaying the selected report.

The section contains a read-only `QTextEdit` widget inside a `QGroupBox`.

The report file is read using:

`Path.read_text(encoding="utf-8")`

The complete file contents are displayed as plain text inside the text area.

Because the `QTextEdit` widget is configured as read-only, the user can inspect the report without modifying its contents through the application.

The source file itself is not changed by the viewer.

#### Supported Report Files

The file viewer is intended for text-based files generated by the Sales Report application.

The main graphical interface currently uses it for:

* TXT sales reports.
* JSON analysis files.
* CSV analysis summaries.

The viewer does not perform format-specific parsing.

It reads the selected file as UTF-8 text and displays its contents directly.

Binary formats such as XLSX are not handled by this window and are opened separately by the main graphical interface through the operating system.

#### Close Button Area

The `build_button_area()` method creates a horizontal layout containing the:

`Cerrar reporte`

button.

The button's `clicked` signal is connected directly to:

`close()`

When pressed, the report viewer window closes without affecting the main Sales Report application window.

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
* Parse binary report formats.

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

The graphical interface currently uses separate methods to display text-based generated reports:

* `open_report_txt()`
* `open_report_json()`
* `open_report_csv()`

Each method creates a new `FileViewerWindow` instance using the corresponding generated report path.

The XLSX report follows a different workflow and is opened externally through the operating system rather than through `FileViewerWindow`.

The relationship can be represented as:

`SalesReportWindow`

→ User selects a TXT, JSON, or CSV report

→ `FileViewerWindow`

→ Read the selected file using UTF-8

→ Display its contents in read-only mode

#### Responsibilities

This module is responsible for:

* Creating an independent report-viewing window.
* Reading generated text-based report files.
* Displaying file contents as plain text.
* Preventing modification through the viewer.
* Providing a control for closing the viewer window.

This module is not responsible for:

* Generating sales reports.
* Validating CSV files.
* Analyzing sales data.
* Saving report files.
* Opening XLSX workbooks.
* Selecting the source CSV file.
* Selecting the output folder.

Those responsibilities belong to the controller, backend modules, and main graphical interface.

---

### Chart Generation Module

The chart generation module converts previously calculated sales-analysis results into PNG chart images.

It uses pandas plotting capabilities together with Matplotlib to generate visual representations of monthly sales performance, percentage growth, product rankings, category performance, and optional city and payment-method analyses.

The module does not calculate sales metrics or rankings directly. Instead, it receives the structured results produced by the sales-analysis module and converts those results into chart images.

Generated charts use the same shared base filename used by the remaining report outputs, allowing PNG images to remain associated with the TXT, JSON, CSV, and XLSX files generated during the same workflow.

The module currently provides the following functions:

* `build_graph_image()`
* `save_chart_images()`

#### Dependencies

The chart-generation workflow uses:

* `pandas`: DataFrame manipulation and high-level plotting.
* `matplotlib.pyplot`: Chart configuration and PNG image storage.
* `pathlib.Path`: Output-directory and file-path management.
* `ChartGenerationError`: Application-specific chart-generation exception.

#### Chart Generation Architecture

The chart-generation workflow follows this general structure:

```text
analysis_result
      |
      v
save_chart_images()
      |
      +-- Prepare Top 5 DataFrames
      |
      +-- Prepare monthly product/category display columns
      |
      +-- Select analysis DataFrames
      |
      v
build_graph_image()
      |
      +-- Create output directory
      +-- Build bar chart
      +-- Configure labels
      +-- Configure title
      +-- Rotate x-axis labels
      +-- Apply tight layout
      +-- Save PNG at 150 DPI
      +-- Close Matplotlib figure
      |
      v
Generated PNG Path
```

The resulting chart paths are collected into a dictionary and returned to the caller.

#### Generic Chart Builder

The `build_graph_image()` function is the reusable chart-generation helper used by all chart types in the module.

It receives:

* A pandas `DataFrame`.
* The DataFrame column used for the x-axis.
* The DataFrame column used for the y-axis.
* The x-axis label.
* The y-axis label.
* The chart title.
* The output directory.
* The output filename without an extension.

The function automatically adds:

`.png`

to the provided filename.

#### Output Directory Creation

Before saving a chart, `build_graph_image()` converts the provided output directory into a:

`Path`

The destination directory and any missing parent directories are created through:

```python
folder.mkdir(parents=True, exist_ok=True)
```

This allows chart generation to work even when the configured destination directory does not already exist.

#### Chart Type

All charts generated by the current implementation use:

`bar`

charts.

The chart is created through the pandas:

`DataFrame.plot()`

interface.

The current configuration uses:

* `kind="bar"`
* `legend=False`
* Custom chart title.
* Custom x-axis and y-axis columns.
* Color `#4472C4`.

#### Chart Formatting

After creating the chart, the module applies additional Matplotlib formatting.

The x-axis label is configured through:

`plt.xlabel()`

The y-axis label is configured through:

`plt.ylabel()`

X-axis values are rotated:

`90`

degrees.

This helps display long category, product, month, city, and payment-method labels vertically.

The chart layout is adjusted using:

`plt.tight_layout()`

before the image is saved.

#### PNG Image Storage

Generated charts are saved through:

`plt.savefig()`

using:

`150 DPI`

The resulting path is returned as a `Path` object.

The general filename structure is:

`<shared_base_filename>_<chart_description>.png`

#### Matplotlib Figure Cleanup

The `build_graph_image()` function uses a `finally` block to execute:

`plt.close()`

This means the active Matplotlib figure is closed whether chart generation succeeds or raises a supported exception.

Closing the figure prevents previously generated plots from remaining active while multiple charts are generated during the same application workflow.

#### Chart Error Handling

The generic chart builder explicitly handles the following exception types:

* `OSError`
* `KeyError`
* `ValueError`
* `TypeError`

These errors may represent situations such as:

* Problems creating the destination directory.
* Problems saving the PNG file.
* Missing DataFrame columns.
* Invalid plotting values.
* Incorrect data types provided to the plotting workflow.

When one of these errors occurs, the module raises:

`ChartGenerationError`

using exception chaining.

The original exception therefore remains associated with the application-specific error.

#### Complete Chart Generation Process

The `save_chart_images()` function coordinates generation of all supported sales-analysis charts.

It receives:

* `analysis_result`
* `output_folder`
* `file_name_base`

The function uses the analysis structures already calculated by the analyzer and delegates individual PNG creation to:

`build_graph_image()`

#### Top 5 Data Preparation

The sales-analysis module stores Top 5 rankings as lists of dictionaries.

Before chart generation, the chart manager converts:

`top_5_best_selling_products`

into a pandas DataFrame.

It also converts:

`top_5_highest_income_products`

into a pandas DataFrame.

These DataFrames are then used for product-ranking charts.

The chart module does not recalculate or reorder the Top 5 results.

#### Standard Charts

The current implementation always generates ten standard chart images:

1. Monthly income.
2. Monthly units sold.
3. Monthly income percentage variation.
4. Monthly unit-sales percentage variation.
5. Monthly best-selling product.
6. Monthly highest-income category.
7. Top 5 highest-income products.
8. Top 5 products by units sold.
9. Income by category.
10. Units sold by category.

#### Monthly Income Chart

The dictionary key is:

`grafica_de_ingresos_mensuales`

The chart uses:

* X-axis: `mes`
* Y-axis: `ingreso_total`
* X-axis label: `Mes`
* Y-axis label: `Ingreso total`
* Title: `Ingreso mensual`

The generated filename uses:

`_ingreso_por_mes.png`

#### Monthly Units-Sold Chart

The dictionary key is:

`grafica_de_unidades_vendidas_mensualmente`

The chart uses:

* X-axis: `mes`
* Y-axis: `unidades_vendidas`
* X-axis label: `Mes`
* Y-axis label: `Unidades vendidas`
* Title: `Unidades vendidas por mes`

The generated filename uses:

`_unidades_vendidas_por_mes.png`

#### Monthly Income Percentage Growth Chart

The dictionary key is:

`grafica_crecimiento_porcentaje_mensual`

The chart uses:

* X-axis: `mes`
* Y-axis: `crecimiento_ingreso_porcentaje`
* X-axis label: `Mes`
* Y-axis label: `Variación de ingreso (%)`
* Title: `Variación porcentual de ingreso por mes`

The generated filename uses:

`_crecimiento_porcentaje_por_mes.png`

#### Monthly Unit Percentage Growth Chart

The dictionary key is:

`grafica_crecimiento_porcentaje_unidades`

The chart uses:

* X-axis: `mes`
* Y-axis: `crecimiento_unidades_porcentaje`
* X-axis label: `Mes`
* Y-axis label: `Variación de unidades (%)`
* Title: `Variación porcentual de unidades por mes`

The generated filename uses:

`_crecimiento_porcentaje_unidades.png`

#### Monthly Best-Selling Product Chart

The monthly best-selling-product chart uses:

`monthly_best_selling_product`

Before generating the image, the module creates a copy of the original DataFrame.

This prevents chart-specific display transformations from modifying the original analysis result.

A new display column is created:

`mes_producto`

Its value combines:

`mes`

with:

`producto`

using the following conceptual structure:

```text
YYYY-MM - Product
```

This combined value is used as the chart x-axis.

The dictionary key is:

`grafica_producto_top_mensual`

The chart uses:

* X-axis: `mes_producto`
* Y-axis: `unidades_vendidas`
* X-axis label: `Mes y Producto`
* Y-axis label: `Unidades vendidas`
* Title: `Unidades del producto más Vendido por mes`

The generated filename uses:

`_producto_top_mensual.png`

If multiple products are tied for the highest number of units sold during the same month, each available record can be represented independently.

#### Monthly Highest-Income Category Chart

The monthly highest-income-category chart uses:

`monthly_highest_income_category`

The original DataFrame is copied before chart-specific transformations are performed.

The module creates:

`mes_categoria`

by combining:

* `mes`
* `categoria`

The resulting value follows the conceptual structure:

```text
YYYY-MM - Category
```

The dictionary key is:

`grafica_categoria_top_ingreso`

The chart uses:

* X-axis: `mes_categoria`
* Y-axis: `ingreso_total`
* X-axis label: `Mes y Categoría`
* Y-axis label: `Ingreso total`
* Title: `Categoría con mejor ingreso por mes`

The generated filename uses:

`_categoria_top_ingreso_mensual.png`

Multiple categories can be represented for the same month when the analysis contains tied highest-income categories.

#### Top 5 Highest-Income Products Chart

The dictionary key is:

`grafica_producto_top_ingreso`

The source data is:

`top_5_highest_income_products`

after conversion into a pandas DataFrame.

The chart uses:

* X-axis: `producto`
* Y-axis: `ingreso_total`
* X-axis label: `Producto`
* Y-axis label: `Ingreso total`
* Title: `Top 5 productos por ingreso`

The generated filename uses:

`_ingreso_producto_top.png`

#### Top 5 Products by Units Sold Chart

The dictionary key is:

`grafica_unidades_producto_top`

The source data is:

`top_5_best_selling_products`

after conversion into a pandas DataFrame.

The chart uses:

* X-axis: `producto`
* Y-axis: `unidades_vendidas`
* X-axis label: `Producto`
* Y-axis label: `Unidades vendidas`
* Title: `Top 5 productos por unidades vendidas`

The generated filename uses:

`_unidades_producto_top.png`

#### Category Income Chart

The dictionary key is:

`grafica_ingreso_categoria`

The source data is:

`category_summary`

The chart uses:

* X-axis: `categoria`
* Y-axis: `ingreso_total`
* X-axis label: `Categoría`
* Y-axis label: `Ingreso total`
* Title: `Ingreso por categoría`

The generated filename uses:

`_ingreso_categoria.png`

#### Category Units-Sold Chart

The dictionary key is:

`grafica_unidades_categoria`

The source data is:

`category_summary`

The chart uses:

* X-axis: `categoria`
* Y-axis: `unidades_vendidas`
* X-axis label: `Categoría`
* Y-axis label: `Unidades vendidas`
* Title: `Ventas por categoría`

The generated filename uses:

`_unidades_categoria.png`

#### Optional City Charts

City charts are generated only when:

`city_summary`

exists in `analysis_result`, is not `None`, and is not empty.

When city information is available, two additional charts are generated.

##### City Income Chart

The dictionary key is:

`grafica_ingreso_ciudad`

The chart uses:

* X-axis: `ciudad`
* Y-axis: `ingreso_total`
* X-axis label: `Ciudad`
* Y-axis label: `Ingreso total`
* Title: `Ingreso por ciudad`

The generated filename uses:

`_ingreso_ciudad.png`

##### City Units-Sold Chart

The dictionary key is:

`grafica_unidades_ciudad`

The chart uses:

* X-axis: `ciudad`
* Y-axis: `unidades_vendidas`
* X-axis label: `Ciudad`
* Y-axis label: `Unidades vendidas`
* Title: `Ventas por ciudad`

The generated filename uses:

`_unidades_ciudad.png`

#### Optional Payment-Method Charts

Payment-method charts are generated only when:

`payment_method_summary`

exists in `analysis_result`, is not `None`, and is not empty.

When payment-method information is available, two additional charts are generated.

##### Payment-Method Income Chart

The dictionary key is:

`grafica_ingreso_metodo_pago`

The chart uses:

* X-axis: `metodo_pago`
* Y-axis: `ingreso_total`
* X-axis label: `Método de pago`
* Y-axis label: `Ingreso total`
* Title: `Ingreso por método de pago`

The generated filename uses:

`_ingreso_metodo_pago.png`

##### Payment-Method Units-Sold Chart

The dictionary key is:

`grafica_unidades_metodo_pago`

The chart uses:

* X-axis: `metodo_pago`
* Y-axis: `unidades_vendidas`
* X-axis label: `Método de pago`
* Y-axis label: `Unidades vendidas`
* Title: `Ventas por método de pago`

The generated filename uses:

`_unidades_metodo_pago.png`

#### Number of Generated Charts

The module always generates:

`10`

standard charts.

If city information is available, two additional charts are generated.

If payment-method information is available, two additional charts are generated.

Therefore, depending on available optional data, the workflow can generate:

* 10 charts with no optional analyses.
* 12 charts when either city or payment-method analysis is available.
* 14 charts when both optional analyses are available.

#### Generated Chart Dictionary

The `save_chart_images()` function returns a dictionary mapping chart identifiers to their generated PNG paths.

The standard structure is:

```python
{
    "grafica_de_ingresos_mensuales": Path(...),
    "grafica_de_unidades_vendidas_mensualmente": Path(...),
    "grafica_crecimiento_porcentaje_mensual": Path(...),
    "grafica_crecimiento_porcentaje_unidades": Path(...),
    "grafica_producto_top_mensual": Path(...),
    "grafica_categoria_top_ingreso": Path(...),
    "grafica_producto_top_ingreso": Path(...),
    "grafica_unidades_producto_top": Path(...),
    "grafica_ingreso_categoria": Path(...),
    "grafica_unidades_categoria": Path(...)
}
```

When city analysis is available, the dictionary also contains:

```python
{
    "grafica_ingreso_ciudad": Path(...),
    "grafica_unidades_ciudad": Path(...)
}
```

When payment-method analysis is available, the dictionary also contains:

```python
{
    "grafica_ingreso_metodo_pago": Path(...),
    "grafica_unidades_metodo_pago": Path(...)
}
```

#### Shared Filename Integration

The chart manager receives:

`file_name_base`

from the controller.

This is the same shared base filename used during the report-generation workflow.

Each chart adds its own descriptive suffix.

For example, if the shared base filename is:

`ventas_agosto_2026-09-19_07-45-30-125`

generated chart files may include:

`ventas_agosto_2026-09-19_07-45-30-125_ingreso_por_mes.png`

`ventas_agosto_2026-09-19_07-45-30-125_unidades_vendidas_por_mes.png`

`ventas_agosto_2026-09-19_07-45-30-125_producto_top_mensual.png`

`ventas_agosto_2026-09-19_07-45-30-125_ingreso_categoria.png`

This keeps chart images associated with the report files produced from the same source CSV.

#### Controller Integration

The controller generates charts through:

`chart_manager.save_chart_images()`

The controller provides:

* `analysis_result`
* `output_folder`
* Shared base filename.

The resulting chart dictionary is stored in the controller result as:

`reports_path_charts`

This allows the graphical interface to access generated chart identifiers and their corresponding PNG paths.

#### Graphical Interface Integration

The graphical interface receives:

`reports_path_charts`

from the controller.

Each chart identifier is added to the chart selector.

The corresponding PNG path is stored inside:

`charts_paths`

The graphical interface can then open the selected generated chart through the operating system.

The chart-management module itself does not display the generated images inside the GUI.

#### Analysis Integration

The chart manager depends on analysis structures produced by the sales-analysis module.

The required analysis entries include:

* `monthly_summary`
* `monthly_best_selling_product`
* `monthly_highest_income_category`
* `top_5_best_selling_products`
* `top_5_highest_income_products`
* `category_summary`

Optional analysis entries include:

* `city_summary`
* `payment_method_summary`

The chart manager does not calculate these analysis structures.

#### Input and Output

##### `build_graph_image()`

* **Input:** DataFrame, x-axis column, y-axis column, axis labels, chart title, destination folder, and output filename.
* **Output:** `Path` pointing to the generated PNG image.

##### `save_chart_images()`

* **Input:** Complete analysis-result dictionary, output directory as `str | Path`, and shared base filename.
* **Output:** Dictionary mapping chart identifiers to generated PNG image paths.

#### Responsibilities

The chart-generation module is responsible for:

* Receiving previously calculated sales-analysis results.
* Converting supported analysis structures into charts.
* Generating bar charts.
* Applying chart titles and axis labels.
* Rotating x-axis labels.
* Applying chart layout adjustments.
* Generating PNG images.
* Saving chart images at 150 DPI.
* Creating output directories when necessary.
* Maintaining chart-specific filename suffixes.
* Preparing chart-specific DataFrame copies.
* Converting Top 5 lists into DataFrames for visualization.
* Returning generated chart paths.
* Converting supported generation failures into `ChartGenerationError`.
* Closing Matplotlib figures after generation attempts.

The chart-generation module is not responsible for:

* Reading source CSV files.
* Validating sales records.
* Calculating total income.
* Calculating total units sold.
* Calculating monthly growth.
* Determining Top 5 rankings.
* Determining monthly best-selling products.
* Determining monthly highest-income categories.
* Generating TXT reports.
* Generating JSON files.
* Generating CSV files.
* Generating XLSX workbooks.
* Displaying charts inside the graphical interface.

Those responsibilities belong to the corresponding validation, analysis, reporting, file-management, controller, and graphical-interface modules.

#### Related Exception

* `ChartGenerationError`

---
