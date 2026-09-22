# Sales Report

> **Project Status:** Version **3.0** — Functional modular desktop application with PySide6, multi-format report export, PDF reporting, monthly analysis, automatic chart generation, and an interactive sales dashboard. The project has been manually tested with sample sales CSV files.

Sales Report is a modular Python application for validating sales data, analyzing valid records, generating structured reports, exporting analysis results in multiple formats, producing automatic sales charts, and presenting calculated metrics through a graphical dashboard.

The application includes a PySide6 graphical interface that allows users to:

* Select a source CSV file.
* Choose an output directory.
* Generate reports and charts.
* Inspect generated TXT, JSON, and CSV files.
* Open XLSX reports.
* Open PDF reports.
* Open generated PNG charts.
* Access the configured output directory.
* Open an interactive sales dashboard.

The application interface and user-facing messages are displayed in Spanish, while the project source code and technical documentation are maintained in English.

---

## Project Architecture

The project follows a modular architecture in which each module is responsible for a specific part of the application workflow.

The application separates:

* Graphical presentation.
* Dashboard presentation.
* Workflow orchestration.
* Source-file validation.
* CSV reading.
* Data normalization and record validation.
* Sales analysis.
* Plain-text report formatting.
* Multi-format file management.
* Chart generation.
* PDF generation.
* Custom exception handling.

The current application relationship can be represented as:

```text
                         Source CSV
                             |
                             v
                       SalesReportWindow
                             |
                             v
                controller.generate_sales_report()
                             |
                             v
                         validator
                             |
                             v
                        csv_reader
                             |
                             v
                validator.validate_dataframe()
                             |
                             v
                          analyzer
                             |
                    analysis_result
                             |
           +-----------------+-----------------+
           |                 |                 |
           v                 v                 v
       reporter         chart_manager      file_manager
           |                 |                 |
           |                 |          +------+------+
           |                 |          |      |      |
           |                 |         TXT   JSON    CSV
           |                 |                 |
           |                 |                XLSX
           |                 |
           |                 v
           |            PNG charts
           |                 |
           +-----------------+-------------------+
                             |
                             v
                        pdf_reporter
                             |
                             v
                            PDF
                             |
                             v
              reports + analysis_result
                             |
                             v
                       SalesReportWindow
                     /                  \
                    v                    v
          Generated File Access    DashboardWindow
                                         |
                              +----------+----------+
                              |          |          |
                              v          v          v
                             KPIs   Best Results   Charts
```

Generated TXT, JSON, and CSV files can be inspected through:

`FileViewerWindow`

Generated XLSX reports, PDF reports, and PNG charts are opened using the operating system's associated applications.

The dashboard receives the already calculated:

* `analysis_result`
* `charts_paths`

and presents the information without recalculating backend metrics.

---

## Main Modules

The main project modules include:

* `controller`: Coordinates the complete sales-report generation workflow and returns both generated-output information and the structured analysis result.
* `validator`: Validates the source file, normalizes records, validates sales data, detects warnings, and separates valid and invalid rows.
* `csv_reader`: Reads the validated CSV file into a pandas `DataFrame`.
* `analyzer`: Calculates general metrics, aggregated summaries, rankings, monthly growth, monthly performance results, and optional analyses.
* `reporter`: Generates the structured human-readable plain-text sales report.
* `file_manager`: Saves TXT, JSON, CSV, and XLSX output files.
* `chart_manager`: Generates PNG chart images from sales-analysis results.
* `pdf_reporter`: Generates a structured PDF report containing sales information, tables, charts, validation errors, and warnings.
* `errors`: Defines application-specific exceptions and Spanish user-facing error messages.
* `gui.main_window`: Provides the main PySide6 graphical interface.
* `gui.file_viewer_window`: Displays generated TXT, JSON, and CSV files in read-only viewer windows.
* `gui.dashboard_window`: Provides the interactive graphical sales dashboard.
* Console application entry point: Provides a direct backend execution workflow using predefined source and output paths.

---

## Installation and Usage

### Requirements

Before running the project, make sure the following tools are installed:

* Python 3.10 or later.
* `pip`.
* Git, if the project will be cloned from GitHub.

The application uses libraries including:

* `PySide6`
* `pandas`
* `numpy`
* `openpyxl`
* `matplotlib`
* `reportlab`

The complete dependency list is maintained in:

`requirements.txt`

Install all project dependencies using:

```bash
pip install -r requirements.txt
```

---

## Installation

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

The application processes sales information from a CSV file selected by the user or supplied through the console workflow.

The CSV file must contain the following required columns:

```text
producto_id,producto,categoria,precio,cantidad,fecha
```

The expected date format is:

```text
YYYY-MM-DD
```

The application also supports:

* `ciudad`
* `metodo_pago`

as optional columns.

These columns are not required for the core validation workflow.

When present, they are normalized and used to generate additional:

* Analysis summaries.
* Rankings.
* Report sections.
* CSV files.
* XLSX worksheets.
* PDF tables.
* Charts.

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

## Graphical Application

The project provides a PySide6 graphical interface through:

`SalesReportWindow`

The main window allows the user to:

1. Select a source CSV file.
2. Optionally select a custom output directory.
3. Use `reports/` as the default output directory.
4. Start the complete report-generation process.
5. View the current application status.
6. View generated TXT, JSON, XLSX, PDF, and CSV paths.
7. Select generated CSV summaries from a combo box.
8. Open TXT, JSON, and CSV files through read-only viewer windows.
9. Open the XLSX workbook through the operating system.
10. Open the generated PDF report through the operating system.
11. Select generated charts from a combo box.
12. Open generated PNG charts through the operating system.
13. Open the configured output directory.
14. Open the interactive sales dashboard.

The current main window uses:

```text
Title: Generador de Reportes de Ventas
Width: 900
Height: 1000
```

---

## Console Entry Point

The project also contains a console execution workflow.

The current console configuration uses:

```python
input_file_path = "data/sales.csv"
output_folder = "reports"
```

It calls:

```python
reports, _ = controller.generate_sales_report(
    input_file_path,
    output_folder
)
```

The generated-output dictionary is printed in the console.

The structured `analysis_result` is intentionally ignored by this entry point because it is not required for console output.

Nested dictionaries such as CSV and chart path collections are iterated so every generated entry can be printed individually.

---

## Application Workflow

When the user starts report generation, the application performs the following workflow:

1. Verifies that a source CSV file is available.
2. Sends the source path and output directory to `controller.generate_sales_report()`.
3. Starts the execution timer.
4. Validates the source CSV file.
5. Reads the validated file into a pandas `DataFrame`.
6. Normalizes and validates the sales records.
7. Separates valid and invalid rows.
8. Detects validation warnings.
9. Verifies that valid records are available.
10. Calculates row-level income.
11. Calculates total income.
12. Calculates total units sold.
13. Generates the product summary.
14. Generates the category summary.
15. Generates the monthly summary.
16. Calculates monthly income growth.
17. Calculates monthly income percentage growth.
18. Calculates monthly unit-sales growth.
19. Calculates monthly unit-sales percentage growth.
20. Determines overall highest-performing records.
21. Generates Top 5 product rankings.
22. Determines the best-selling product or tied products for each month.
23. Determines the highest-income category or tied categories for each month.
24. Generates city analysis when `ciudad` is available.
25. Generates payment-method analysis when `metodo_pago` is available.
26. Generates the structured plain-text report.
27. Creates a shared base filename.
28. Saves the TXT report.
29. Saves the complete structured analysis as JSON.
30. Saves five standard CSV analysis summaries.
31. Saves optional city and payment-method CSV summaries when available.
32. Generates the XLSX workbook.
33. Generates ten standard PNG charts.
34. Generates optional city and payment-method charts when available.
35. Generates the PDF report using the calculated analysis, validation information, and generated chart paths.
36. Calculates total execution time.
37. Returns `reports`.
38. Returns the complete `analysis_result`.
39. Displays generated output information in the graphical interface.
40. Stores the structured analysis for dashboard access.
41. Enables generated-output controls.
42. Enables dashboard access.

---

## Controller Return Contract

The controller returns:

```python
return reports, analysis_result
```

The first structure:

`reports`

contains generated-output and workflow information.

The second:

`analysis_result`

contains the complete structured sales analysis.

Conceptually:

```text
controller.generate_sales_report()
            |
            +---- reports
            |       |
            |       +-- row totals
            |       +-- TXT path
            |       +-- JSON path
            |       +-- CSV paths
            |       +-- XLSX path
            |       +-- PNG paths
            |       +-- PDF path
            |       +-- execution time
            |
            +---- analysis_result
                    |
                    +-- general metrics
                    +-- summaries
                    +-- rankings
                    +-- monthly analysis
                    +-- optional analysis
```

The GUI stores these structures separately as:

* `data_analysis`
* `analysis_result`

This allows the generated files and analytical structures to be consumed independently.

---

## Generated Output Files

Generated outputs are stored in the selected output directory.

If no custom directory is selected, the default directory is:

```text
reports/
```

If the destination directory does not exist, the application creates it when necessary.

All files generated during the same execution share a base filename containing:

* Original source CSV filename without its extension.
* Current local date.
* Current local time.
* Milliseconds.

The base filename follows:

```text
<source_filename>_YYYY-MM-DD_HH-MM-SS-fff
```

For example:

```text
ventas_agosto_2026-09-19_07-45-30-125
```

A normal execution can generate:

* TXT
* JSON
* CSV
* XLSX
* PNG
* PDF

files associated with the same processing run.

Each execution generates a new timestamp, allowing results from separate executions to coexist.

---

## Generated TXT Report

The TXT file contains the human-readable sales report.

Depending on available data, it includes:

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

Monthly growth values that cannot be calculated are displayed as:

`N/D`

The TXT report is saved using UTF-8 encoding.

---

## Generated JSON Analysis

The JSON file contains the complete structured sales-analysis result.

Before serialization, pandas DataFrames are converted into JSON-compatible structures.

Standard structured analyses include:

* `product_summary`
* `category_summary`
* `monthly_summary`
* `monthly_best_selling_product`
* `monthly_highest_income_category`

Optional analyses include:

* `city_summary`
* `payment_method_summary`

Missing pandas values are converted into JSON-compatible null values.

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

The CSV-path dictionary uses:

```text
resumen_producto
resumen_categoria
resumen_mensual
resumen_mejores_vendidos_por_mes
resumen_categoria_mayor_ingreso_por_mes
```

Optional entries are:

```text
ciudad_resumen
metodo_de_pago_resumen
```

The physical filename suffixes include:

```text
_productos.csv
_categorias.csv
_meses.csv
_producto_top_mensual.csv
_categoria_top_ingreso_mensual.csv
_ciudades.csv
_metodos_pago.csv
```

City and payment-method CSV files are generated only when their corresponding analyses are available.

---

## Generated XLSX Workbook

The application generates a structured Excel workbook using `openpyxl`.

The workbook contains structured sales, ranking, monthly, and validation information.

Standard worksheets include:

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

Optional worksheets can include:

* `Resumen por ciudad`
* `Resumen por método de pago`

The generated XLSX file can be opened from the graphical interface through the operating system's associated application.

---

## Generated PNG Charts

Automatic chart generation is handled by:

`chart_manager`

Charts are generated as bar charts using pandas and Matplotlib.

Generated images use:

* PNG format.
* 150 DPI.
* Custom titles.
* Custom axis labels.
* 90-degree x-axis label rotation.
* Automatic layout adjustment through `tight_layout()`.

The standard workflow generates ten charts.

### Standard Charts

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

They represent:

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

When `city_summary` is available:

```text
grafica_ingreso_ciudad
grafica_unidades_ciudad
```

represent:

* Income by city.
* Units sold by city.

### Optional Payment-Method Charts

When `payment_method_summary` is available:

```text
grafica_ingreso_metodo_pago
grafica_unidades_metodo_pago
```

represent:

* Income by payment method.
* Units sold by payment method.

The application therefore generates:

* 10 charts without optional analysis.
* 12 charts when one optional analysis is available.
* 14 charts when both optional analyses are available.

Generated chart paths are returned through:

`reports_path_charts`

---

## Generated PDF Report

PDF generation is handled by:

`pdf_reporter`

using ReportLab.

The PDF receives:

* Complete `analysis_result`.
* Output directory.
* Shared report base filename.
* Original source CSV path.
* Complete validation result.
* Generated chart paths.

The generated PDF uses:

`letter`

page size.

The report includes:

* A title derived from the source CSV filename.
* General sales summary.
* Structured analysis tables.
* Generated PNG charts.
* Validation errors.
* Validation warnings.

### PDF General Summary

The PDF general summary displays:

* Total rows.
* Valid rows.
* Invalid rows.
* Total income.
* Units sold.

### PDF Analysis Tables

Supported lists and pandas DataFrames from `analysis_result` are converted into ReportLab tables.

Empty structures are skipped.

Missing table values are represented as:

`N/D`

Table headers are normalized into human-readable text.

The PDF uses translated Spanish section names for known analysis structures.

### PDF Charts

Previously generated chart PNG files are embedded directly in the PDF.

The PDF reporter does not recreate charts.

The workflow therefore requires:

```text
Chart Generation
      |
      v
PNG paths
      |
      v
PDF Generation
```

### PDF Validation Information

Validation errors are ordered by line number.

Validation warnings are also included in the final document.

### PDF Filename

The PDF uses the same shared base filename as the remaining report outputs:

```text
<shared_base_filename>.pdf
```

The generated path is returned through:

`report_path_pdf`

---

## Graphical Report Access

After successful processing, the graphical interface displays generated output information.

TXT, JSON, and CSV files are displayed through independent read-only:

`FileViewerWindow`

instances.

CSV summaries can be selected through:

`csv_combobox`

Generated CSV paths are displayed inside a scrollable area.

The XLSX workbook is opened through:

`QDesktopServices`

using the operating system's associated application.

The generated PDF report is also opened through:

`QDesktopServices`

The main interface verifies the PDF file exists before attempting to open it.

Generated chart names are added to:

`chart_combobox`

Their paths are stored in:

`charts_paths`

The selected chart can be opened through the operating system.

The graphical interface additionally provides direct access to the configured output directory.

---

## Sales Dashboard

The application includes a dedicated:

`DashboardWindow`

for displaying sales-analysis information visually.

The dashboard receives:

