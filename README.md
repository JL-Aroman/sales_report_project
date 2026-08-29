# Sales Report

> **Project Status:** Version 1.2 completed - Functional console application. This project has been manually tested with a sample sales CSV file.

Automatic sales reporting system for processing sales data, validating CSV files, analyzing valid records, and generating structured reports.

---

## Project Architecture (Current State)

The project follows a modular architecture in which each module is responsible for a specific part of the application workflow.

## Installation and Usage

### Requirements

Before running the project, make sure the following tools are installed:

- Python 3.10 or later.
- `pip`, the Python package installer.
- Git, if the project will be cloned from GitHub.

### Installation

1. Clone the repository:
git clone <repository-url>


2. Move into the project directory:
cd sales_report_project

3. Create a virtual environment:
python -m venv .venv

4. Activate the virtual environment.
On Windows:
.venv\Scripts\activate
On macOS or Linux:
source .venv/bin/activate

5. Install the project dependencies:
pip install -r requirements.txt

### Input CSV File

Place the source CSV file inside the `data` directory using the following filename:

data/sales.csv

The CSV file must contain the following columns:

producto_id,producto,categoria,precio,cantidad,fecha

The expected date format is:

YYYY-MM-DD

The application also support the following optional columns:

- `ciudad`
- `metodo_pago`

These columns are not required for the core validation process. When present, they are normalized and used to generate additional sales analysis summaries.

Example:

producto_id,producto,categoria,precio,cantidad,fecha
P001,Producto A,Categoria A,150.50,2,2026-07-01
P002,Producto B,Categoria B,89.90,5,2026-07-02

A CSV file may also include the optional fields: 

producto_id,producto,categoria,precio,cantidad,fecha,ciudad,metodo_pago 
P001,Producto A,Categoria A,150.50,2,2026-07-01,Guadalajara,Tarjeta 
P002,Producto B,Categoria B,89.90,5,2026-07-02,Zapopan,Efectivo

### Running the Application

Run the application from the project root directory:

python main.py

The application will perform the following workflow:

1. Validate the source CSV file. 
2. Read the file into a pandas `DataFrame`. 
3. Normalize and validate the sales records. 
4. Separate valid and invalid rows. 
5. Analyze the valid sales data. 
6. Generate a structured plain-text report. 
7. Generate a shared dynamic base filename. 
8. Save the plain-text sales report. 
9. Save the complete analysis results as a JSON file. 
10. Save the product and category analysis summaries as independent CSV files. 
11. Save city and payment method CSV summaries when the corresponding optional data is available. 
12. Display the paths of the generated files. 
13. Display the total execution time.

### Generated Output Files

The generated files are saved inside the `reports` directory.

All files created during the same execution share a dynamically generated base filename contining the current date and time.

For example:

`reports/sales_report_2026-08-28_16-30-25-125.txt` 
`reports/sales_report_2026-08-28_16-30-25-125.json` 
`reports/sales_report_2026-08-28_16-30-25-125_products.csv` 
`reports/sales_report_2026-08-28_16-30-25-125_categories.csv` 

When optional analysis data is available, the application may also generate: 

`reports/sales_report_2026-08-28_16-30-25-125_cities.csv` 
`reports/sales_report_2026-08-28_16-30-25-125_payment_methods.csv`

If the `reports` directory does not exist, the application creates it automatically.

Each ececution generates a new dynamic base filename, allowing repor files from different executions to be stored independently.

### Console Output

After a successful execution, the console displays the generated text and JSON file paths, the generated CSV analysis file paths, and the total execution time. 

For example: 

Report saved at: reports/sales_report_2026-08-28_16-30-25-125.txt 
Report saved at: reports/sales_report_2026-08-28_16-30-25-125.json 
Reports CSV product_summary: reports/sales_report_2026-08-28_16-30-25-125_products.csv
category_summary: reports/sales_report_2026-08-28_16-30-25-125_categories.csv 
city_summary: reports/sales_report_2026-08-28_16-30-25-125_cities.csv 
payment_method_summary: reports/sales_report_2026-08-28_16-30-25-125_payment_methods.csv 

Execution time: 0.0123 seconds 

The city and payment method CSV paths are displayed only when those optional analyses are available.

If an application-specific error occurs, the corresponding error message is displayed and the reporting workflow stops.

---

### Custom Exceptions Module

The custom exceptions module defines the application-specific errors used throughout the Sales Report project.

Its purpose is to make failures easier to identify, handle, and report from the main application flow.

All custom exceptions inherit from `AppError`, which acts as the base exception for expected application errors.

The module currently handles errors related to:

