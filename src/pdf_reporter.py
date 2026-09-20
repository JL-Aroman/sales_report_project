"""PDF report generation module.

This module converts structured sales-analysis results, validation information,
and previously generated chart images into a complete PDF sales report using
ReportLab.

The PDF includes a title derived from the source CSV filename, general sales
metrics, structured analysis tables, generated chart images, validation errors,
and validation warnings.

Analysis structures stored as pandas DataFrames or lists of dictionaries are
converted into ReportLab tables. Table titles and column headers are formatted
for human-readable presentation in Spanish.

Generated chart images are embedded into the document using the paths produced
by the chart-generation module.

The main `save_pdf_reporter()` function coordinates the complete PDF-generation
workflow and converts supported generation or file-system failures into the
application-specific `PDFGenerationError` exception.
"""


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet as style
from reportlab.lib import colors
from pathlib import Path
from src.errors import PDFGenerationError
import pandas as pd
from typing import Dict, Any, List


TRANSLATE_TITLES = {
    "product_summary": "Resumen de Productos",
    "category_summary": "Resumen de Categorías",
    "monthly_summary": "Resumen Mensual",
    "best_selling_product": "Producto Más Vendido",
    "highest_income_product": "Producto con Mayor Ingreso",
    "highest_income_category": "Categoría con Mayor Ingreso",
    "top_5_best_selling_products": "Top 5 Productos Más Vendidos",
    "top_5_highest_income_products": "Top 5 Productos con Mayor Ingreso",
    "monthly_best_selling_product": "Producto Más Vendido Mensual",
    "monthly_highest_income_category": "Categoría con Mayor Ingreso Mensual",
    "city_summary": "Resumen por Ciudad",
    "highest_income_city": "Ciudad con Mayor Ingreso",
    "payment_method_summary": "Resumen por Método de Pago",
    "highest_income_payment_method": "Método de Pago con Mayor Ingreso",
}
WIDTH_PAGE, HEIGHT_PAGE = letter
MARGIN = 72

def get_title_pdf(input_file_name: Path) -> Paragraph:
    """Create the main PDF title from the source CSV filename.

    Extracts the source filename without its extension, replaces underscores
    with spaces, joins the resulting words, capitalizes the final text, and
    creates a ReportLab title paragraph.

    Args:
        input_file_name: Path of the source CSV file used to generate the
            sales report.

    Returns:
        A ReportLab `Paragraph` containing the formatted PDF title.
    """
    file_name = input_file_name.stem
    file_name = str(file_name).split("_")
    file_name = " ".join(file_name)
    file_name = file_name.capitalize()
    title = Paragraph(file_name, style()["Title"])
    return title

def get_title_table_spanish(title: str) -> Paragraph:
    """Create a Spanish title for an analysis table.

    Searches `TRANSLATE_TITLES` for a predefined Spanish representation of the
    supplied analysis-result key.

    When no predefined translation exists, underscores are replaced with spaces
    and the resulting text is converted to uppercase.

    Args:
        title: Analysis-result key used to identify the table.

    Returns:
        A ReportLab `Paragraph` containing the formatted table title.
    """
    text = TRANSLATE_TITLES.get(title, title.replace("_", " ").upper())
    return Paragraph(text, style()["Heading2"])

def get_widths_columns(num_columns: int) -> List[float]:
    """Calculate equal column widths for a PDF table.

    Calculates the usable page width by subtracting the configured left and
    right margins from the page width.

    The remaining width is divided equally among all table columns.

    Args:
        num_columns: Number of columns contained in the table.

    Returns:
        A list containing one equal width value for each table column.
    """
    width_available = WIDTH_PAGE - (MARGIN * 2)
    width_column = width_available / num_columns
    return [width_column] * num_columns

def normalize_headers(headers: List[str]) -> List[str]:
    """Convert DataFrame column names into readable table headers.

    Replaces underscores with spaces and capitalizes each supplied column name.

    Args:
        headers: List containing the original DataFrame column names.

    Returns:
        A list containing the normalized human-readable column headers.
    """
    new_headers = []
    for head in headers:
        head = head.replace("_", " ").capitalize()
        new_headers.append(head)
    return new_headers