```python
DashboardWindow(
    analysis_result,
    chart_paths
)
```

It does not read or analyze the source CSV again.

It reuses the analysis already calculated during report generation.

The window is configured as:

```text
Title: Panel de ventas
Width: 1500
Height: 900
```

### General KPI Cards

The dashboard currently displays:

* `INGRESO TOTAL`
* `UNIDADES VENDIDAS`
* `FILAS VÁLIDAS`
* `FILAS INVÁLIDAS`

These values originate from:

```text
total_income
total_units_sold
total_valid_rows
total_invalid_rows
```

### Best-Result Cards

The dashboard also displays:

* Best-selling product.
* Highest-income product.
* Highest-income category.

The underlying analysis structures preserve tied records, allowing multiple products or categories to be displayed when they share the same maximum value.

### Interactive Charts

The dashboard contains a `QComboBox` populated from:

`chart_paths`

The selected chart is loaded using:

`QPixmap`

and displayed directly inside the dashboard.

Images are scaled to fit within approximately:

```text
500 × 400
```

while maintaining their original aspect ratio.

Smooth image transformation is used when scaling.

The first available chart is displayed when the chart card is initialized.

Changing the combo-box selection updates the displayed chart immediately.

---

## Dashboard Data Flow

The dashboard relationship can be represented as:

```text
Analyzer
   |
   v
analysis_result
   |
   +-------------------+
   |                   |
   |              Chart Manager
   |                   |
   |                   v
   |               chart_paths
   |                   |
   +---------+---------+
             |
             v
       SalesReportWindow
             |
             v
       DashboardWindow
        /     |      \
       v      v       v
     KPIs  Results  Charts
```

No sales metrics are recalculated when the dashboard is opened.

---

## Analysis Features

The analysis module provides the structures used by reports, exported files, charts, PDF generation, and the dashboard.

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

The analysis module calculates these values once before they are passed to presentation and export modules.

---

## Monthly Analysis

The current monthly summary contains:

```text
mes
filas_validas
unidades_vendidas
ingreso_total
crecimiento_ingreso
crec_ingreso_pct
crecimiento_unidades
crec_unidades_pct
```

Monthly records are sorted chronologically.

Growth values compare each month against the immediately preceding month.

The application also generates:

`monthly_best_selling_product`

and:

`monthly_highest_income_category`

These structures preserve ties when multiple records share the corresponding monthly maximum.

---

## Validation

The application validates required sales information before analysis.

Required columns are:

```text
producto_id
producto
categoria
precio
cantidad
fecha
```

The validation workflow includes:

* Empty-value validation.
* Numeric price validation.
* Positive price validation.
* Integer quantity validation.
* Positive quantity validation.
* Exact `YYYY-MM-DD` date-format validation.
* Calendar-date validation.

Valid and invalid records are separated before analysis.

Only valid records are used for sales calculations.

---

## Validation Warnings

Warnings represent non-critical conditions that do not invalidate the corresponding sales row.

The current warning system includes:

`inconsistent_product_name`

Warnings are preserved separately from validation errors and can appear in:

* TXT reports.
* XLSX reports.
* PDF reports.

---

## Application Status and Errors

The graphical interface provides status messages throughout the application workflow.

The status area informs the user about events such as:

* CSV file selection.
* Output-folder selection.
* Start of processing.
* Missing source-file selection.
* Successful report generation.
* Successful chart generation.
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
* Chart-generation failures.
* PDF-generation failures.

Chart-generation failures use:

`ChartGenerationError`

PDF-generation failures use:

`PDFGenerationError`

When an application-specific or unexpected exception occurs during the graphical generation workflow, the interface updates the application status and displays the corresponding error through a critical message box.

The graphical application remains open so the user can correct the problem and try again.

---

## Output Directory Access

After successful report generation, the graphical interface enables:

`Abrir carpeta de salida`

The configured directory is opened through the platform-specific mechanism:

* Windows: `os.startfile()`
* macOS: `open`
* Linux and compatible systems: `xdg-open`

This allows generated report files to be accessed directly from the desktop application.

---

## Current Development State — Version 3.0

Version **3.0** is the currently documented project version.

The current application includes:

* Modular Python architecture.
* PySide6 graphical desktop interface.
* Source CSV selection.
* Custom output-directory selection.
* Default `reports/` directory.
* CSV source-file validation.
* Data normalization.
* Record validation.
* Validation errors.
* Non-critical warnings.
* General sales metrics.
* Product summaries.
* Category summaries.
* Optional city analysis.
* Optional payment-method analysis.
* Tie-preserving maximum-value detection.
* Generic Top 5 ranking logic.
* Monthly sales analysis.
* Monthly income growth.
* Monthly unit-sales growth.
* Monthly percentage growth.
* Monthly best-selling products.
* Monthly highest-income categories.
* Human-readable TXT reporting.
* Structured JSON export.
* Five standard CSV exports.
* Optional city CSV export.
* Optional payment-method CSV export.
* Multi-sheet XLSX workbook generation.
* Automatic PNG chart generation.
* Ten standard charts.
* Up to four optional charts.
* PDF report generation.
* PDF analysis tables.
* PDF embedded charts.
* PDF validation errors.
* PDF validation warnings.
* Read-only TXT viewing.
* Read-only JSON viewing.
* Read-only CSV viewing.
* Operating-system XLSX opening.
* Operating-system PDF opening.
* Operating-system PNG opening.
* Interactive sales dashboard.
* General KPI dashboard cards.
* Best-result dashboard cards.
* Tie-preserving dashboard presentation.
* Interactive dashboard chart selector.
* In-window PNG chart rendering through `QPixmap`.
* Reuse of `analysis_result` without recalculation.
* Controller dual return: `reports, analysis_result`.
* Dynamic source-based filenames.
* Custom application-specific exception hierarchy.
* Dedicated `ChartGenerationError`.
* Dedicated `PDFGenerationError`.
* Output-directory access.
* Cross-platform output-folder opening.
* Execution-time measurement.
* Console execution workflow.

The project remains organized so validation, analysis, presentation, storage, chart generation, PDF generation, dashboard visualization, graphical interaction, and workflow orchestration are handled by independent modules.

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
* PDF-generation failures.

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

`No se pudo generar el archivo PDF.`

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
* `PDFGenerationError`: Raised when the PDF report cannot be generated.

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

##### PDF Generation

PDF-generation failures are represented by:

* `PDFGenerationError`

This exception is used when the PDF report cannot be generated successfully.

PDF-generation failures remain separate from `ReportGenerationError`, `ReportSaveError`, and `ChartGenerationError`, allowing the application to distinguish PDF-specific failures from other report-generation, file-storage, and chart-generation operations.

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

When an `AppError` occurs during report, chart, or PDF generation, the GUI can display its Spanish error message directly to the user.

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

The same behavior applies to PDF-generation errors.

For example:

```python
raise PDFGenerationError()
```

uses:

`No se pudo generar el archivo PDF.`

A custom PDF-related message can also be supplied when more specific context is required.

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
├── ChartGenerationError
└── PDFGenerationError
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
* Representing PDF-generation failures.

This module is not responsible for:

* Detecting every error condition directly.
* Displaying graphical error dialogs.
* Logging errors.
* Recovering automatically from failed operations.
* Validating source files directly.
* Generating reports.
* Generating charts.
* Generating PDF files.

Those responsibilities belong to the modules that detect, raise, catch, or present the corresponding exceptions.

---

### File Validation and Data Normalization Module

The file validation and data normalization module prepares the source CSV file and its raw sales data for the processing workflow.

It validates the physical input file, normalizes string values inside pandas `DataFrame` objects, applies independent critical validation rules, separates valid and invalid records, and collects validation errors and non-critical warnings.

Each validation rule is implemented in a separate helper function. This modular structure keeps the validation process easier to maintain, test, modify, and extend.

The module also supports optional fields such as `ciudad` and `metodo_pago`. These columns are preserved and normalized when present without being required for the core validation workflow.

The module currently provides the following functions:

* `validate_csv_file()`
* `normalize_dataframe()`
* `validated_empty_values()`
* `validated_price()`
* `validated_amount()`
* `validated_date()`
* `detect_warnings()`
* `validate_dataframe()`

#### Required Columns

The validation process requires the following columns:

* `producto_id`
* `producto`
* `categoria`
* `precio`
* `cantidad`
* `fecha`

These columns are defined in:

`REQUIRED_COLUMNS`

All required columns must be present before record-level validation begins.

#### Optional Columns

The current validation workflow supports the following optional columns:

* `ciudad`
* `metodo_pago`

These columns are not required for the validation process.

When present, they are preserved and normalized together with the required sales data.

They are later available to the analysis workflow for optional city and payment-method summaries.

#### File Validation Process

The `validate_csv_file()` function validates the physical source file before the CSV-reading stage.

It performs the following checks:

1. Verifies that the provided path is not `None` or empty.
2. Converts the string path into a `Path` object.
3. Confirms that the path exists in the file system.
4. Ensures that the path points to a regular file rather than a directory.
5. Verifies that the file extension is `.csv`.
6. Ensures that the file contains at least one byte.
7. Opens the file in binary mode.
8. Reads one byte to verify physical readability.
9. Returns the validated `Path` object.

File readability is checked using binary mode.

This step verifies only that the file can be physically accessed and read.

It does not:

* Decode the CSV contents.
* Parse CSV rows.
* Validate CSV syntax.
* Convert the file into a pandas `DataFrame`.

Those responsibilities belong to the CSV-reading module.

If the file cannot be opened or read because of a file-system error, the original `OSError` is converted into:

`FileReadError`

#### Data Normalization Process

The `normalize_dataframe()` function creates a copy of the raw DataFrame before applying normalization rules.

The original DataFrame is therefore preserved.

The required fields are normalized as follows.

##### `producto_id`

The function:

* Removes all whitespace.
* Converts the value to uppercase.

For example:

```text
p001  →  P001
```

Whitespace is removed through a regular expression rather than only trimming the beginning and end.

##### `producto`

The function:

* Replaces repeated whitespace with a single space.
* Removes leading whitespace.
* Removes trailing whitespace.

##### `categoria`

The function:

* Replaces repeated whitespace with a single space.
* Removes leading whitespace.
* Removes trailing whitespace.

##### `precio`

All whitespace is removed from the value.

##### `cantidad`

All whitespace is removed from the value.

##### `fecha`

All whitespace is removed from the value.

##### `ciudad`

When the optional `ciudad` column exists, the function:

* Replaces repeated whitespace with a single space.
* Removes leading whitespace.
* Removes trailing whitespace.

##### `metodo_pago`

When the optional `metodo_pago` column exists, the function:

* Replaces repeated whitespace with a single space.
* Removes leading whitespace.
* Removes trailing whitespace.

After normalization, a new DataFrame is returned without modifying the original input.

#### Independent Validation Functions

Critical record validation is divided into four independent helper functions:

* `validated_empty_values()`
* `validated_price()`
* `validated_amount()`
* `validated_date()`

Each function returns a dictionary containing:

* `invalid_indexes`
* `errors`

`invalid_indexes` identifies DataFrame rows containing critical validation failures.

`errors` contains detailed information describing each detected failure.

A single row can produce more than one validation error.

#### Empty-Value Validation

The `validated_empty_values()` function checks every column listed in:

`REQUIRED_COLUMNS`

An error is generated whenever a required field contains an empty string.

Each error contains:

* `line_number`
* `column`
* `error_type`
* `message`
* `original_value`

The error type is:

`empty_value`

The corresponding DataFrame row index is also added to:

`invalid_indexes`

#### CSV Line Numbers

Validation errors use CSV-oriented line numbers rather than zero-based DataFrame indexes.

The reported line number is calculated as:

```text
DataFrame index + 2
```

The additional two positions account for:

* Python's zero-based DataFrame index.
* The CSV header row.

For example, DataFrame index:

`0`

is reported as CSV line:

`2`

#### Price Validation

The `validated_price()` function validates non-empty values from:

`precio`

Empty values are skipped because they have already been handled by:

`validated_empty_values()`

A valid price must:

* Be convertible to a numeric value.
* Be greater than zero.

The function can generate the following error types.

##### `invalid_number`

Generated when the price cannot be converted into a numeric value.

##### `negative_or_zero_value`

Generated when the numeric price is:

* Zero.
* Negative.

Rows containing either error are added to:

`invalid_indexes`

#### Quantity Validation

The `validated_amount()` function validates non-empty values from:

`cantidad`

Empty values are handled separately by:

`validated_empty_values()`

A valid quantity must:

* Be convertible to a number.
* Represent a whole number.
* Be greater than zero.

Decimal quantities are not accepted.

The function can generate the following error types.

##### `decimal_not_allowed`

Generated when a numeric quantity contains a decimal component.

##### `negative_or_zero_value`

Generated when the quantity is zero or negative.

##### `invalid_integer`

Generated when the value cannot be interpreted as a numeric quantity.

Rows containing these errors are added to:

`invalid_indexes`

#### Date Validation

The `validated_date()` function validates non-empty values from:

`fecha`

Empty values are handled separately by:

`validated_empty_values()`

Date validation occurs in two stages.

##### Format Validation

The value must match:

```text
YYYY-MM-DD
```

The format is checked using the regular expression:

```text
^\d{4}-\d{2}-\d{2}$
```

Values that do not match the required structure generate:

`invalid_date_format`

##### Calendar Validation

Values with the correct text structure are passed to:

`pd.to_datetime()`

using:

```text
%Y-%m-%d
```

This verifies that the supplied date actually exists in the calendar.

For example, a structurally correct but nonexistent date is rejected.

The resulting error type remains:

`invalid_date_format`

#### Warning Detection

The `detect_warnings()` function analyzes records that already passed all critical validation rules.

Warnings represent non-critical inconsistencies and do not cause rows to become invalid.

The current implementation detects:

`inconsistent_product_name`

#### Inconsistent Product Names

Valid rows are grouped by:

`producto_id`

The function verifies whether each product identifier is associated with only one product name.

When the same `producto_id` appears with multiple different product names, the function generates a warning containing:

* `warning_type`
* `field`
* `message`
* `affected_value`
* `details`

The warning type is:

`inconsistent_product_name`

The affected field is:

`producto`

`affected_value` contains the corresponding:

`producto_id`

`details` contains the different product names associated with that identifier.