- Empty, missing, or invalid file paths.
- Unsupported file extensions.
- Empty or unreadable CSV files.
- Missing or invalid CSV headers.
- Missing required columns.
- Invalid CSV structures.
- Empty or unusable DataFrames.
- Data validation failures.
- Absence of valid rows for analysis.
- Report generation failures.
- Report saving failures.

#### Exception Hierarchy

- `AppError`: Base class for all application-specific exceptions.
- `EmptyPathError`: Raised when the provided file path is empty.
- `FileNotFoundAppError`: Raised when the provided file path does not exist.
- `InvalidFilePathError`: Raised when the path does not point to a valid file.
- `InvalidFileExtensionError`: Raised when the file extension is not supported.
- `EmptyFileError`: Raised when the CSV file contains no data.
- `FileReadError`: Raised when the CSV file cannot be read correctly.
- `MissingColumnsError`: Raised when required columns are missing.
- `EmptyHeadersError`: Raised when the CSV file has no valid headers.
- `InvalidCSVStructureError`: Raised when the CSV structure is invalid.
- `EmptyDataFrameError`: Raised when the DataFrame contains no usable data.
- `DataValidationError`: Raised when the DataFrame validation process fails.
- `NoValidRowsError`: Raised when no valid rows are available for analysis.
- `ReportGenerationError`: Raised when the report content cannot be generated.
- `ReportSaveError`: Raised when the report file cannot be saved.

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

The report file management module handles the storage of generated sales reports and structured analysis result in the file system.

The module generates a shared dynamic base file name that can be use to save the plain-text report, the complete JSON analysis, and individual CSV analysis summaries.

The module currently provides the following functions:

- `save_report()`
- `create_report_base_name()`
- `save_analysis_json()`
- `save_analysis_result_csv_files()`
- `create_save_analysis_result_csv_files_and_path()`

#### Report Saving Process

The `save_report()` function performs the following operations:

1. Receives th generated report text.
2. Receives the destination folder.
3. Receives a previously generated base filename.
4. Add the `.txt` extension to the base filename.
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

The same base can be used to generate different output files with the same timestamp, such as:

`sales_report_2026-08-23_13-45-30-125.txt`

`sales_report_2026-08-23_13-45-30-125.json`

The same base filename is also used to generate the individual CSV analysis summaries.

for Example:

`sales_report_2026-08-23_13-45-30-125_products.csv`

`sales_report_2026-08-23_13-45-30-125_categories.csv`

#### JSON Analysis Saving Process

The `save_analysis_json()` function saves the complete sales analysis result as a JSON file.

Before serealization, pandas `DataFrame` summaries are converted into list of dictionaries.

The following summaries are converted:

- `product_summary`
- `category_summary`
- `city_summary` when available
- `payment_method_summary` when available

The function adds the `.json` extension to the provided base filename and writes the resulting JSON file using UTF-8 encoding and formatted indentation.

#### CSV Analysis Summary Saving Process

The `save_analysis_result_csv_files()` function saves aggregated analysis summaries as independent CSV files.

The following summaries are always saved:

- `product_summary`
- `category_summary`

The followin summaries are saved only when they are available:

- `city_summary`
- `payment_method_summary`

Each generated CSV file uses the shared base filename followed by a descriptive suffix.

The function returns a dictionary containing the paths of the generated CSV files.

#### Individual CSV File Creation

The `create_save_analysis_result_csv_files_and_path()` function creates and saves a single analysis summary CSV file.

It receives a pandas `DataFrame`, the destination folder, the shared base filename, and a descriptive prefix.

The function creates the destination directory when necessary, generates the complete CSV filename, saves the DataFrame without its pandas index, and returns the resulting `Path` object.

#### Input and Output

##### `save_report()`

- **Input:** The complete report text, the destination folder, and a base filename without an extension.
- **Output:** A `Path` object pointing to the saved report file.

The output folder may be provided as either a string or a `Path` object.

#### `create_report_base_name()`

- **Input:** None.
- **Output:** A dynamic base filename containing the `sales_report` prefix and the current date and time.

#### `save_analysis_json()`

- **Input:** The analysis-result dictionary, the destination folder, and a base filename without an extension.
- **Output:** A `Path` object pointing to the saved JSON analysis file.

#### `save_analysis_result_csv_files()`

- **Input:** The analysis-result dictionary, the destination folder, and a shared base filename without an extension.
- **Output:** A dictionary containing the `Path` objects of the generated CSV analysis files.

#### `create_save_analysis_result_csv_files_and_path()`

- **Input:** A pandas `DataFrame`, the destination folder, a shared base filename, and a descriptive prefix.
- **Output:** A `Path` object pointing to the saved CSV file.

#### Error Handling

File-system errors produced while creating destination directories, writing the text report, or writing the JSON analysis file are converted into the custom `ReportSaveError` exception.

#### Related Exception

- `ReportSaveError`

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