def get_table(df: pd.DataFrame) -> Table:
    """Convert a pandas DataFrame into a formatted ReportLab table.

    Normalizes the DataFrame column headers, converts DataFrame rows into
    table-compatible lists, calculates equal column widths, and creates a
    ReportLab `Table`.

    A grid is applied to every generated table.

    Tables containing eight columns use a font size of 5, while tables
    containing six columns use a font size of 7. Other table sizes use the
    default ReportLab font size.

    The first row is configured as a repeating header when a table extends
    across multiple PDF pages.

    Args:
        df: DataFrame containing the information to represent in the PDF.

    Returns:
        A formatted ReportLab `Table`.
    """
    original_headers = list(df.columns)
    headers = normalize_headers(original_headers)
    rows = df.values.tolist()
    list_for_table = [headers] + rows
    widths = get_widths_columns(len(headers))
    table = Table(list_for_table, colWidths=widths)
    if len(headers) == 8:
        table.setStyle(TableStyle([
            ("FONTSIZE", (0,0), (-1,-1), 5),
            ("GRID", (0,0), (-1, -1), 0.5, colors.black),
        ]))
    elif len(headers) == 6:
        table.setStyle(TableStyle([
            ("FONTSIZE", (0,0), (-1,-1), 7),
            ("GRID", (0,0), (-1, -1), 0.5, colors.black),
        ]))
    else:
        table.setStyle(TableStyle([
                    ("GRID", (0,0), (-1, -1), 0.5, colors.black),
                ]))
    table.repeatRows = 1
    return table

def get_tables(analysis_result: Dict[str, Any]) -> List:
    """Create PDF table elements from structured analysis results.

    Iterates through the complete analysis-result dictionary and converts
    supported structured values into ReportLab tables.

    Lists are converted into pandas DataFrames before table generation.
    Existing pandas DataFrames are used directly.

    Empty lists and empty DataFrames are omitted.

    Missing DataFrame values are replaced with `N/D` before the table is
    created.

    Scalar analysis values are ignored because general metrics are displayed
    separately through `get_general_summary()`.

    Each generated table is preceded by its Spanish section title and separated
    from surrounding content using ReportLab `Spacer` elements.

    Args:
        analysis_result: Dictionary containing the complete structured
            sales-analysis result.

    Returns:
        A list containing ReportLab paragraphs, tables, and spacers ready to
        be added to the PDF document.
    """
    elements = []
    for key, value in analysis_result.items():
        title_spanish = get_title_table_spanish(key)
        if isinstance(value, list):
            if len(value) == 0:
                continue
            table = get_table(pd.DataFrame(value).fillna("N/D"))
        elif isinstance(value, pd.DataFrame):
            if value.empty:
                continue
            table = get_table(value.fillna("N/D"))
        else:
            continue
        elements.append(title_spanish)
        elements.append(Spacer(1,12))
        elements.append(table)
        elements.append(Spacer(1,12))
    return elements

def get_image(file_path: str | Path) -> Image:
    """Create a ReportLab image element from a generated chart file.

    Creates an image using the supplied chart path and scales it to the
    available PDF page width with a fixed height of 300 points.

    Args:
        file_path: Path of the PNG chart image to embed in the PDF.

    Returns:
        A ReportLab `Image` ready to be added to the document.
    """
    grafica = Image(file_path, width=WIDTH_PAGE - (MARGIN * 2), height=300)
    return grafica

def get_charts(charts: Dict[str, Path]) -> List:
    """Create PDF image elements from generated sales charts.

    Iterates through the chart-path dictionary produced by the chart-generation
    module and converts every chart path into a ReportLab image.

    A spacer is added after each chart to visually separate consecutive images.

    Args:
        charts: Dictionary mapping chart identifiers to generated PNG paths.

    Returns:
        A list containing ReportLab images and spacers ready to be added to
        the PDF document.
    """
    elements = []
    for _, value in charts.items():
        chart = get_image(value)
        elements.append(chart)
        elements.append(Spacer(1,12))
    return elements

def get_general_summary(analysis_result: Dict[str, Any]) -> Paragraph:
    """Create the general sales summary for the PDF report.

    Formats the primary sales metrics into a ReportLab paragraph.

    The summary includes:

    - Total processed rows.
    - Total valid rows.
    - Total invalid rows.
    - Total income.
    - Total units sold.

    Total income is formatted as currency using thousands separators and two
    decimal places.

    Args:
        analysis_result: Dictionary containing the calculated sales metrics.

    Returns:
        A ReportLab `Paragraph` containing the general sales summary.
    """
    summary = Paragraph(f"""
RESUMEN GENERAL <br/>
<br/>
Total de filas: {analysis_result["total_rows"]}<br/>
Filas válidas: {analysis_result["total_valid_rows"]}<br/>
Filas inválidas: {analysis_result["total_invalid_rows"]}<br/>
Ingreso Total: ${analysis_result["total_income"]:,.2f}<br/>
Unidades vendidas: {analysis_result["total_units_sold"]}<br/>
""", style()["Normal"])
    return summary