Repeated names are removed from the details while preserving their original encounter order.

These warnings do not invalidate the corresponding sales rows.

#### DataFrame Validation Process

The `validate_dataframe()` function coordinates the complete DataFrame-validation workflow.

It performs the following operations:

1. Verifies that the input DataFrame is not empty.
2. Confirms that all columns listed in `REQUIRED_COLUMNS` are present.
3. Normalizes the raw sales data.
4. Preserves and normalizes supported optional columns when present.
5. Executes `validated_empty_values()`.
6. Collects empty-value errors and invalid indexes.
7. Executes `validated_price()`.
8. Collects price errors and invalid indexes.
9. Executes `validated_amount()`.
10. Collects quantity errors and invalid indexes.
11. Executes `validated_date()`.
12. Collects date errors and invalid indexes.
13. Removes duplicate invalid indexes.
14. Sorts the invalid indexes.
15. Separates valid and invalid records.
16. Converts valid `precio` values into numeric values.
17. Converts valid `cantidad` values into numeric values.
18. Converts valid `fecha` values into pandas datetime values.
19. Executes `detect_warnings()` using only valid records.
20. Collects non-critical warnings.
21. Calculates validation totals.
22. Returns the complete validation result.

#### Duplicate Invalid Indexes

A single sales record may violate multiple validation rules.

For example, the same row could contain:

* An invalid price.
* An invalid quantity.
* An invalid date.

This can cause the same row index to appear multiple times while the individual validation helpers are running.

Before separating valid and invalid rows, the workflow removes duplicate indexes.

This ensures that each invalid sales record appears only once inside:

`df_invalid_rows`

while all individual error records remain available inside:

`errors`

#### Valid and Invalid Records

After all critical validations have been completed, records are separated according to their indexes.

Valid records are stored in:

`df_valid_rows`

Invalid records are stored in:

`df_invalid_rows`

Rows containing at least one critical validation error are excluded from the valid DataFrame.

Warnings do not move rows into the invalid DataFrame.

#### Valid-Record Type Conversion

After invalid records have been removed, the following valid columns are converted into numeric pandas values:

* `precio`
* `cantidad`

The conversion is performed through:

`pd.to_numeric()`

Valid dates are converted through:

`pd.to_datetime()`

using the expected:

`YYYY-MM-DD`

format.

Type conversion occurs only on:

`df_valid_rows`

#### Validation Result

The `validate_dataframe()` function returns a dictionary containing:

* `df_valid_rows`: DataFrame containing records that passed all critical validation rules.
* `df_invalid_rows`: DataFrame containing records with one or more critical validation errors.
* `errors`: Flat list containing all detailed validation errors.
* `warnings`: Flat list containing non-critical data inconsistencies.
* `total_rows`: Total number of normalized sales records.
* `total_valid_rows`: Number of records that passed validation.
* `total_invalid_rows`: Number of records containing at least one critical validation error.

Optional columns present in the source CSV are preserved inside the resulting valid and invalid DataFrames.

#### Validation Result Structure

The returned structure follows this general form:

```python
{
    "df_valid_rows": DataFrame(...),
    "df_invalid_rows": DataFrame(...),
    "errors": [
        ...
    ],
    "warnings": [
        ...
    ],
    "total_rows": ...,
    "total_valid_rows": ...,
    "total_invalid_rows": ...
}
```

#### Error Structure

A validation error follows this general structure:

```python
{
    "line_number": 2,
    "column": "precio",
    "error_type": "invalid_number",
    "message": "...",
    "original_value": "..."
}
```

Depending on the validation rule, supported error types include:

* `empty_value`
* `invalid_number`
* `negative_or_zero_value`
* `decimal_not_allowed`
* `invalid_integer`
* `invalid_date_format`

#### Warning Structure

The current warning structure follows this general form:

```python
{
    "warning_type": "inconsistent_product_name",
    "field": "producto",
    "message": "...",
    "affected_value": "P001",
    "details": [
        "Producto A",
        "Producto B"
    ]
}
```

#### Input and Output

##### `validate_csv_file()`

* **Input:** String containing the source CSV file path.
* **Output:** Validated `Path` ready for the CSV-reading process.

##### `normalize_dataframe()`

* **Input:** Raw pandas DataFrame containing sales data as strings.
* **Output:** New DataFrame containing normalized values while preserving supported optional columns.

##### `validated_empty_values()`

* **Input:** Normalized sales DataFrame.
* **Output:** Dictionary containing empty-value errors and invalid row indexes.

##### `validated_price()`

* **Input:** Normalized sales DataFrame.
* **Output:** Dictionary containing price-validation errors and invalid row indexes.

##### `validated_amount()`

* **Input:** Normalized sales DataFrame.
* **Output:** Dictionary containing quantity-validation errors and invalid row indexes.

##### `validated_date()`

* **Input:** Normalized sales DataFrame.
* **Output:** Dictionary containing date-validation errors and invalid row indexes.

##### `detect_warnings()`

* **Input:** DataFrame containing records that passed critical validation.
* **Output:** Dictionary containing non-critical product-name warnings.

##### `validate_dataframe()`

* **Input:** Raw pandas DataFrame containing sales records as strings.
* **Output:** Dictionary containing valid rows, invalid rows, errors, warnings, and validation totals.

#### Related Exceptions

The module may raise the following application-specific exceptions:

* `EmptyPathError`
* `FileNotFoundAppError`
* `InvalidFilePathError`
* `InvalidFileExtensionError`
* `EmptyFileError`
* `FileReadError`
* `EmptyDataFrameError`
* `MissingColumnsError`

#### Module Responsibilities

The validation module is responsible for:

* Validating the physical source CSV path.
* Verifying basic file accessibility.
* Normalizing sales-data strings.
* Verifying required columns.
* Detecting empty required fields.
* Validating prices.
* Validating quantities.
* Validating dates.
* Separating valid and invalid records.
* Converting valid numeric and date values.
* Detecting non-critical product-name inconsistencies.
* Collecting errors and warnings.
* Calculating validation totals.
* Preserving supported optional columns.

The validation module is not responsible for:

* Parsing CSV contents into a DataFrame.
* Calculating sales metrics.
* Calculating rankings.
* Calculating monthly summaries.
* Generating human-readable reports.
* Saving report files.
* Generating charts.
* Displaying graphical interface elements.

Those responsibilities belong to the CSV-reading, analysis, reporting, file-management, chart-management, controller, and graphical-interface modules.

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

The resulting structures are used by report generation, PDF generation, file export, and chart-generation components.

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

* `crec_ingreso_pct`
* `crec_unidades_pct`

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
* `crec_ingreso_pct`: Percentage income change from the previous month.
* `crecimiento_unidades`: Absolute units-sold difference from the previous month.
* `crec_unidades_pct`: Percentage units-sold change from the previous month.

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

```text id="7314xl"
mes
| filas_validas
| unidades_vendidas
| ingreso_total
| crecimiento_ingreso
| crec_ingreso_pct
| crecimiento_unidades
| crec_unidades_pct
```

For example, conceptually:

```text id="qie7ky"
2026-07 | 25 | 84  | 15420.50 | NaN      | NaN    | NaN | NaN
2026-08 | 31 | 102 | 18750.00 | 3329.50  | 21.59  | 18  | 21.43
2026-09 | 18 | 56  | 9320.75  | -9429.25 | -50.29 | -46 | -45.10
```

Growth values compare each month against the immediately preceding month.

The first month contains missing growth values because no previous month is available.

#### Monthly Best-Selling Product Result

The `monthly_best_selling_product` DataFrame follows this structure:

```text id="rbaecg"
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

```text id="cx2z5m"
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
* **Output:** City-summary DataFrame sorted by total income.

##### `get_payment_method_summary()`

* **Input:** Valid sales DataFrame containing `metodo_pago` and `ingreso_fila`.
* **Output:** Payment-method-summary DataFrame sorted by total income.

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

* A list of highest-income records.
* A section title.
* A primary dictionary key.
* An optional secondary dictionary key.

When a secondary key is supplied, both descriptive values are displayed separated by a hyphen.

When no secondary key is supplied, only the primary descriptive field is displayed.

Each formatted record also includes:

* `ingreso_total`
* `unidades_vendidas`

The helper is currently reused for:

* Highest-income products.
* Highest-income categories.
* Highest-income cities.
* Highest-income payment methods.

All tied records supplied by the analysis layer are preserved.

#### Highest-Income Product

The highest-income-product section is generated through:

`get_highest_income()`

using:

* `highest_income_product`
* `producto_id`
* `producto`

The section begins with:

`PRODUCTO CON MAYOR INGRESO`

Each record displays:

* Product identifier.
* Product name.
* Total income.
* Units sold.

#### Highest-Income Category

The highest-income-category section is generated through:

`get_highest_income()`

using:

* `highest_income_category`
* `categoria`

The section begins with:

`CATEGORÍA CON MAYOR INGRESO`

Each record displays:

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

Each record displays:

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

Each record displays:

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

This generic helper is reused for:

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

The monthly formatter calculates one sign for the absolute income variation and one sign for the absolute unit-sales variation.

Those signs are also reused when displaying their corresponding percentage variations.

#### Monthly Summary

The `get_monthly_summary()` function generates a detailed month-by-month sales section.

Unlike the product, category, city, and payment-method summaries, monthly information is not displayed through a direct pandas table.

The DataFrame is first processed using:

`replace({np.nan: None})`

and then converted into individual dictionary records.

This allows missing growth values to be handled explicitly during text formatting.

For every month, the section reads:

* `mes`
* `filas_validas`
* `unidades_vendidas`
* `ingreso_total`
* `crecimiento_ingreso`
* `crec_ingreso_pct`
* `crecimiento_unidades`
* `crec_unidades_pct`

The generated section begins with:

`RESUMEN POR MES`

The current reporter therefore expects the monthly-analysis DataFrame to provide the exact percentage-growth columns:

* `crec_ingreso_pct`
* `crec_unidades_pct`

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

The absolute numeric value is formatted independently while its sign is obtained through:

`get_sign()`

#### Monthly Income Percentage Variation

The percentage income difference is read from:

`crec_ingreso_pct`

and displayed as:

`Variación porcentual de ingreso`

For example:

`+12.45%`

or:

`-8.30%`

Percentage values are displayed with two decimal places.

The sign used for this value follows the sign calculated from:

`crecimiento_ingreso`

#### Monthly Unit Variation

The absolute difference in units sold is read from:

`crecimiento_unidades`

and displayed as:

`Variación de unidades`

For example:

`+25`

or:

`-14`

Unit variations are displayed without decimal places.

#### Monthly Unit Percentage Variation

The percentage difference in units sold is read from:

`crec_unidades_pct`

and displayed as:

`Variación porcentual de unidades`

For example:

`+10.50%`

or:

`-6.75%`

Percentage values are displayed with two decimal places.

The sign used for this value follows the sign calculated from:

`crecimiento_unidades`

#### Missing Monthly Growth Values

The first available month has no previous month against which growth can be calculated.

When a monthly growth value is unavailable, the report displays:

`N/D`

This applies independently to:

* Income variation.
* Income percentage variation.
* Unit variation.
* Unit percentage variation.

pandas `NaN` values are converted into:

`None`

before this presentation logic is applied.

#### Monthly Best-Selling Product

The `get_monthly_best_selling_product()` function generates the section containing the best-selling product or products for every month.

The supplied DataFrame is processed by replacing pandas `NaN` values with:

`None`

and converting its records into dictionaries.

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

Multiple products can be displayed under the same month when the analysis layer identifies a tie for the highest number of units sold.

#### Monthly Highest-Income Category

The `get_monthly_highest_income_category()` function generates the highest-income category or categories for every month.

The supplied DataFrame is processed by replacing pandas `NaN` values with:

`None`

and converting its records into dictionaries.

The generated section begins with:

`CATEGORÍA CON MAYOR INGRESO POR MES`

Records are visually grouped by month.

A month heading is displayed only when the current record belongs to a different month from the previously processed record.

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

Each validation-error record can contain:

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

1. Adds the warning-section title.
2. Detects when no warnings are available.
3. Sorts warnings by `affected_value`.
4. Displays the affected product identifier.
5. Displays the warning type.
6. Displays the warning message.
7. Displays warning details.

Each warning contains information such as:

* `affected_value`
* `warning_type`
* `message`
* `details`

When `details` contains multiple values, they are joined into comma-separated text.

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

The reporter receives previously calculated analysis data and applies presentation formatting only.

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

The reporter centralizes several previously duplicated presentation responsibilities.

`get_highest_income()` handles highest-income formatting for:

* Products.
* Categories.
* Cities.
* Payment methods.

`get_top_5()` handles both supported Top 5 product rankings.

`get_summary()` handles DataFrame-summary formatting for:

* Products.
* Categories.
* Cities.
* Payment methods.

This design keeps presentation rules consistent while reducing duplicated formatting code.

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
* Determine Top 5 rankings.
* Determine highest-income records.
* Determine monthly best-selling products.
* Determine monthly highest-income categories.
* Save report files directly.
* Generate charts.

Those responsibilities belong to the validation, CSV-reading, analysis, file-management, and chart-management modules.

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

It acts as the orchestration layer between the graphical interface and the specialized modules responsible for file validation, CSV reading, DataFrame validation, sales analysis, plain-text report generation, file export, chart generation, and PDF report generation.

The controller receives the source CSV file path and output directory, executes the complete processing pipeline, generates all supported report files and chart images, measures the total execution time, and returns both generated-output information and the complete structured sales-analysis result.

The generated outputs currently include:

* TXT reports.
* JSON analysis files.
* CSV summary files.
* XLSX workbooks.
* PNG chart images.
* PDF reports.

The returned `analysis_result` can also be reused by presentation components such as the graphical sales dashboard without recalculating the sales metrics.

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
14. Generates the PDF report using `pdf_reporter.save_pdf_reporter()`.
15. Stops the execution timer.
16. Calculates the total execution time.
17. Adds the execution time to the generated-output dictionary.
18. Returns both `reports` and `analysis_result` to the caller.

#### Module Coordination

The controller coordinates the following modules:

