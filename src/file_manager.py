"""Report file management and export module.

This module handles the storage and export of generated sales reports and
structured analysis results.

It creates destination directories when necessary, generates a shared
timestamp-based filename, saves human-readable reports as TXT files,
exports complete analysis results as JSON, saves aggregated analysis
summaries as independent CSV files, and generates Excel workbooks containing
multiple analysis and validation worksheets.

Exported analysis data may include product, category, monthly, city, and
payment-method summaries, together with general metrics, Top 5 product
rankings, validation errors, and validation warnings.

TXT and JSON files are written using UTF-8 encoding. CSV files are generated
from pandas DataFrames, while XLSX worksheets are populated from analysis
results using openpyxl.
"""
from pathlib import Path
from datetime import datetime
import pandas as pd
import json
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils.dataframe import dataframe_to_rows

from typing import Dict, Any, List

from src.errors import ReportSaveError


def save_report(
        report_text: str,
        output_folder: str | Path,
        file_name: str
) -> Path:
    """Save a generated sales report as a TXT file.

    Creates the destination directory and any missing parent directories before
    writing the report.

    The function receives a previously generated shared base filename, adds the
    `.txt` extension, and writes the report content using UTF-8 encoding.

    Args:
        report_text: Complete human-readable report content to save.
        output_folder: Directory where the TXT report will be stored.
        file_name: Shared base filename without a file extension.

    Returns:
        Path to the generated TXT report.

    Raises:
        ReportSaveError: If the destination directory cannot be created or the
            report file cannot be written because of a file-system error.
    """
    output_filename = f"{file_name}.txt"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        with open(path, "w", encoding="utf-8") as file:
            file.write(report_text)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def create_report_base_name() -> str:
    """Generate a shared timestamp-based filename for report output files.

    Uses the current local date and time to create a timestamp containing the
    year, month, day, hour, minute, second, and milliseconds.

    The timestamp is combined with the `sales_report` prefix. The resulting
    base filename can be reused by the TXT, JSON, CSV, and XLSX export
    functions so that files generated during the same report process share
    the same identifier.

    Returns:
        A base filename formatted as
        `sales_report_YYYY-MM-DD_HH-MM-SS-fff`.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    file_name = f"sales_report_{timestamp}"
    return file_name

def save_analysis_json(
        analysis_result: Dict[str, Any], 
        output_folder: str | Path, 
        file_name: str
) -> Path:
    """Save the complete sales analysis result as a JSON file.

    Creates a copy of the analysis result and converts pandas DataFrame
    summaries into lists of dictionaries so that they can be serialized
    to JSON.

    Product, category, and monthly summaries are always converted. City and
    payment-method summaries are also converted when they are present and
    contain analysis data.

    The function receives a previously generated shared base filename, adds
    the `.json` extension, creates the destination directory when necessary,
    and writes the resulting structure using UTF-8 encoding.

    Args:
        analysis_result: Dictionary containing the complete sales analysis
            results.
        output_folder: Directory where the JSON analysis file will be stored.
        file_name: Shared base filename without a file extension.

    Returns:
        Path to the generated JSON analysis file.

    Raises:
        ReportSaveError: If the destination directory cannot be created or the
            JSON file cannot be written because of a file-system error.
    """
    analysis_json = analysis_result.copy()
    analysis_json["product_summary"] = analysis_json["product_summary"].to_dict(orient="records")
    analysis_json["category_summary"] = analysis_json["category_summary"].to_dict(orient="records")
    analysis_json["monthly_summary"] = analysis_json["monthly_summary"].to_dict(orient="records")
    if "city_summary" in analysis_json.keys() and analysis_json["city_summary"] is not None:
        analysis_json["city_summary"] = analysis_json["city_summary"].to_dict(orient="records")
    if "payment_method_summary" in analysis_json.keys() and analysis_json["payment_method_summary"] is not None:
        analysis_json["payment_method_summary"] = analysis_json["payment_method_summary"].to_dict(orient="records")
    output_filename = f"{file_name}.json"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        with open(path, "w", encoding="utf-8") as file:
            json.dump(analysis_json, file, indent=4, ensure_ascii=False)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def save_analysis_result_csv_files(
        analysis_result: Dict[str, Any], 
        output_folder: str | Path, 
        file_name: str
) -> Dict[str, Any]:
    """Save analysis summary DataFrames as independent CSV files.

    Creates individual CSV files for the product, category, and monthly
    summaries. Optional city and payment-method summaries are also exported
    when they are available in the analysis result.

    Each generated file uses the shared report base filename followed by a
    descriptive suffix identifying the corresponding analysis summary.

    The creation and storage of each individual CSV file is delegated to
    `create_save_analysis_result_csv_files_and_path()`.

    Args:
        analysis_result: Dictionary containing the complete sales analysis
            results and summary DataFrames.
        output_folder: Directory where the CSV files will be stored.
        file_name: Shared base filename without a file extension.

    Returns:
        A dictionary containing the generated CSV file paths. The dictionary
        always contains `resumen_producto`, `resumen_categoria`, and
        `resumen_mensual`. It may also contain `ciudad_resumen` and
        `metodo_de_pago_resumen` when the corresponding optional analyses
        are available.
    """
    analysis_csv = analysis_result.copy()
    reports = {}
    reports["resumen_producto"] = create_save_analysis_result_csv_files_and_path(analysis_csv["product_summary"], output_folder, file_name, "products")
    reports["resumen_categoria"] = create_save_analysis_result_csv_files_and_path(analysis_csv["category_summary"], output_folder, file_name, "categories")
    reports["resumen_mensual"] = create_save_analysis_result_csv_files_and_path(analysis_result["monthly_summary"], output_folder, file_name, "months")
    if "city_summary" in analysis_csv and analysis_csv["city_summary"] is not None:
        reports["ciudad_resumen"] = create_save_analysis_result_csv_files_and_path(analysis_csv["city_summary"], output_folder, file_name, "cities")
    if "payment_method_summary" in analysis_csv and analysis_csv["payment_method_summary"] is not None:
        reports["metodo_de_pago_resumen"] = create_save_analysis_result_csv_files_and_path(analysis_csv["payment_method_summary"], output_folder, file_name, "payment_methods")
    return reports

def create_save_analysis_result_csv_files_and_path(
        df: pd.DataFrame, 
        folder: str | Path, 
        file_name: str, 
        prefix: str
) -> Path:
    """Create and save an individual analysis summary as a CSV file.

    Builds the output filename using the shared report base filename and a
    descriptive suffix, creates the destination directory when necessary,
    and exports the provided pandas DataFrame without its index.

    Args:
        df: DataFrame containing the analysis summary to export.
        folder: Directory where the CSV file will be stored.
        file_name: Shared base filename without a file extension.
        prefix: Descriptive filename suffix identifying the analysis summary.

    Returns:
        Path to the generated CSV file.

    Raises:
        ReportSaveError: If the destination directory cannot be created or the
            CSV file cannot be written because of a file-system error.
    """
    output_filename = f"{file_name}_{prefix}.csv"
    try:
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        df.to_csv(path, index=False)
    except OSError as error:
        raise ReportSaveError() from error
    return path

def build_sheet_general_summary(wb: Workbook, analysis_result: Dict[str, Any]) -> Worksheet:
    """Build the general sales summary worksheet.

    Creates a worksheet named `Resumen General` and populates it with the main
    sales-processing metrics contained in the analysis result.

    The worksheet contains the total number of rows, valid rows, invalid rows,
    total income, and total units sold.

    Args:
        wb: Excel workbook where the worksheet will be created.
        analysis_result: Dictionary containing the calculated sales metrics.

    Returns:
        The created `Worksheet` containing the general sales summary.
    """
    ws = wb.create_sheet("Resumen General")
    headers = ["Métrica", "Valor"]
    ws.append(headers)
    ws.append(["Total de filas", analysis_result["total_rows"]])
    ws.append(["Filas válidas", analysis_result["total_valid_rows"]])
    ws.append(["Filas inválidas", analysis_result["total_invalid_rows"]])
    ws.append(["Ingreso total", analysis_result["total_income"]])
    ws.append(["Unidades vendidas", analysis_result["total_units_sold"]])
    return ws

def build_sheet_products(wb: Workbook, df: pd.DataFrame) -> Worksheet:
    """Build the product summary worksheet.

    Creates a worksheet named `Productos` and populates it with the complete
    product-summary DataFrame.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        df: DataFrame containing the aggregated product analysis.

    Returns:
        The created `Worksheet` containing the product summary.
    """
    ws = wb.create_sheet("Productos")
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_categories(wb: Workbook, df: pd.DataFrame) -> Worksheet:
    """Build the categories summary worksheet.

    Creates a worksheet named `Categorías` and populates it with the complete
    category-summary DataFrame.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        df: DataFrame containing the aggregated category analysis.

    Returns:
        The created `Worksheet` containing the category summary.
    """
    ws = wb.create_sheet("Categorías")
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_bestselling(wb: Workbook, top_best_products: List[Dict[str, Any]]) -> Worksheet:
    """Build the Top 5 best-selling products worksheet.

    Creates a worksheet named `Productos mejor vendidos`, converts the
    received Top 5 product data into a pandas DataFrame, and writes the
    resulting rows to the worksheet.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        top_best_products: Collection containing the Top 5 best-selling
            product records.

    Returns:
        The created `Worksheet` containing the best-selling product ranking.
    """
    ws = wb.create_sheet("Productos mejor vendidos")
    df = pd.DataFrame(top_best_products)
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_top_income(wb: Workbook, top_highest_income_products: List[Dict[str,Any]]) -> Worksheet:
    """Build the Top 5 highest-income products worksheet.

    Creates a worksheet named `Productos con mejor ingreso`, converts the
    received Top 5 product data into a pandas DataFrame, and writes the
    resulting rows to the worksheet.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        top_highest_income_products: Collection containing the Top 5 products
            ranked by generated income.

    Returns:
        The created `Worksheet` containing the highest-income product ranking.
    """
    ws = wb.create_sheet("Productos con mejor ingreso")
    df = pd.DataFrame(top_highest_income_products)
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_city_summary(wb: Workbook, df: pd.DataFrame) -> Worksheet:
    """Build the city summary worksheet.

    Creates a worksheet named `Resumen por ciudad` and populates it with the
    city-summary DataFrame.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        df: DataFrame containing aggregated sales analysis by city.

    Returns:
        The created `Worksheet` containing the city summary.
    """
    ws = wb.create_sheet("Resumen por ciudad")
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_payment_method_summary(wb: Workbook, df: pd.DataFrame) -> Worksheet:
    """Build the payment-method summary worksheet.

    Creates a worksheet named `Resumen por metodo de pago` and populates it
    with the payment-method summary DataFrame.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    Args:
        wb: Excel workbook where the worksheet will be created.
        df: DataFrame containing aggregated sales analysis by payment method.

    Returns:
        The created `Worksheet` containing the payment-method summary.
    """
    ws = wb.create_sheet("Resumen por método de pago")
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_monthly_summary(wb: Workbook, df: pd.DataFrame) -> Worksheet:
    """Build the monthly sales summary worksheet.

    Creates a worksheet named `Resumen por mes` and populates it with the
    monthly-summary DataFrame.

    The DataFrame column names are included as worksheet headers, while the
    pandas index is excluded.

    The worksheet contains the monthly sales information calculated by the
    analysis module, including valid row totals, units sold, and total income.

    Args:
        wb: Excel workbook where the worksheet will be created.
        df: DataFrame containing aggregated monthly sales analysis.

    Returns:
        The created `Worksheet` containing the monthly sales summary.
    """
    ws = wb.create_sheet("Resumen por mes")
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)
    return ws

def build_sheet_validation_errors(wb: Workbook, errors: List[Dict[str, Any]]) -> Worksheet:
    """Build the validation-errors worksheet.

    Creates a worksheet named `Validación de errores` containing the
    validation errors detected while processing the source sales data.

    Internal error dictionary keys are mapped to Spanish worksheet headers.
    Each error is written using the predefined column order, and missing
    values are replaced with an empty string.

    Args:
        wb: Excel workbook where the worksheet will be created.
        errors: List of dictionaries containing validation error records.

    Returns:
        The created `Worksheet` containing the validation error records.
    """
    ws = wb.create_sheet("Validación de errores")
    map_headers = {
        "line_number": "línea",
        "column": "columna",
        "error_type": "tipo_error",
        "message": "mensaje",
        "original_value": "valor_original"
    }
    ws.append(list(map_headers.values()))
    for error in errors:
        row = [error.get(value, "") for value in map_headers.keys()]
        ws.append(row)
    return ws

def build_sheet_warnings(wb: Workbook, warnings: List[Dict[str, Any]]) -> Worksheet:
    """Build the validation-warnings worksheet.

    Creates a worksheet named `Advertencias` containing warnings detected
    during sales-data validation.

    Internal warning dictionary keys are mapped to Spanish worksheet headers.
    Each warning is written using the predefined column order, and missing
    values are replaced with an empty string.

    Warning values stored as lists are converted into comma-separated text
    before being written to the worksheet.

    Args:
        wb: Excel workbook where the worksheet will be created.
        warnings: List of dictionaries containing validation warning records.

    Returns:
        The created `Worksheet` containing the validation warning records.
    """
    ws = wb.create_sheet("Advertencias")
    map_headers = {
        "warning_type": "tipo_advertencia",
        "field": "campo",
        "message": "mensaje",
        "affected_value": "valor_afectado",
        "details": "detalles"
    }
    ws.append(list(map_headers.values()))
    for warning in warnings:
        processed_row = []
        for internal_key in map_headers.keys():
            value = warning.get(internal_key, "")
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            processed_row.append(value)
        ws.append(processed_row)
    return ws

def save_report_xlsx(
        analysis_result: Dict[str, Any], 
        errors, 
        warnings, 
        output_folder: str | Path, 
        file_name: str
) -> Path:
    """Generate and save the complete sales analysis as an Excel workbook.

    Creates an XLSX workbook containing multiple worksheets representing the
    main sales analysis, monthly analysis, rankings, optional summaries,
    validation errors, and validation warnings.

    The default worksheet created by openpyxl is removed before the report
    worksheets are generated.

    The workbook always includes general, product, category, monthly,
    Top 5 best-selling product, Top 5 highest-income product, validation-error,
    and validation-warning worksheets.
                        
    City and payment-method worksheets are also generated when the
    corresponding analysis results are available.

    The function receives a previously generated shared base filename, adds
    the `.xlsx` extension, creates the destination directory when necessary,
    and saves the completed workbook.

    Args:
        analysis_result: Dictionary containing the complete sales analysis
            results and summary structures.
        errors: Collection containing validation error records.
        warnings: Collection containing validation warning records.
        output_folder: Directory where the XLSX workbook will be stored.
        file_name: Shared base filename without a file extension.

    Returns:
        Path to the generated XLSX workbook.

    Raises:
        ReportSaveError: If the destination directory cannot be created or the
            workbook cannot be saved because of a file-system error.
    """ 
    output_filename = f"{file_name}.xlsx"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename

        wb = Workbook()
        wb.remove(wb.active)

        build_sheet_general_summary(wb, analysis_result)
        build_sheet_products(wb, analysis_result["product_summary"])
        build_sheet_categories(wb, analysis_result["category_summary"])
        build_sheet_monthly_summary(wb, analysis_result["monthly_summary"])
        if "city_summary" in analysis_result and analysis_result["city_summary"] is not None:
            build_sheet_city_summary(wb, analysis_result["city_summary"])
        if "payment_method_summary" in analysis_result and analysis_result["payment_method_summary"] is not None:
            build_sheet_payment_method_summary(wb, analysis_result["payment_method_summary"])
        build_sheet_bestselling(wb, analysis_result["top_5_best_selling_products"])
        build_sheet_top_income(wb, analysis_result["top_5_highest_income_products"])
        build_sheet_validation_errors(wb, errors)
        build_sheet_warnings(wb, warnings)
        wb.save(path)
    except OSError as error:
        raise ReportSaveError() from error
    return path