def get_errors(errors: List[Dict[str, Any]]) -> Paragraph:
    """Create the validation-errors section for the PDF report.

    Sorts validation errors by CSV line number and converts them into
    human-readable text.

    For each validation error, the generated section includes the line number,
    affected column, error type, descriptive message, and original value when
    available.

    When no validation errors are available, the section indicates that no
    validation errors were found.

    Args:
        errors: List containing validation-error dictionaries.

    Returns:
        A ReportLab `Paragraph` containing the formatted validation-errors
        section.
    """
    summary = []
    summary.append("ERRORES DE VALIDACIÓN<br/>")
    if len(errors) < 1:
        summary.append("No se encontraron errores de validación.")
        return Paragraph("<br/>".join(summary), style()["Normal"])
    sorted_errors = sorted(errors, key=lambda x: x["line_number"])
    for error in sorted_errors:
        if error["original_value"] == "":
            summary_errors = f"""<br/>
- Línea {error["line_number"]} | {error["column"]} | {error["error_type"]} | {error["message"]}"""
        else:
            summary_errors = f"""<br/>
- Línea {error["line_number"]} | {error["column"]} | {error["error_type"]} | {error["message"]} 
  Valor original: {error['original_value']}"""
        summary.append(summary_errors)
    summary.append("")
    return Paragraph("<br/>".join(summary), style()["Normal"])

def get_warnings(warnings: List[Dict[str, Any]]) -> Paragraph:
    """Create the validation-warnings section for the PDF report.

    Sorts validation warnings by `affected_value` and converts them into
    human-readable text.

    For each warning, the generated section includes the affected product
    identifier, warning type, descriptive message, and warning details.

    Multiple warning-detail values are joined using comma-separated text.

    When no validation warnings are available, the section indicates that no
    warnings were found.

    Args:
        warnings: List containing validation-warning dictionaries.

    Returns:
        A ReportLab `Paragraph` containing the formatted validation-warnings
        section.
    """
    summary = []
    summary.append("ADVERTENCIAS<br/>")
    if len(warnings) < 1:
        summary.append("No se encontraron advertencias<br/>")
        return Paragraph("<br/>".join(summary), style()["Normal"])
    sorted_warnings = sorted(warnings, key=lambda x: x["affected_value"])
    for warning in sorted_warnings:
        summary_warning = f"""<br/>
- producto_id {warning["affected_value"]} | {warning["warning_type"]} | {warning["message"]} <br/>
  Detalles: {", ".join(warning["details"])}"""
        summary.append(summary_warning)
    return Paragraph("<br/>".join(summary), style()["Normal"])

def save_pdf_reporter(
        analysis_result: Dict[str, Any], 
        output_folder: str | Path, 
        file_base_name: str, 
        input_file_name: Path,
        validation_result: Dict[str, Any],
        charts: Dict[str, Path]
    ) -> Path:
    """Generate and save the complete PDF sales report.

    Coordinates the PDF-generation workflow using ReportLab.

    The function creates the destination directory when necessary, constructs
    the output PDF path, initializes a letter-sized `SimpleDocTemplate`, and
    builds the document from independently generated ReportLab elements.

    The PDF currently includes:

    - A title derived from the source CSV filename.
    - A general sales summary.
    - Structured analysis tables.
    - Generated PNG chart images.
    - Validation errors.
    - Validation warnings.

    Analysis lists and DataFrames are converted into tables through
    `get_tables()`. Generated chart paths are converted into image elements
    through `get_charts()`.

    The PDF uses the shared report base filename supplied by the controller so
    it remains associated with the other outputs generated during the same
    workflow.

    Args:
        analysis_result: Dictionary containing the complete structured
            sales-analysis result.
        output_folder: Directory where the generated PDF file will be stored.
        file_base_name: Shared base filename used by the report-generation
            workflow.
        input_file_name: Path of the original source CSV file, used to create
            the PDF title.
        validation_result: Dictionary containing validation information,
            including `errors` and `warnings`.
        charts: Dictionary mapping chart identifiers to generated PNG paths.

    Returns:
        Path to the generated PDF report.

    Raises:
        PDFGenerationError: If the output directory or PDF document cannot be
            generated because of a supported file-system or value error.
    """
    try:
        output_file_name = f"{file_base_name}.pdf"
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_file_name
        path_for_doc = str(path)
        doc = SimpleDocTemplate(path_for_doc, pagesize=letter)
        elements = []
        elements.append(get_title_pdf(input_file_name))
        elements.append(Spacer(1,12))
        elements.append(get_general_summary(analysis_result))
        elements.append(Spacer(1,12))
        elements = elements + get_tables(analysis_result)
        elements = elements + get_charts(charts)
        elements.append(Spacer(1,12))
        elements.append(get_errors(validation_result["errors"]))
        elements.append(Spacer(1,12))     
        elements.append(get_warnings(validation_result["warnings"]))
        doc.build(elements)
    except(OSError, ValueError) as error:
        raise PDFGenerationError() from error
    return path