* `validator`: Validates the source file path, normalizes sales data, validates records, detects warnings, and separates valid and invalid rows.
* `csv_reader`: Reads the validated CSV file and converts its contents into a pandas `DataFrame`.
* `analyzer`: Calculates sales metrics, aggregated summaries, rankings, monthly analysis, growth indicators, and optional analyses.
* `reporter`: Converts analysis results, validation errors, and warnings into a structured plain-text sales report.
* `file_manager`: Generates the shared report base filename and saves TXT, JSON, CSV, and XLSX output files.
* `chart_manager`: Generates PNG chart images from the calculated sales-analysis results.
* `pdf_reporter`: Generates the PDF report using sales-analysis information, validation information, source-file information, and previously generated chart paths.

The controller itself does not implement the internal processing logic of these modules.

Its responsibility is to call them in the correct order, transfer their results between workflow stages, and expose the final generated-output and analysis structures to the caller.

#### Input Configuration

The `generate_sales_report()` function receives:

* `input_file_path`: Source CSV file path represented as a string.
* `output_folder`: Destination directory represented as either `str` or `Path`.

The source path is first validated before being passed to the CSV-reading module.

The output directory is passed to the file, chart, and PDF generation functions responsible for storing generated outputs.

#### Function Return Type

The function is declared as:

```python
def generate_sales_report(
    input_file_path: str,
    output_folder: str | Path
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
```

The returned tuple contains:

1. `reports`: Dictionary containing generated-output paths, processing totals, and execution information.
2. `analysis_result`: Dictionary containing the complete structured sales analysis produced by the analysis module.

This allows generated-file information and analytical information to remain logically separated while both remain available to the graphical layer.

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

Validation errors and warnings are later reused by the plain-text reporter, XLSX export workflow, and PDF-report workflow.

#### Sales Analysis

The controller sends the validation result to:

`analyzer.analyze_sales()`

The resulting:

`analysis_result`

contains the calculated structures required by reporting, file export, chart generation, PDF generation, and dashboard presentation.

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

The same `analysis_result` is reused throughout the remaining workflow and is returned to the caller after all output generation is complete.

#### Analysis Result Reuse

The controller calculates the structured sales analysis only once.

After:

`analyzer.analyze_sales(validation_result)`

returns the result, the same `analysis_result` is reused by:

* Plain-text report generation.
* JSON export.
* CSV export.
* XLSX generation.
* Chart generation.
* PDF generation.
* Graphical dashboard integration.

This avoids re-reading the source CSV or recalculating sales metrics when the graphical dashboard is opened.

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

This shared base filename is reused by:

* TXT export.
* JSON export.
* CSV exports.
* XLSX export.
* PNG chart generation.
* PDF generation.

The exact filename construction rules are defined by the file-management module.

#### Output File Coordination

The controller coordinates generation of the following report files:

* TXT sales report.
* JSON structured analysis.
* CSV analysis summaries.
* XLSX workbook.
* PDF report.

The controller also coordinates:

* PNG chart generation.

All generated paths are collected inside the:

`reports`

dictionary.

The structured analytical data itself remains available separately through:

`analysis_result`

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

The standard CSV export includes:

* Product summary.
* Category summary.
* Monthly summary.
* Monthly best-selling products.
* Monthly highest-income categories.

Optional CSV summaries may also include:

* City summary.
* Payment-method summary.

#### CSV Report Paths

The `reports_path_csv` dictionary uses internal Spanish identifiers for generated summary files.

The standard entries are:

* `resumen_producto`
* `resumen_categoria`
* `resumen_mensual`
* `resumen_mejores_vendidos_por_mes`
* `resumen_categoria_mayor_ingreso_por_mes`

Optional entries are:

* `ciudad_resumen`
* `metodo_de_pago_resumen`

A conceptual structure is:

```python
{
    "resumen_producto": Path(...),
    "resumen_categoria": Path(...),
    "resumen_mensual": Path(...),
    "resumen_mejores_vendidos_por_mes": Path(...),
    "resumen_categoria_mayor_ingreso_por_mes": Path(...),

    # Optional
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

Chart-generation logic remains inside the dedicated `chart_manager` module rather than the controller.

The chart-generation stage occurs before PDF generation because the PDF workflow receives the generated chart-path dictionary.

The same chart-path dictionary is later available to the graphical interface and can be reused by the sales dashboard.

#### PDF Report Coordination

The PDF report is generated using:

`pdf_reporter.save_pdf_reporter()`

The function receives:

* Complete `analysis_result`.
* Configured output folder.
* Shared base filename.
* Validated source-file `Path`.
* Complete `validation_result`.
* Generated chart-path dictionary.

The chart dictionary passed to the PDF reporter is:

`reports["reports_path_charts"]`

The resulting PDF path is stored as:

`report_path_pdf`

Conceptually, the call follows this structure:

```python
reports["report_path_pdf"] = pdf_reporter.save_pdf_reporter(
    analysis_result,
    output_folder,
    file_name,
    file_path,
    validation_result,
    reports["reports_path_charts"]
)
```

Because the PDF reporter receives `reports_path_charts`, chart generation must be completed before the PDF-generation stage.

The internal layout and formatting of the PDF remain the responsibility of the dedicated `pdf_reporter` module.

#### Generated-Output Dictionary

The first value returned by:

`generate_sales_report()`

is:

`reports`

This dictionary contains information about generated files and the completed workflow.

It contains:

* `total_rows`: Total number of processed sales records.
* `total_valid_rows`: Number of records that passed validation.
* `total_invalid_rows`: Number of records containing validation errors.
* `report_path_txt`: Path pointing to the generated TXT report.
* `report_path_json`: Path pointing to the generated JSON analysis.
* `reports_path_csv`: Dictionary containing generated CSV summary paths.
* `report_path_xlsx`: Path pointing to the generated XLSX workbook.
* `reports_path_charts`: Dictionary containing generated PNG chart paths.
* `report_path_pdf`: Path pointing to the generated PDF report.
* `execution_time`: Formatted string containing the total workflow execution time.

#### Generated-Output Structure

A simplified `reports` dictionary follows this structure:

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
        "resumen_mejores_vendidos_por_mes": Path(...),
        "resumen_categoria_mayor_ingreso_por_mes": Path(...),

        # Optional
        "ciudad_resumen": Path(...),
        "metodo_de_pago_resumen": Path(...)
    },

    "report_path_xlsx": Path(...),

    "reports_path_charts": {
        "...": Path(...),
        "...": Path(...)
    },

    "report_path_pdf": Path(...),

    "execution_time": "Execution time: 0.0123 seconds"
}
```

The city and payment-method CSV entries are optional.

The exact chart keys are determined by the chart-generation module.

#### Structured Analysis Result

The second value returned by:

`generate_sales_report()`

is:

`analysis_result`

This is the original structured dictionary produced by:

`analyzer.analyze_sales(validation_result)`

It is returned separately from `reports` so presentation components can access the calculated sales information directly without reading exported files or repeating the analysis.

The structure can contain:

* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`
* `total_income`
* `total_units_sold`
* `product_summary`
* `category_summary`
* `monthly_summary`
* `best_selling_product`
* `highest_income_product`
* `highest_income_category`
* `top_5_best_selling_products`
* `top_5_highest_income_products`
* `monthly_best_selling_product`
* `monthly_highest_income_category`

Optional entries can include:

* `city_summary`
* `highest_income_city`
* `payment_method_summary`
* `highest_income_payment_method`

The exact analytical structure is defined by the sales-analysis module.

#### Controller Return Structure

The complete return value follows this conceptual structure:

```python
return reports, analysis_result
```

or conceptually:

```text
generate_sales_report()
        |
        +---- reports
        |       |
        |       +-- processing totals
        |       +-- TXT path
        |       +-- JSON path
        |       +-- CSV paths
        |       +-- XLSX path
        |       +-- PNG chart paths
        |       +-- PDF path
        |       +-- execution time
        |
        +---- analysis_result
                |
                +-- general metrics
                +-- product summaries
                +-- category summaries
                +-- rankings
                +-- monthly analysis
                +-- optional city analysis
                +-- optional payment-method analysis
```

This separation allows the caller to use generated-file information and structured analytical data independently.

#### GUI Integration

The controller acts as the primary backend entry point used by the graphical interface.

The GUI calls:

`controller.generate_sales_report()`

and provides:

* Selected source CSV path.
* Configured output directory.

The graphical interface receives both returned dictionaries.

Conceptually:

```python
self.data_analysis, self.analysis_result = control.generate_sales_report(
    self.file_path,
    self.output_folder
)
```

The first returned dictionary is stored by the GUI as:

`data_analysis`

and provides generated-output information such as:

* `report_path_txt`
* `report_path_json`
* `reports_path_csv`
* `report_path_xlsx`
* `reports_path_charts`
* `report_path_pdf`
* `execution_time`

The second returned dictionary is stored as:

`analysis_result`

and contains the structured sales data calculated by the backend.

The controller does not determine how generated outputs or analytical information are displayed by the graphical interface.

This keeps the graphical interface separated from backend processing details.

#### Dashboard Integration

The controller does not create or display the graphical dashboard.

Instead, it exposes the already calculated:

`analysis_result`

to the GUI.

The GUI can then pass this structured analysis, together with generated chart paths, to the dedicated dashboard window.

Conceptually:

```text
analyzer.analyze_sales()
          |
          v
    analysis_result
          |
          +--------------------------+
          |                          |
          v                          v
Report/File Generation          GUI Dashboard
```

This allows the dashboard to reuse the same analysis performed during report generation without:

* Re-reading the CSV file.
* Re-validating the records.
* Recalculating sales totals.
* Recalculating rankings.
* Recalculating monthly metrics.

The controller therefore acts as the connection point between backend analysis and presentation-layer reuse.

#### Execution Time

The controller uses:

`time.perf_counter()`

to measure the duration of the complete workflow.

Timing begins before source-file validation and ends only after all configured outputs have been generated.

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
* PDF generation and storage.

The final duration is calculated as:

`end - start`

and formatted in seconds with four decimal places.

For example:

`Execution time: 0.0123 seconds`

The execution time is stored inside the:

`reports`

dictionary.

It is not added separately to:

`analysis_result`

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
* PDF generation.

are propagated to the caller.

Application-specific exceptions can then be handled by the graphical interface.

Unexpected Python exceptions may also propagate to the GUI, where they can be presented through the application's error-handling workflow.

#### Input and Output

##### `generate_sales_report()`

* **Input:** Source CSV path as `str` and destination output directory as `str | Path`.
* **Output:** `Tuple[Dict[str, Any], Dict[str, Any]]` containing:

  * A generated-output dictionary with processing totals, TXT, JSON, CSV, XLSX, PNG chart, and PDF paths, together with total execution time.
  * The complete structured `analysis_result` generated by the sales-analysis module.

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
* Coordinating PDF generation.
* Ensuring charts are generated before the PDF stage that consumes their paths.
* Measuring the total workflow execution time.
* Collecting generated-output paths and processing information in `reports`.
* Returning `reports` to the caller.
* Returning the complete `analysis_result` to the caller.
* Making the existing structured analysis available for presentation-layer reuse.

The controller is not responsible for:

* Implementing CSV parsing logic.
* Performing individual validation rules.
* Calculating sales metrics directly.
* Formatting the plain-text report directly.
* Creating report files directly.
* Drawing chart images directly.
* Building the PDF report layout directly.
* Building the dashboard interface.
* Displaying graphical interface elements.
* Handling user interaction.

Those responsibilities belong to the specialized backend modules and graphical interface.

---

### Graphical User Interface Module

The graphical user interface module provides the main desktop window for the Sales Report application using PySide6.

It allows the user to select a source CSV file, choose an output directory, generate sales reports and charts through the backend controller, inspect generated TXT, JSON, CSV, XLSX, and PDF files, open generated PNG charts, access an interactive sales dashboard, and open the configured output directory directly from the application.

TXT, JSON, and CSV files are displayed through dedicated read-only `FileViewerWindow` instances.

XLSX files, PDF reports, and generated PNG charts are opened through the operating system's associated applications using `QDesktopServices`.

The generated structured sales analysis and chart paths can also be passed to a dedicated `DashboardWindow` for interactive sales visualization.

The graphical layer separates widget creation, signal connection, layout construction, event handling, output access, dashboard access, and generated-result state management into independent methods.

This structure reduces duplicated interface code and keeps the module modular, maintainable, and easier to extend.

The graphical interface and user-facing messages are displayed in Spanish, while the project source code and technical documentation are maintained in English.

The module currently provides the following class:

* `SalesReportWindow`

#### Main Window

The `SalesReportWindow` class inherits from PySide6 `QMainWindow` and represents the main desktop window of the application.

The window is configured with:

* Title: `Generador de Reportes de Ventas`
* Width: `900`
* Height: `1000`
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
* `pdf_path`: `None`
* `analysis_result`: `None`
* `data_analysis`: `None`

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
15. Adds the sales-dashboard access button.
16. Disables generated-output controls through `off_buttons()`.
17. Assigns the completed layout to the central widget.

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
* `build_pdf_layout()`
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
* `open_report_pdf()`
* `open_chart_graphic()`
* `open_output_folder()`
* `open_dashboard()`

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
* PDF report information.

Generated TXT, JSON, XLSX, and PDF path labels are initially empty and are populated after successful report generation.

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
* Opening the PDF report.
* Opening the selected generated chart.
* Opening the output directory.
* Opening the sales dashboard.

The dashboard-access button is displayed as:

`Abrir panel de ventas`

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
* `button_pdf_show_report` → `open_report_pdf()`
* `button_open_dashboard` → `open_dashboard()`

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
8. Sales-dashboard access.

The report and chart areas are organized through dedicated layouts and group boxes, while output-folder and dashboard access buttons are added directly to the main application layout.

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
2. Previously stored TXT, JSON, CSV, XLSX, PDF, and chart paths are cleared.
3. Previously stored controller and structured-analysis results are cleared.
4. Previously displayed generated-report and chart information is removed.
5. The selected path is stored in `file_path`.
6. The selected-file label is updated.
7. The application status is updated according to the currently configured output directory.

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
2. Previously stored TXT, JSON, CSV, XLSX, PDF, and chart paths are cleared.
3. Previously stored controller and structured-analysis results are cleared.
4. Previously displayed generated-report and chart information is removed.
5. The selected directory is stored in `output_folder`.
6. The output-folder label is updated.
7. The application status is updated according to whether a source CSV file has already been selected.

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
6. Clears stored TXT, JSON, CSV, XLSX, PDF, and chart paths.
7. Clears previous controller-result and structured-analysis state.
8. Clears previously displayed output information.
9. Calls `controller.generate_sales_report()`.
10. Receives the controller result and structured sales-analysis result.
11. Stores the generated-output information in `data_analysis`.
12. Stores the structured sales-analysis information in `analysis_result`.
13. Stores and displays the generated TXT report path.
14. Stores and displays the generated JSON analysis path.
15. Stores and displays the generated XLSX report path.
16. Stores and displays the generated PDF report path.
17. Adds generated CSV summary names to the CSV selector.
18. Creates labels containing generated CSV paths.
19. Stores CSV summary names and paths in `csv_paths`.
20. Adds generated chart names to the chart selector.
21. Creates labels containing generated chart paths.
22. Stores chart names and paths in `charts_paths`.
23. Updates the application status after successful generation.
24. Enables generated-output and dashboard controls.
25. Displays application-specific or unexpected errors when necessary.
26. Re-enables the report-generation button after processing.

#### Controller Result Storage

The report-generation call currently assigns two returned structures:

```python
self.data_analysis, self.analysis_result = control.generate_sales_report(
    self.file_path,
    self.output_folder
)
```

`data_analysis` contains the generated-output information used by the graphical interface.

The GUI currently reads the following entries from `data_analysis`:

* `report_path_txt`
* `report_path_json`
* `reports_path_csv`
* `report_path_xlsx`
* `reports_path_charts`
* `report_path_pdf`

`analysis_result` contains the structured sales-analysis result used by the dashboard.

Keeping both structures available allows the main window to handle generated files while also supplying analytical information to `DashboardWindow`.

#### Backend Controller Integration

The GUI delegates the complete backend workflow to:

`controller.generate_sales_report()`

The graphical interface provides:

* `file_path`
* `output_folder`

The resulting information is stored separately as:

* `data_analysis`: Generated report paths and controller output information.
* `analysis_result`: Structured sales-analysis information.

The backend remains responsible for validation, reading, analysis, report generation, chart generation, PDF generation, and file storage.

The GUI uses these returned structures for output access and dashboard presentation rather than recalculating backend metrics itself.

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
* PDF reports.
* CSV summaries.
* Scrollable CSV path information.

The output-directory and dashboard buttons are not part of this group box. They are added separately to the main application layout.

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

#### PDF Report Layout

The `build_pdf_layout()` method creates the PDF report controls.

It contains:

* PDF section label.
* Generated PDF path.
* `Ver PDF` button.

The PDF report is opened externally through the operating system.

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

#### PDF Report Access

The generated PDF report path is stored in:

`pdf_path`

The:

`Ver PDF`

button calls:

`open_report_pdf()`

PDF reports are not displayed through `FileViewerWindow`.

The method first verifies that the PDF file exists.

If the file does not exist, a warning `QMessageBox` is displayed with:

`El archivo PDF no existe`

If the file exists, its path is converted into a local `QUrl` and opened through:

`QDesktopServices.openUrl()`

This allows the operating system to launch the application associated with PDF files.

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

The same chart-path dictionary is later supplied to the sales dashboard.

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

#### Sales Dashboard Access

The:

`Abrir panel de ventas`

button calls:

`open_dashboard()`

The dashboard button is enabled only after a report-generation process completes successfully.

The `open_dashboard()` method creates:

`DashboardWindow`

using:

* `analysis_result`
* `charts_paths`

Conceptually:

```python
self.ds_window = ds.DashboardWindow(
    self.analysis_result,
    self.charts_paths
)
```

The dashboard window reference is stored in:

`ds_window`

and displayed through:

```python
self.ds_window.show()
```

The main GUI therefore acts as the connection point between the completed backend analysis and the dashboard presentation layer.

The dashboard does not trigger a new report-generation process. It uses the structured analysis and chart paths already available from the most recent successful workflow.

#### Dashboard Integration Architecture

The dashboard integration follows this structure:

```text
controller.generate_sales_report()
            |
            v
  +-----------------------+
  |                       |
  v                       v
data_analysis       analysis_result
  |                       |
  |                       |
  |                 +-----+
  |                 |
  v                 v
Generated files   DashboardWindow
                    ^
                    |
               charts_paths
```

`data_analysis` is used by the main GUI for generated-output access.

`analysis_result` and `charts_paths` are supplied to the dashboard.

#### Generated-Output Control Management

The GUI centralizes enabling and disabling controls associated with generated reports, charts, and the sales dashboard.

##### `on_buttons()`

Enables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.
* PDF report access.
* Chart selector.
* Chart access button.
* Sales-dashboard access.

This method is called after successful report and chart generation.

##### `off_buttons()`

Disables:

* Output-folder access.
* TXT report access.
* JSON report access.
* CSV selector.
* CSV report access.
* XLSX report access.
* PDF report access.
* Chart selector.
* Chart access button.
* Sales-dashboard access.

This method is used when:

* A new source CSV file is selected.
* A new output folder is selected.
* A new report-generation process begins.
* Previously generated results should no longer be considered current.

#### Generated-Output State Cleanup

The GUI separates internal state cleanup from visual cleanup.

##### `clean_paths()`

Resets internal generated-output and analysis references:

* `txt_path` → `None`
* `json_path` → `None`
* `csv_paths` → `{}`
* `xlsx_path` → `None`
* `charts_paths` → `{}`
* `pdf_path` → `None`
* `analysis_result` → `None`
* `data_analysis` → `None`

This prevents previously generated reports, charts, controller results, or analysis data from remaining associated with a new source file, output directory, or generation process.

##### `clean_labels()`

Clears generated-output information displayed in the interface.

It:

* Clears the TXT path label.
* Clears the JSON path label.
* Clears the XLSX path label.
* Clears the PDF path label.
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
* `pdf_path`: Generated PDF report path.
* `analysis_result`: Structured analysis data from the most recent successful processing workflow.
* `data_analysis`: Controller-result dictionary containing generated report paths and related output information.

The class also maintains interface widgets, layouts, buttons, selectors, report-viewer windows, the dashboard window, and generated-output controls.

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
* `QDesktopServices`: Opening XLSX reports, PDF reports, and PNG charts through the operating system.
* `QUrl`: Conversion of local XLSX, PDF, and PNG paths for `QDesktopServices`.

The GUI also integrates the project-specific:

`DashboardWindow`

for displaying the generated sales-analysis dashboard.

#### Current GUI Workflow

The current graphical workflow is:

1. Launch `SalesReportWindow`.
2. Select a source CSV file.
3. Optionally select a custom output directory.
4. Use `reports/` when no custom directory is selected.
5. Press `Crear reporte`.
6. Verify that a source CSV file exists in the interface state.
7. Disable previous generated-output and dashboard controls.
8. Clear previous report, chart, controller-result, and analysis state.
9. Send the source CSV and output folder to `controller.generate_sales_report()`.
10. Execute the complete backend workflow.
11. Receive generated-output information and the structured analysis result.
12. Store the controller output in `data_analysis`.
13. Store structured analysis in `analysis_result`.
14. Display the generated TXT path.
15. Display the generated JSON path.
16. Display the generated XLSX path.
17. Display the generated PDF path.
18. Populate the CSV selector.
19. Display CSV paths inside the CSV scroll area.
20. Populate the chart selector.
21. Display generated chart paths inside the chart scroll area.
22. Store chart paths in `charts_paths`.
23. Enable generated-output and dashboard controls.
24. Allow TXT, JSON, and CSV reports to be inspected through `FileViewerWindow`.
25. Allow the XLSX workbook to be opened through the operating system.
26. Allow the PDF report to be opened through the operating system.
27. Allow generated PNG charts to be opened through the operating system.
28. Allow the configured output directory to be opened.
29. Allow the sales dashboard to be opened using `analysis_result` and `charts_paths`.
30. Display the final success status or an error message.

#### Error Handling

The graphical interface handles:

* Application-specific exceptions derived from `AppError`.
* Unexpected Python exceptions.

During report generation, errors update the status to:

`Error en el proceso`

and are displayed through a critical `QMessageBox`.

The `open_report_xlsx()` method also handles a missing XLSX file by displaying a warning message.

The `open_report_pdf()` method handles a missing PDF file by displaying a warning message.

The `open_chart_graphic()` method handles:

* Empty chart selection through an informational message.
* Missing PNG files through a warning message.

The dashboard button remains disabled until successful report generation, preventing normal interface access to the dashboard before current analysis information is available.

The graphical application remains open after handled errors so the user can correct the configuration or try again.

#### Input and Output

##### `SalesReportWindow`

* **Input:** User interaction through the graphical interface.
* **Output:** Main desktop interface for configuring, generating, displaying, and accessing sales reports, charts, and the sales dashboard.

##### `create_labels()`

* **Input:** None.
* **Output:** Creates the labels required by the main interface.

##### `create_buttons()`

* **Input:** None.
* **Output:** Creates report, chart, dashboard, file-selection, folder-selection, and output-access buttons.

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

##### `build_pdf_layout()`

* **Input:** None.
* **Output:** `QVBoxLayout` containing PDF report controls.

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
* **Output:** Updates the source-file state and resets previous generated-report, chart, and analysis state.

##### `selected_folder_path()`

* **Input:** Directory selected through `QFileDialog`.
* **Output:** Updates the output-folder state and resets previous generated-output and analysis state.

##### `generate_reports()`

* **Input:** Selected CSV path and configured output directory.
* **Output:** Generates reports and charts through the controller, stores the returned structured analysis, and updates the GUI with TXT, JSON, CSV, XLSX, PDF, and PNG chart information.

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

##### `open_report_pdf()`

* **Input:** Generated PDF path stored in `pdf_path`.
* **Output:** Opens the PDF report using the operating system's associated application or displays a warning when the file does not exist.

##### `open_chart_graphic()`

* **Input:** Chart selected through `chart_combobox`.
* **Output:** Opens the corresponding PNG chart through the operating system or displays an informational/warning message when necessary.

##### `open_output_folder()`

* **Input:** Configured output directory.
* **Output:** Opens the directory through the operating-system file manager.

##### `open_dashboard()`

* **Input:** Current `analysis_result` and `charts_paths` stored by the main window.
* **Output:** Creates and displays a `DashboardWindow` containing sales-analysis information and generated charts.

##### `clean_layout()`

* **Input:** Qt layout containing dynamically generated widgets.
* **Output:** Removes the dynamically generated widgets.

##### `clean_labels()`

* **Input:** None.
* **Output:** Clears TXT, JSON, CSV, XLSX, PDF, and chart information displayed in the interface.

##### `clean_paths()`

* **Input:** None.
* **Output:** Resets stored TXT, JSON, CSV, XLSX, PDF, chart, controller-result, and structured-analysis state.

##### `on_buttons()`

* **Input:** None.
* **Output:** Enables controls associated with generated reports, charts, and dashboard access.

##### `off_buttons()`

* **Input:** None.
* **Output:** Disables controls associated with generated reports, charts, and dashboard access.

#### Current Development Status

The graphical interface is connected to the Sales Report backend workflow and supports report, PDF, chart, and dashboard access.

Currently available:

* Main PySide6 desktop window.
* Source CSV selection.
* Output-folder selection.
* Default output directory.
* Application status messages.
* Backend controller integration.
* Separate storage of controller output and structured analysis.
* TXT report generation and access.
* JSON analysis generation and access.
* CSV summary generation and selection.
* Scrollable CSV path display.
* XLSX report generation and access.
* PDF report generation and access.
* Generated PNG chart selection.
* Scrollable chart path display.
* Generated PNG chart opening.
* Sales-dashboard access.
* `DashboardWindow` integration.
* Structured `analysis_result` transfer to the dashboard.
* Generated chart-path transfer to the dashboard.
* Read-only TXT, JSON, and CSV viewer integration.
* Operating-system XLSX opening.
* Operating-system PDF opening.
* Operating-system PNG opening.
* Output-directory access.
* Centralized label creation.
* Centralized button creation.
* Centralized signal connection.
* Dedicated file sub-layouts.
* Dedicated PDF sub-layout.
* Dedicated chart sub-layouts.
* Generated-output state cleanup.
* Controller-result state cleanup.
* Structured-analysis state cleanup.
* Generated-output control management.
* Dashboard control management.
* Application-specific error presentation.
* Unexpected error presentation.
* Missing-XLSX warning presentation.
* Missing-PDF warning presentation.
* Missing-PNG warning presentation.
* Empty-chart-selection information presentation.

---

### Console Application Entry Point Module

The console application entry point module provides a direct command-line execution path for the Sales Report application.

It defines the source CSV file and output directory, delegates the complete Sales Report processing workflow to the controller, receives the generated-output information, and displays the resulting processing data and generated file paths in the console.

The controller currently returns two structures:

* `reports`: Generated-output information, processing totals, and execution information.
* `analysis_result`: Complete structured sales-analysis data.

The console entry point uses only the `reports` dictionary and intentionally ignores `analysis_result`, because the structured analysis is primarily reused by other application components such as the graphical sales dashboard.

The module also handles application-specific errors derived from `AppError` and unexpected Python exceptions.

The module currently provides the following function:

* `main()`

#### Main Function

The `main()` function coordinates the console execution workflow.

It:

1. Defines the source CSV file.
2. Defines the output directory.
3. Calls `controller.generate_sales_report()`.
4. Receives the generated-output dictionary and structured analysis result.
5. Uses the generated-output dictionary.
6. Ignores the structured analysis result.
7. Iterates through the returned output information.
8. Prints generated paths, processing totals, and execution information.
9. Expands nested dictionaries so their individual entries can be displayed.
10. Handles application-specific and unexpected exceptions.

#### Input Configuration

The current console entry point defines:

```python
input_file_path = "data/sales.csv"
output_folder = "reports"
```

The source CSV file is therefore expected at:

`data/sales.csv`

The configured destination directory is:

`reports`

These values are passed directly to:

`controller.generate_sales_report()`

#### Controller Integration

The console entry point delegates the complete backend workflow to:

`controller.generate_sales_report()`

The call follows:

```python
reports, _ = controller.generate_sales_report(
    input_file_path,
    output_folder
)
```

The controller returns:

```text
reports, analysis_result
```

The first value is stored in:

`reports`

The second value is intentionally discarded using:

`_`

This is appropriate for the console entry point because it does not require direct access to the structured analytical data used by other presentation components.

#### Generated-Output Result

The `reports` dictionary contains information produced by the complete backend workflow.

It can include:

* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`
* `report_path_txt`
* `report_path_json`
* `reports_path_csv`
* `report_path_xlsx`
* `reports_path_charts`
* `report_path_pdf`
* `execution_time`

The exact generation and structure of these values are controlled by the Sales Report controller and its specialized backend modules.

#### Ignored Analysis Result

The controller also returns the complete:

`analysis_result`

produced by the sales-analysis module.

This structure contains calculated sales metrics, summaries, rankings, monthly analyses, and optional analytical results.

The console entry point does not use this structure directly.

It is ignored through:

```python
reports, _ = controller.generate_sales_report(
    input_file_path,
    output_folder
)
```

This avoids unnecessary local state while preserving the controller's shared return contract with other application components.

The structured analysis can instead be reused by components such as the graphical sales dashboard.

#### Console Output

After successful processing, the module iterates through:

`reports`

using:

```python
for item, value in reports.items():
```

Each top-level result is inspected before being printed.

#### Simple Result Values

When a returned value is not a dictionary, the entry is printed directly using:

```python
print(f"{item}: {value}")
```

This applies to values such as:

* Processing totals.
* TXT path.
* JSON path.
* XLSX path.
* PDF path.
* Execution time.

#### Nested Result Dictionaries

Some controller results are dictionaries containing multiple generated outputs.

Examples include:

* `reports_path_csv`
* `reports_path_charts`

When the current value is a dictionary, the module performs a nested iteration:

```python
for report, path in value.items():
    print(f"{report}: {path}")
```

This allows every generated CSV summary and chart path to be displayed independently.

The console entry point therefore does not require special printing logic for each individual nested output type.

#### Console Output Workflow

The output-display process can be represented as:

```text
reports
   |
   v
for item, value in reports.items()
   |
   +-- value is dict?
   |       |
   |       +-- Yes
   |       |     |
   |       |     v
   |       |  iterate nested entries
   |       |     |
   |       |     v
   |       |  print name + path
   |       |
   |       +-- No
   |             |
   |             v
   |          print item + value
```

This generic structure allows new nested output dictionaries to be displayed without creating a separate print block for every output type.

#### Backend Workflow

The console module does not perform the Sales Report processing logic itself.

The controller is responsible for coordinating:

* Source-file validation.
* CSV reading.
* DataFrame normalization.
* Sales-record validation.
* Sales analysis.
* Plain-text report generation.
* TXT export.
* JSON export.
* CSV summary export.
* XLSX generation.
* PNG chart generation.
* PDF generation.
* Execution-time measurement.

The console entry point only supplies the initial configuration, invokes the controller, and displays the returned information.

#### Error Handling

The `main()` function wraps the application workflow inside a `try` block.

Application-specific exceptions derived from:

`AppError`

are handled through:

```python
except AppError as error:
    print(error)
```

This allows application-specific error messages to be displayed in the console without producing an unhandled traceback during normal error conditions.

#### Unexpected Exceptions

Unexpected Python exceptions are also caught:

```python
except Exception as error:
    print(error)
```

The corresponding exception message is printed to the console.

This provides a final protection layer for errors that are not part of the application's custom exception hierarchy.

#### Application Entry Point

The module uses the standard Python direct-execution pattern:

```python
if __name__ == "__main__":
    main()
```

This ensures that:

`main()`

is executed when the module is run directly.

Importing the module from another Python module does not automatically execute the Sales Report workflow.

#### Application Execution Workflow

The complete console workflow is:

1. Execute the module directly.
2. Reach the `if __name__ == "__main__":` condition.
3. Call `main()`.
4. Define `data/sales.csv` as the source CSV file.
5. Define `reports` as the output directory.
6. Call `controller.generate_sales_report()`.
7. Execute the complete backend workflow.
8. Receive `reports`.
9. Receive the complete `analysis_result`.
10. Ignore `analysis_result` through `_`.
11. Iterate through the generated-output dictionary.
12. Detect nested dictionaries.
13. Print nested output entries individually.
14. Print non-dictionary values directly.
15. Handle application-specific errors when necessary.
16. Handle unexpected exceptions when necessary.

#### Module Coordination

The console application entry point interacts directly with:

* `src.controller`: Executes the complete Sales Report backend workflow.
* `src.errors.AppError`: Provides the base application-specific exception used by the console error handler.

The module does not interact directly with:

* `validator`
* `csv_reader`
* `analyzer`
* `reporter`
* `file_manager`
* `chart_manager`
* `pdf_reporter`

Those modules are coordinated internally by the controller.

#### Console Entry Point Relationship

The application relationship can be represented as:

```text
Console Application Entry Point
            |
            v
          main()
            |
            v
controller.generate_sales_report()
            |
            +---------------------------+
            |                           |
            v                           v
         reports                  analysis_result
            |                           |
            v                           v
    Console output                  ignored (_)
```

The controller continues internally through the complete backend pipeline:

```text
Console Entry Point
        |
        v
Controller
        |
        +--> Validator
        |
        +--> CSV Reader
        |
        +--> Analyzer
        |
        +--> Reporter
        |
        +--> File Manager
        |
        +--> Chart Manager
        |
        +--> PDF Reporter
        |
        v
reports + analysis_result
        |
        v
Console Entry Point
```

#### Input and Output

##### `main()`

* **Input:** Uses the configured source CSV path `data/sales.csv` and output directory `reports`.
* **Output:** Executes the Sales Report backend workflow and displays processing information and generated output paths in the console.

The function itself returns:

`None`

#### Responsibilities

This module is responsible for:

* Providing the console application `main()` function.
* Defining the console source CSV path.
* Defining the console output directory.
* Calling the Sales Report controller.
* Receiving the controller's two return values.
* Using the generated-output dictionary.
* Intentionally ignoring the structured `analysis_result`.
* Printing top-level processing information.
* Iterating nested output dictionaries.
* Printing generated CSV paths.
* Printing generated chart paths.
* Printing generated report paths.
* Printing execution information.
* Handling application-specific exceptions.
* Handling unexpected exceptions.
* Providing the direct Python execution entry point.

This module is not responsible for:

* Creating the PySide6 application environment.
* Creating graphical windows.
* Building graphical interface layouts.
* Opening the sales dashboard.
* Selecting files through graphical dialogs.
* Validating source files.
* Reading CSV files.
* Validating sales records.
* Calculating sales metrics.
* Generating reports directly.
* Generating charts directly.
* Building PDF reports directly.
* Saving output files directly.
* Implementing the internal backend workflow.

Those responsibilities belong to the graphical application, controller, and specialized backend modules.

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

Generated charts use the same shared base filename used by the remaining report outputs, allowing PNG images to remain associated with the TXT, JSON, CSV, XLSX, and PDF files generated during the same workflow.

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
* Y-axis: `crec_ingreso_pct`
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
* Y-axis: `crec_unidades_pct`
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

The controller uses this dictionary in two later parts of the application workflow:

* It returns the generated chart identifiers and PNG paths for graphical-interface access.
* It passes the generated chart paths to the PDF-report generation workflow.

This means chart generation occurs before PDF generation in the current processing pipeline.

#### PDF Report Integration

The chart-generation module does not generate PDF files directly.

After `save_chart_images()` returns the generated chart dictionary, the controller passes:

`reports_path_charts`

to the dedicated PDF-report module.

This allows the PDF reporter to reuse the already generated PNG chart images without requiring the chart manager to know how the PDF document is built.

The relationship can be represented as:

```text
chart_manager.save_chart_images()
        |
        v
reports_path_charts
        |
        +--------> Graphical Interface
        |
        +--------> PDF Reporter
```

This preserves separation between:

* Chart generation.
* PDF document generation.
* Graphical presentation.

#### Graphical Interface Integration

The graphical interface receives:

`reports_path_charts`

from the controller.

Each chart identifier can be added to the chart selector.

The corresponding PNG path can be stored inside:

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

The monthly-summary charts specifically consume:

* `mes`
* `ingreso_total`
* `unidades_vendidas`
* `crec_ingreso_pct`
* `crec_unidades_pct`

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
* Generating PDF reports.
* Displaying charts inside the graphical interface.

Those responsibilities belong to the corresponding validation, analysis, reporting, file-management, PDF-reporting, controller, and graphical-interface modules.

#### Related Exception

* `ChartGenerationError`

---

### PDF Report Generation Module

The PDF report generation module converts structured sales-analysis results, validation information, and previously generated chart images into a complete PDF sales report.

The module uses ReportLab to create a letter-sized document containing:

* A report title derived from the source CSV filename.
* General sales metrics.
* Structured analysis tables.
* Generated PNG charts.
* Validation errors.
* Validation warnings.

The PDF is generated after the sales-analysis and chart-generation stages have completed.

The module receives the same shared base filename used by the remaining report outputs, allowing the PDF file to remain associated with the TXT, JSON, CSV, XLSX, and PNG files generated during the same workflow.

The module currently provides the following functions:

* `get_title_pdf()`
* `get_title_table_spanish()`
* `get_widths_columns()`
* `normalize_headers()`
* `get_table()`
* `get_tables()`
* `get_image()`
* `get_charts()`
* `get_general_summary()`
* `get_errors()`
* `get_warnings()`
* `save_pdf_reporter()`

#### Dependencies

The PDF-generation workflow uses:

* `reportlab.lib.pagesizes.letter`: Defines the PDF page size.
* `SimpleDocTemplate`: Builds the final PDF document.
* `Paragraph`: Creates text sections and titles.
* `Table`: Creates structured analysis tables.
* `TableStyle`: Applies table formatting.
* `Image`: Embeds generated chart images.
* `Spacer`: Adds vertical spacing between document elements.
* `getSampleStyleSheet()`: Provides standard ReportLab text styles.
* `colors`: Provides table-grid colors.
* `pathlib.Path`: Handles output paths and directories.
* `pandas`: Converts structured analysis information into tabular data.
* `PDFGenerationError`: Application-specific PDF-generation exception.

#### PDF Configuration

The module uses the ReportLab:

`letter`

page size.

The page dimensions are stored in:

```python
WIDTH_PAGE, HEIGHT_PAGE = letter
```

A margin of:

`72`

points is used when calculating the available width for tables and chart images.

The configured value is stored in:

`MARGIN`

#### Table Title Translation

The module defines:

`TRANSLATE_TITLES`

to convert internal `analysis_result` keys into Spanish titles suitable for the generated PDF.

The current translations include:

* `product_summary` → `Resumen de Productos`
* `category_summary` → `Resumen de Categorías`
* `monthly_summary` → `Resumen Mensual`
* `best_selling_product` → `Producto Más Vendido`
* `highest_income_product` → `Producto con Mayor Ingreso`
* `highest_income_category` → `Categoría con Mayor Ingreso`
* `top_5_best_selling_products` → `Top 5 Productos Más Vendidos`
* `top_5_highest_income_products` → `Top 5 Productos con Mayor Ingreso`
* `monthly_best_selling_product` → `Producto Más Vendido Mensual`
* `monthly_highest_income_category` → `Categoría con Mayor Ingreso Mensual`
* `city_summary` → `Resumen por Ciudad`
* `highest_income_city` → `Ciudad con Mayor Ingreso`
* `payment_method_summary` → `Resumen por Método de Pago`
* `highest_income_payment_method` → `Método de Pago con Mayor Ingreso`

These translations affect presentation only and do not modify the original analysis-result keys.

#### PDF Title

The `get_title_pdf()` function creates the main document title from the original source CSV filename.

It receives:

`input_file_name`

as a `Path`.

The function:

1. Extracts the filename without its extension using `Path.stem`.
2. Splits the filename at underscore characters.
3. Joins the resulting parts using spaces.
4. Capitalizes the resulting title.
5. Creates a ReportLab `Paragraph` using the standard `Title` style.

For example, a source file named conceptually:

`ventas_agosto.csv`

produces the title:

`Ventas agosto`

The function returns a ReportLab:

`Paragraph`

#### Analysis Table Titles

The `get_title_table_spanish()` function creates the heading displayed before each analysis table.

It receives an `analysis_result` key and searches for its Spanish representation inside:

`TRANSLATE_TITLES`

When a predefined translation is available, that translated title is used.

When no translation is available, the function:

1. Replaces underscores with spaces.
2. Converts the resulting text to uppercase.

The final title is returned as a ReportLab `Paragraph` using:

`Heading2`

#### Column Width Calculation

The `get_widths_columns()` function calculates equal widths for all columns in a PDF table.

The available width is calculated using:

```python
WIDTH_PAGE - (MARGIN * 2)
```

The resulting width is divided by the number of table columns.

The function returns:

`List[float]`

containing one width value for each column.

All columns within the same table therefore receive equal widths.

#### Header Normalization

The `normalize_headers()` function converts DataFrame column names into more readable table headers.

For every header, the function:

1. Replaces underscores with spaces.
2. Applies `capitalize()`.

For example:

`unidades_vendidas`

becomes:

`Unidades vendidas`

The function returns a new list of normalized headers and does not modify the original list.

#### DataFrame Table Generation

The `get_table()` function converts a pandas DataFrame into a ReportLab `Table`.

The process includes:

1. Reading the original DataFrame column names.
2. Normalizing the column headers.
3. Converting DataFrame rows into lists.
4. Combining headers and rows.
5. Calculating equal column widths.
6. Creating the ReportLab table.
7. Applying table formatting.
8. Configuring the first row as a repeating header.

Every generated table receives a visible black grid.

Tables containing:

`8`

columns use:

`5`

as their font size.

Tables containing:

`6`

columns use:

`7`

as their font size.

Tables with other numbers of columns retain the default ReportLab font size while still receiving the table grid.

The table is configured with:

```python
table.repeatRows = 1
```

This causes the header row to repeat when a table continues across multiple PDF pages.

#### Analysis Table Generation

The `get_tables()` function converts supported structures from:

`analysis_result`

into ReportLab table elements.

The function iterates through every analysis-result entry.

When the value is a:

`list`

the list is converted into a pandas DataFrame.

When the value is already a:

`pandas.DataFrame`

it is processed directly.

Empty lists and empty DataFrames are omitted.

Missing values are replaced with:

`N/D`

before table generation.

Other value types are ignored by this function.

This means scalar values such as:

* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`
* `total_income`
* `total_units_sold`

are not converted into tables because they are displayed separately through the general-summary section.

For each supported analysis structure, the function adds:

1. Spanish table title.
2. Vertical spacer.
3. Generated table.
4. Vertical spacer.

The resulting elements are returned as a list ready to be included in the PDF document.

#### Tables Included in the PDF

Depending on the contents of `analysis_result`, table generation can include:

* Product summary.
* Category summary.
* Monthly summary.
* Best-selling products.
* Highest-income products.
* Highest-income categories.
* Top 5 best-selling products.
* Top 5 highest-income products.
* Monthly best-selling products.
* Monthly highest-income categories.

When optional analysis information is available, the PDF can also include:

* City summary.
* Highest-income cities.
* Payment-method summary.
* Highest-income payment methods.

Optional or empty structures are omitted automatically.

#### Chart Image Generation

The PDF module does not generate charts itself.

Charts are generated previously by the dedicated chart-generation module.

The PDF reporter receives a dictionary containing the generated PNG paths and embeds those existing images into the document.

#### Individual Chart Image

The `get_image()` function converts a generated chart path into a ReportLab `Image`.

The chart is displayed using:

* Width: Available PDF page width.
* Height: `300` points.

The image width is calculated through:

```python
WIDTH_PAGE - (MARGIN * 2)
```

The function returns a ReportLab:

`Image`

#### Chart Collection

The `get_charts()` function converts the complete generated-chart dictionary into PDF elements.

It receives:

`charts`

which maps chart identifiers to PNG paths.

The function iterates through the chart paths and creates one ReportLab image for every generated chart.

A vertical:

`Spacer(1, 12)`

is inserted after each chart.

The chart identifiers themselves are not currently used as visible chart titles inside the PDF.

The charts are embedded according to the order received from the chart dictionary.

#### General Sales Summary

The `get_general_summary()` function creates the general sales-summary section.

The section begins with:

`RESUMEN GENERAL`

and displays:

* Total processed rows.
* Total valid rows.
* Total invalid rows.
* Total income.
* Total units sold.

The values are obtained from:

* `total_rows`
* `total_valid_rows`
* `total_invalid_rows`
* `total_income`
* `total_units_sold`

Total income is formatted using:

* Currency notation.
* Thousands separators.
* Two decimal places.

For example:

`$12,450.75`

The section is returned as a ReportLab `Paragraph` using the standard:

`Normal`

style.

#### Validation Errors

The `get_errors()` function creates the validation-errors section of the PDF.

The section begins with:

`ERRORES DE VALIDACIÓN`

When no validation errors are available, the PDF displays:

`No se encontraron errores de validación.`

When errors exist, they are sorted by:

`line_number`

For each validation error, the section displays:

* CSV line number.
* Column.
* Error type.
* Error message.
* Original value when available.

A validation-error structure can contain:

* `line_number`
* `column`
* `error_type`
* `message`
* `original_value`

When:

`original_value`

is an empty string, the original-value text is omitted.

The final content is returned as a ReportLab `Paragraph`.

#### Validation Warnings

The `get_warnings()` function creates the validation-warnings section.

The section begins with:

`ADVERTENCIAS`

When no warnings are available, the PDF displays:

`No se encontraron advertencias`

When warnings exist, they are sorted by:

`affected_value`

For every warning, the PDF displays:

* Affected `producto_id`.
* Warning type.
* Warning message.
* Warning details.

The current warning structure uses information such as:

* `affected_value`
* `warning_type`
* `message`
* `details`

When multiple detail values are available, they are joined using comma-separated text.

The resulting content is returned as a ReportLab `Paragraph`.

#### PDF Generation Process

The `save_pdf_reporter()` function coordinates the complete PDF-generation workflow.

It receives:

* `analysis_result`
* `output_folder`
* `file_base_name`
* `input_file_name`
* `validation_result`
* `charts`

The process performs the following operations:

1. Creates the PDF output filename.
2. Converts the output directory into a `Path`.
3. Creates the destination directory and missing parent directories when necessary.
4. Creates the complete PDF output path.
5. Converts the path to a string for ReportLab.
6. Creates a letter-sized `SimpleDocTemplate`.
7. Creates an empty document-element list.
8. Adds the main report title.
9. Adds the general sales summary.
10. Adds all supported structured analysis tables.
11. Adds all generated chart images.
12. Adds the validation-errors section.
13. Adds the validation-warnings section.
14. Builds the final PDF document.
15. Returns the generated PDF path.

#### PDF Document Structure

The current PDF follows this general order:

```text
Report Title

General Summary

Analysis Tables
    ├── Product Summary
    ├── Category Summary
    ├── Monthly Summary
    ├── Overall Rankings
    ├── Top 5 Rankings
    ├── Monthly Rankings
    └── Optional City / Payment-Method Analysis

Generated Charts

Validation Errors

Validation Warnings
```

The exact set of tables and charts depends on the analysis structures and optional data available during the workflow.

#### Shared Filename Integration

The PDF reporter receives:

`file_base_name`

from the controller.

This is the same base filename used by the remaining generated report outputs.

The PDF filename follows:

```text
<shared_base_filename>.pdf
```

For example, if the shared base filename is:

`ventas_agosto_2026-09-20_15-30-25-125`

the generated PDF is:

`ventas_agosto_2026-09-20_15-30-25-125.pdf`

This keeps the PDF associated with all other files generated during the same processing workflow.

#### Output Directory

The destination folder is converted into:

`Path`

and created through:

```python
folder.mkdir(parents=True, exist_ok=True)
```

This allows PDF generation even when the configured destination directory does not already exist.

#### Controller Integration

The controller generates the PDF after the chart-generation stage.

The controller calls:

`pdf_reporter.save_pdf_reporter()`

and provides:

* Complete `analysis_result`.
* Configured output folder.
* Shared base filename.
* Source CSV `Path`.
* Complete validation result.
* Generated chart paths.

Conceptually:

```python
reports["report_path_pdf"] = pdf_reporter.save_pdf_reporter(
    analysis_result,
    output_folder,
    file_name,
    file_path,
    validation_result,
    reports["reports_path_charts"]
)
```

The generated PDF path is stored by the controller as:

`report_path_pdf`

#### Chart Manager Integration

The PDF reporter receives:

`reports_path_charts`

after the chart-generation module has completed.

The dependency can be represented as:

```text
Sales Analysis
      |
      v
Chart Generation
      |
      v
reports_path_charts
      |
      v
PDF Report Generation
```

The PDF module therefore embeds existing chart files rather than recalculating sales metrics or recreating charts.

#### Validation Integration

The complete:

`validation_result`

is supplied to the PDF reporter.

The PDF-generation workflow currently uses:

* `validation_result["errors"]`
* `validation_result["warnings"]`

These structures are passed to:

* `get_errors()`
* `get_warnings()`

The PDF reporter does not perform validation itself.

#### Analysis Integration

The PDF reporter consumes the complete:

`analysis_result`

produced by the sales-analysis module.

Scalar general metrics are used by:

`get_general_summary()`

Structured lists and DataFrames are processed by:

`get_tables()`

The PDF module does not calculate:

* Total income.
* Total units sold.
* Product summaries.
* Category summaries.
* Monthly metrics.
* Rankings.
* Growth values.
* Optional city metrics.
* Optional payment-method metrics.

Those values are received from the analysis layer.

#### PDF Error Handling

The main PDF-generation workflow catches:

* `OSError`
* `ValueError`

When one of these supported failures occurs, the module raises:

`PDFGenerationError`

using exception chaining.

Conceptually:

```python
except (OSError, ValueError) as error:
    raise PDFGenerationError() from error
```

This converts supported PDF-generation and file-system failures into the common application-specific exception hierarchy while preserving the original Python exception as its cause.

#### Generated PDF Path

The `save_pdf_reporter()` function returns:

`Path`

pointing to the generated PDF document.

The controller stores this path as:

`report_path_pdf`

The graphical interface later receives this value and allows the user to open the generated PDF through the operating system.

#### Graphical Interface Integration

The graphical interface receives:

`report_path_pdf`

from the controller.

The path is stored in:

`pdf_path`

and displayed in the generated-files section.

The:

`Ver PDF`

button calls:

`open_report_pdf()`

The GUI verifies that the generated file exists and opens it using the operating system's associated PDF application through `QDesktopServices`.

The PDF reporter itself does not display or open the generated document.

#### Input and Output

##### `get_title_pdf()`

* **Input:** Source CSV `Path`.
* **Output:** ReportLab `Paragraph` containing the PDF title.

##### `get_title_table_spanish()`

* **Input:** Analysis-result key as a string.
* **Output:** ReportLab `Paragraph` containing the Spanish analysis-section title.

##### `get_widths_columns()`

* **Input:** Number of table columns.
* **Output:** List containing equal width values for all columns.

##### `normalize_headers()`

* **Input:** List of DataFrame column names.
* **Output:** List containing normalized human-readable headers.

##### `get_table()`

* **Input:** pandas `DataFrame`.
* **Output:** Formatted ReportLab `Table`.

##### `get_tables()`

* **Input:** Complete analysis-result dictionary.
* **Output:** List containing table titles, tables, and spacing elements.

##### `get_image()`

* **Input:** PNG path as `str | Path`.
* **Output:** ReportLab `Image`.

##### `get_charts()`

* **Input:** Dictionary mapping chart identifiers to PNG paths.
* **Output:** List containing chart images and spacing elements.

##### `get_general_summary()`

* **Input:** Complete analysis-result dictionary.
* **Output:** ReportLab `Paragraph` containing the general sales summary.

##### `get_errors()`

* **Input:** List of validation-error dictionaries.
* **Output:** ReportLab `Paragraph` containing the validation-errors section.

##### `get_warnings()`

* **Input:** List of validation-warning dictionaries.
* **Output:** ReportLab `Paragraph` containing the validation-warnings section.

##### `save_pdf_reporter()`

* **Input:** Analysis result, output directory, shared base filename, source CSV path, validation result, and generated chart paths.
* **Output:** `Path` pointing to the generated PDF report.

#### Responsibilities

The PDF report generation module is responsible for:

* Creating the PDF document.
* Creating the PDF title.
* Formatting general sales metrics.
* Translating analysis-section titles into Spanish.
* Normalizing table headers.
* Calculating table column widths.
* Converting analysis DataFrames into PDF tables.
* Converting analysis lists into DataFrames for PDF tables.
* Replacing missing table values with `N/D`.
* Applying table grids.
* Adjusting table font sizes according to column count.
* Repeating table header rows across pages.
* Embedding previously generated PNG charts.
* Formatting validation errors.
* Formatting validation warnings.
* Creating the output directory when necessary.
* Using the shared report base filename.
* Returning the generated PDF path.
* Converting supported PDF-generation failures into `PDFGenerationError`.

The PDF report generation module is not responsible for:

* Reading source CSV files.
* Validating source-file paths.
* Validating individual sales records.
* Calculating sales metrics.
* Calculating rankings.
* Calculating monthly growth.
* Generating chart images.
* Generating TXT reports.
* Generating JSON files.
* Generating CSV files.
* Generating XLSX workbooks.
* Displaying or opening the PDF through the graphical interface.

Those responsibilities belong to the corresponding validation, reading, analysis, reporting, chart-generation, file-management, controller, and graphical-interface modules.

#### Related Exception

* `PDFGenerationError`

---

### Sales Dashboard Module

The Sales Dashboard module provides a dedicated PySide6 window for visually presenting previously calculated sales-analysis results and generated chart images.

The dashboard receives two structures:

* `analysis_result`: Complete structured sales-analysis information produced by the analysis workflow.
* `chart_paths`: Dictionary mapping generated chart identifiers to their PNG file paths.

The module does not read CSV files, validate sales records, calculate sales metrics, or generate chart images.

Its responsibility is exclusively to present existing analysis information through a graphical dashboard.

The dashboard currently displays:

* General sales KPIs.
* Best-selling product results.
* Highest-income product results.
* Highest-income category results.
* Generated sales charts through an interactive selector.

The module currently provides the following class:

* `DashboardWindow`

#### Dashboard Window

The `DashboardWindow` class inherits from PySide6 `QMainWindow` and represents the interactive sales-analysis dashboard.

The window is configured with:

* Title: `Panel de ventas`
* Width: `1500`
* Height: `900`

The dashboard receives:

```python
analysis_result
chart_paths
```

during initialization.

These structures are stored as:

* `self.analysis_result`
* `self.chart_paths`

The dashboard uses a central `QWidget` and a primary vertical `QVBoxLayout` to organize its visual sections.

#### Dashboard Initialization

The `DashboardWindow` constructor receives:

```python
DashboardWindow(
    analysis_result,
    chart_paths
)
```

The initialization process:

1. Stores the structured analysis result.
2. Stores the generated chart paths.
3. Configures the window title.
4. Configures the fixed window size.
5. Creates the central widget.
6. Creates the main vertical layout.
7. Adds the general KPI section.
8. Adds the highlighted best-result section.
9. Adds the chart section.
10. Assigns the completed layout to the central widget.
11. Assigns the central widget to the dashboard window.

#### Dashboard Structure

The dashboard is divided into three main visual areas:

```text
DashboardWindow
│
├── General KPI Section
│
├── Best Results Section
│
└── Charts Section
```

The corresponding layout-building methods are:

* `build_general_kpis_layout()`
* `build_best_result_layout()`
* `build_charts_layout()`

#### Analysis Result Integration

The dashboard uses the existing:

`analysis_result`

generated by the Sales Analysis module.

It does not calculate these metrics internally.

The current dashboard consumes:

* `total_income`
* `total_units_sold`
* `total_valid_rows`
* `total_invalid_rows`
* `best_selling_product`
* `highest_income_product`
* `highest_income_category`

These values have already been calculated by the backend analysis workflow before the dashboard is opened.

#### Chart Path Integration

The dashboard also receives:

`chart_paths`

This dictionary maps chart identifiers to generated PNG file paths.

Conceptually:

```python
{
    "grafica_de_ingresos_mensuales": Path(...),
    "grafica_de_unidades_vendidas_mensualmente": Path(...),
    "...": Path(...)
}
```

The dashboard does not generate these charts.

The PNG images are created previously by the Chart Generation module and are passed to the dashboard through the graphical application workflow.

#### General KPI Section

The general KPI section is created through:

`build_general_kpis_layout()`

This method creates a horizontal layout containing the primary sales indicators.

The current KPIs are:

* `INGRESO TOTAL`
* `UNIDADES VENDIDAS`
* `FILAS VÁLIDAS`
* `FILAS INVÁLIDAS`

The corresponding analysis values are obtained from:

```python
analysis_result["total_income"]
analysis_result["total_units_sold"]
analysis_result["total_valid_rows"]
analysis_result["total_invalid_rows"]
```

Total income is formatted as currency using:

* A currency symbol.
* Thousands separators.
* Two decimal places.

For example:

```text
$125,450.75
```

Each KPI is represented by an independent visual card.

#### KPI Card Creation

The `create_kpi_card()` method creates a reusable visual card for a general KPI.

It receives:

* `title`
* `value`

and returns:

`QFrame`

The frame uses:

```python
QFrame.Shape.Box
```

to visually separate the KPI from surrounding dashboard content.

Each card contains:

* A title label.
* A value label.

#### KPI Title Style

The KPI title uses:

```text
Font size: 20px
Font weight: bold
Font family: Arial
```

The title is centered inside the card using:

`Qt.AlignmentFlag.AlignCenter`

#### KPI Value Style

The KPI value uses:

```text
Font size: 30px
Font weight: bold
Font family: Arial
```

The value is also centered.

The larger font size gives greater visual emphasis to the KPI value than to its title.

#### General KPI Layout

`build_general_kpis_layout()` creates a dictionary containing the formatted KPI values.

Conceptually:

```python
{
    "INGRESO TOTAL": ...,
    "UNIDADES VENDIDAS": ...,
    "FILAS VÁLIDAS": ...,
    "FILAS INVÁLIDAS": ...
}
```

For every entry:

1. The KPI title is obtained.
2. The corresponding formatted value is obtained.
3. `create_kpi_card()` creates the visual frame.
4. The frame is added to the horizontal layout.

The result is a row of independent KPI cards.

#### Best Results Section

The highlighted sales-results section is created through:

`build_best_result_layout()`

This section currently displays:

* Best-selling product or products.
* Highest-income product or products.
* Highest-income category or categories.

The data is obtained from:

```python
analysis_result["best_selling_product"]
analysis_result["highest_income_product"]
analysis_result["highest_income_category"]
```

#### Best-Selling Product

The:

`PRODUCTO MÁS VENDIDO`

card displays:

* Product name.
* Units sold.

The value is formatted conceptually as:

```text
Product Name
150 Unidades.
```

The dashboard supports multiple records when more than one product shares the highest number of units sold.

#### Highest-Income Product

The:

`PRODUCTO CON MAYOR INGRESO`

card displays:

* Product name.
* Total income generated.

Income is formatted as currency using thousands separators and two decimal places.

For example:

```text
Product Name
$25,450.75
```

Multiple products can be displayed when tied for the maximum income value.

#### Highest-Income Category

The:

`CATEGORÍA CON MAYOR INGRESO`

card displays:

* Category name.
* Total income generated.

Income is formatted using the same currency representation used by the highest-income product result.

Multiple categories can be displayed when tied for the maximum income value.

#### Result Card Creation

The `create_result_card()` method creates reusable cards for highlighted sales-analysis results.

It receives:

* `title`
* `list_values`

The `list_values` parameter is represented as:

`List[List[str]]`

This nested structure allows each analytical record to contain multiple display values.

For example:

```python
[
    ["Producto A", "25 Unidades."],
    ["Producto B", "25 Unidades."]
]
```

This allows tied analysis records to be displayed without discarding any of the maximum-value results.

#### Result Card Style

The result-card title uses:

```text
Font size: 20px
Font weight: bold
Font family: Arial
```

Each displayed result value uses:

```text
Font size: 30px
Font weight: bold
Font family: Arial
```

Both titles and result values are centered using:

`Qt.AlignmentFlag.AlignCenter`

#### Tie Preservation

The dashboard preserves the tie-handling behavior established by the Sales Analysis module.

The following structures can contain more than one record:

* `best_selling_product`
* `highest_income_product`
* `highest_income_category`

`build_best_result_layout()` converts every record into display values.

`create_result_card()` then iterates through all supplied records and all their values.

This means the dashboard does not reduce tied results to a single product or category.

#### Chart Section

The dashboard chart section is created through:

`build_charts_layout()`

The method creates a horizontal layout and adds the chart card generated by:

`create_chart_card()`

The chart card provides:

* A chart-selection label.
* A `QComboBox`.
* A chart-image display area.

#### Chart Card Creation

The `create_chart_card()` method creates the interactive chart area.

The chart card contains:

```text
Gráfica:
[ Chart Selector ]

[ Selected Chart Image ]
```

The chart identifier selector is implemented using:

`QComboBox`

The image display area is implemented using:

`QLabel`

#### Chart Selector

The dashboard populates the combo box using the keys contained in:

`chart_paths`

The current implementation iterates through:

```python
for name_path, _ in self.chart_paths.items():
```

and adds:

`name_path`

to the selector.

The combo box therefore contains chart identifiers rather than direct file paths.

#### Chart Selector Style

The chart selector currently uses:

```text
Font size: 12pt
Font weight: bold
Font family: Arial
```

The selector is positioned beside the:

`Gráfica:`

label.

#### Initial Chart Display

After the chart selector is populated, the dashboard immediately calls:

`show_chart_card()`

using:

`self.combo_box.currentText()`

This causes the first available chart to be displayed when the dashboard chart card is created.

#### Interactive Chart Selection

The combo box signal:

`currentTextChanged`

is connected to:

`show_chart_card()`

Conceptually:

```python
self.combo_box.currentTextChanged.connect(
    self.show_chart_card
)
```

When the user selects another chart:

1. The selected chart identifier changes.
2. `show_chart_card()` receives the new identifier.
3. The corresponding PNG path is retrieved.
4. The image is loaded.
5. The dashboard chart display is updated.

No backend recalculation is required when switching charts.

#### Chart Display

The `show_chart_card()` method receives a chart identifier.

Although the parameter is named:

`path_chart`

the current implementation uses it as a key in:

`chart_paths`

Conceptually:

```python
self.chart_paths[path_chart]
```

The actual image path is therefore retrieved from the dictionary before the chart is loaded.

#### QPixmap Integration

The selected PNG image is loaded through:

`QPixmap`

Conceptually:

```python
pixmap = QPixmap(
    str(self.chart_paths[path_chart])
)
```

The path is converted to a string before being passed to `QPixmap`.

#### Chart Scaling

The loaded chart is scaled using:

```text
Maximum width: 500
Maximum height: 400
```

The scaling operation uses:

`Qt.AspectRatioMode.KeepAspectRatio`

This prevents the original chart proportions from being distorted.

The dashboard also uses:

`Qt.TransformationMode.SmoothTransformation`

to improve the visual quality of the resized image.

#### Chart Image Display

After scaling, the image is assigned to:

`chart_image`

through:

```python
self.chart_image.setPixmap(pixmap_scale)
```

The chart-image label is centered in the dashboard chart card.

#### Empty Chart Identifier Handling

`show_chart_card()` verifies:

```python
path_chart.strip() != ""
```

before attempting to retrieve or display an image.

If the supplied chart identifier is empty, the method performs no image update.

#### Main GUI Integration

The dashboard is opened from the main Sales Report graphical interface.

The main GUI stores:

* `analysis_result`
* `charts_paths`

after a successful report-generation workflow.

When the user selects:

`Abrir panel de ventas`

the main interface creates:

```python
DashboardWindow(
    self.analysis_result,
    self.charts_paths
)
```

The dashboard therefore operates on the same analysis information and generated charts already available in the application.

#### Controller Integration

The dashboard does not communicate directly with the controller.

The relationship is indirect:

```text
Controller
    |
    v
analysis_result
    |
    v
Main GUI
    |
    v
DashboardWindow
```

The controller returns the structured sales-analysis result to the main graphical interface.

The main interface then forwards that information to the dashboard.

#### Analyzer Integration

The dashboard depends on structures previously calculated by the Sales Analysis module.

Current analytical dependencies include:

```text
total_income
total_units_sold
total_valid_rows
total_invalid_rows

best_selling_product
highest_income_product
highest_income_category
```

The dashboard does not alter these structures.

It only formats and displays their existing values.

#### Chart Manager Integration

Generated chart files originate from the Chart Generation module.

The relationship is:

```text
Chart Manager
      |
      v
reports_path_charts
      |
      v
Main GUI
      |
      v
chart_paths
      |
      v
DashboardWindow
```

The Dashboard module therefore does not depend on Matplotlib directly.

It displays existing PNG files through PySide6 `QPixmap`.

#### Dashboard Data Flow

The complete data flow can be represented as:

```text
Source CSV
    |
    v
Validation
    |
    v
Sales Analysis
    |
    +------------------------+
    |                        |
    v                        v
analysis_result         Chart Manager
    |                        |
    |                        v
    |                   chart_paths
    |                        |
    +------------+-----------+
                 |
                 v
           Main GUI
                 |
                 v
         DashboardWindow
                 |
       +---------+---------+
       |         |         |
       v         v         v
     KPIs   Best Results  Charts
```

#### PySide6 Components

The dashboard currently uses:

* `QMainWindow`: Dashboard window.
* `QWidget`: Central dashboard container.
* `QVBoxLayout`: Main vertical organization and internal card layouts.
* `QHBoxLayout`: Horizontal KPI, result, and chart organization.
* `QLabel`: KPI titles, values, result text, chart labels, and chart image display.
* `QComboBox`: Interactive chart selection.
* `QFrame`: Visual KPI, result, and chart cards.
* `QPixmap`: PNG chart loading and rendering.
* `Qt.AlignmentFlag`: Widget alignment.
* `Qt.AspectRatioMode`: Aspect-ratio-preserving image scaling.
* `Qt.TransformationMode`: Smooth image transformation.

#### Dashboard Workflow

The current dashboard workflow is:

1. Receive `analysis_result`.
2. Receive `chart_paths`.
3. Create `DashboardWindow`.
4. Configure the window as `1500 × 900`.
5. Create the general KPI section.
6. Read general metrics from `analysis_result`.
7. Create individual KPI cards.
8. Create the highlighted result section.
9. Read best-performing records from `analysis_result`.
10. Preserve and display tied maximum-value records.
11. Create the chart section.
12. Populate the chart selector from `chart_paths`.
13. Display the first available chart.
14. Listen for chart-selection changes.
15. Load the selected PNG through `QPixmap`.
16. Scale the image while preserving aspect ratio.
17. Display the selected chart in the dashboard.

#### Input and Output

##### `DashboardWindow`

* **Input:** Structured sales-analysis dictionary and generated chart-path dictionary.
* **Output:** Interactive PySide6 sales dashboard window.

##### `create_kpi_card()`

* **Input:** KPI title and formatted value.
* **Output:** `QFrame` containing the formatted KPI card.

##### `build_general_kpis_layout()`

* **Input:** Uses general values stored in `analysis_result`.
* **Output:** `QHBoxLayout` containing the general sales KPI cards.

##### `create_result_card()`

* **Input:** Result-card title and nested list containing formatted analytical values.
* **Output:** `QFrame` containing one or more highlighted results.

##### `build_best_result_layout()`

* **Input:** Uses maximum-value result structures stored in `analysis_result`.
* **Output:** `QHBoxLayout` containing best-selling, highest-income product, and highest-income category cards.

##### `create_chart_card()`

* **Input:** Uses the generated chart identifiers and paths stored in `chart_paths`.
* **Output:** `QFrame` containing the chart selector and image display area.

##### `build_charts_layout()`

* **Input:** None directly.
* **Output:** `QHBoxLayout` containing the dashboard chart card.

##### `show_chart_card()`

* **Input:** Selected chart identifier.
* **Output:** Updates `chart_image` with the corresponding scaled PNG chart.

#### Responsibilities

The Sales Dashboard module is responsible for:

* Creating the sales dashboard window.
* Receiving structured sales-analysis results.
* Receiving generated chart paths.
* Displaying general KPI values.
* Formatting total income for presentation.
* Displaying total units sold.
* Displaying valid-row totals.
* Displaying invalid-row totals.
* Displaying the best-selling product or products.
* Displaying the highest-income product or products.
* Displaying the highest-income category or categories.
* Preserving tied maximum-value records in the visual presentation.
* Creating reusable KPI cards.
* Creating reusable result cards.
* Creating the chart-selection interface.
* Populating the chart selector.
* Loading PNG charts through `QPixmap`.
* Scaling chart images.
* Preserving chart aspect ratio.
* Updating the displayed chart interactively.
* Presenting existing analytical information without recalculating it.

The Sales Dashboard module is not responsible for:

* Reading CSV files.
* Validating source paths.
* Validating sales records.
* Normalizing sales data.
* Calculating total income.
* Calculating total units sold.
* Calculating rankings.
* Determining maximum-value records.
* Performing monthly analysis.
* Generating PNG chart files.
* Generating TXT reports.
* Generating JSON files.
* Generating CSV summaries.
* Generating XLSX workbooks.
* Generating PDF reports.
* Managing report filenames.
* Saving generated reports.
* Coordinating the complete backend workflow.

Those responsibilities belong to the corresponding validation, reading, analysis, reporting, file-management, chart-generation, PDF-reporting, controller, and main graphical-interface modules.

#### Current Development Status

The Sales Dashboard currently provides:

* Dedicated `DashboardWindow`.
* Fixed `1500 × 900` dashboard window.
* General KPI visualization.
* Total-income KPI.
* Total-units-sold KPI.
* Valid-row KPI.
* Invalid-row KPI.
* Best-selling product visualization.
* Highest-income product visualization.
* Highest-income category visualization.
* Support for tied best-performing records.
* Reusable KPI cards.
* Reusable result cards.
* Generated-chart selector.
* Automatic first-chart display.
* Interactive chart switching.
* PNG loading through `QPixmap`.
* Aspect-ratio-preserving chart scaling.
* Smooth image transformation.
* Integration with `analysis_result`.
* Integration with generated chart paths.
* Integration with the main graphical interface.
* Reuse of existing backend analysis without recalculation.

---
