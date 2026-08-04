"""Sales report generation module.

This module converts sales analysis results, validation errors, and warnings
into a structured plain-text- report.

Each report section is gnerated by an independent helper function to keep
the reportin workflow modular, maintainable, and easy to extend. The main
report function coordinates these helpers and combines their output into a
complete sales report.
"""

from datetime import date
from pathlib import Path
from typing import Dict, Any, List


def get_general_summary(analysis_result: Dict[str, Any]) -> str:
    """Generate the general sales summary section.

    Extracts rows totals, total income, and total units sold from the analysis
    result. Monetary values are formatted with thousands separators and two
    decimal places.

    Args:
        analysis_result: Dictionary containing the general metrics produced
            by the sales analysis process.

    Returns:
        A formatted string containing the general sales summary.
    """
    general_summary = f"""
GENERAL SUMMARY

Total rows: {analysis_result["total_rows"]}
Valid rows: {analysis_result["total_valid_rows"]}
Invalid rows: {analysis_result["total_invalid_rows"]}
Total income: ${analysis_result["total_income"]:,.2f}
Total units sold: {analysis_result["total_units_sold"]}
"""
    return general_summary
   
def get_best_selling_product(analysis_result: Dict[str, Any]) -> str:
    """Generate the best-selling product section.

    Reads the product records stored in `best_selling_product` and formats
    their identifiers, names and total units sold.

    If multiple products shere the highest number of units sold, every tied
    product is included in the section.

    Args:
        analysis_result: Dictionary containing the sales analysis results,
            including the best-selling product records.

    Returns:
        A formatted string containing all best-selling products.
    """
    list_best_selling_products = analysis_result["best_selling_product"]
    summary = []
    summary.append("BEST SELLING PRODUCT")
    for best_selling_product in list_best_selling_products:
        summary_product = f"""
{best_selling_product["producto_id"]} - {best_selling_product["producto"]}
Units sold: {best_selling_product["unidades_vendidas"]}
"""
        summary.append(summary_product)
    return "\n".join(summary)

def get_highest_income_product(analysis_result: Dict[str, Any]) -> str:
    """Generate the highest-income product section.

    Read the product records stored in `highest_income_product` and formats
    their identifiers, names, and total generated income.

    If multiple products share the highest income, every tied product is 
    included in the section.

    Args:
        analysis_result: Dictionary containing the sales analysis results
            including the highest-income product records.

    Returns:
        A formatted string containing all products tied for the highest
            generated income.
    """
    list_highest_income_products = analysis_result["highest_income_product"]
    summary = []
    summary.append("HIGHEST INCOME PRODUCT")
    for highest_income_product in list_highest_income_products:
        summary_product = f"""
{highest_income_product["producto_id"]} - {highest_income_product["producto"]}
Income: ${highest_income_product["ingreso_total"]:,.2f}
"""
        summary.append(summary_product)
    return "\n".join(summary)

def get_highest_income_category(analysis_result: Dict[str, Any]) -> str:
    """Generate the highest-income category section.

    Reads the category records stored in `highest_income_category` and formats
    their names and total generated income.

    If multiple categories share the highest income, every tied category is
    included in the setion.

    Args:
        analysis_result: Dictionary containing the sales analysis results, 
            including the highest-income category records.

    Returns:
        A formatted string containing all categories tied for the highest 
        generated income.
    """
    list_highest_income_category = analysis_result["highest_income_category"]
    summary = []
    summary.append("HIGHEST INCOME CATEGORY")
    for highest_income_category in list_highest_income_category:
        summary_category = f"""
{highest_income_category["categoria"]}
Income: ${highest_income_category["ingreso_total"]:,.2f}
"""
        summary.append(summary_category)
    return "\n".join(summary)

def get_product_summary(analysis_result: Dict[str, Any]) -> str:
    """Generate the product summry section.

    Converts the product summary DataFrame into a plain-text table without
    including its pandas index.

    Args:
        analysis_result: dictionary containing the `product_summaty`
            DataFrame produced by the sales analysis process.

    Returns:
        a formatted string containing the aggregated product summary.
    """
    summary = []
    summary.append("PRODUCT SUMMARY")
    summary.append(f"\n{analysis_result['product_summary'].to_string(index=False)}\n")
    return "\n".join(summary)

def get_category_summary(analysis_result: Dict[str, Any]) -> str:
    """Generate the category summary section.

    Converts the category summary DataFrame into a plain-text table without
    including its pandas index.

    Args:
        analysis_result: Dictionary containing the `category_summary`
            DataFrame produced by the sales analysis process.

    Returns:
        A formatted string containig the aggregated category summary.
    """
    summary = []
    summary.append("CATEGORY SUMMARY")
    summary.append(f"\n{analysis_result['category_summary'].to_string(index=False)}\n")
    return "\n".join(summary)

def get_errors(errors: List[Dict[str, Any]]) -> str:
    """Generate the validation errors section.

    Sorts validation errors by CSV line number and formats their column,
    error type, message, and original value.

    When an error has no original value, the original-value line is omitted.
    If no errors are available, the section indicates that no validation 
    erros were found.

    Args:
        erros: List of dictionaries containing detailed validation errors.

    Returns:
        A formatted string containing the validation errors in ascending 
        line-number order.
    """
    summary = []
    summary.append("VALIDATION ERRORS")
    if len(errors) < 1:
        summary.append("No validation errors found.\n")
        return "\n".join(summary)
    sorted_errors = sorted(errors, key=lambda x: x["line_number"])
    for error in sorted_errors:
        if error["original_value"] == "":
            summary_errors = f"""
- Line {error["line_number"]} | {error["column"]} | {error["error_type"]} | {error["message"]}"""
        else:
            summary_errors = f"""
- Line {error["line_number"]} | {error["column"]} | {error["error_type"]} | {error["message"]} 
  Original value: {error['original_value']}"""
        summary.append(summary_errors)
    summary.append("")
    return "\n".join(summary)

def get_warnings(warnings: List[Dict[str, Any]]) -> str:
    """Generate the validation warnings section.

    Sorts warnings by their affected product identifier and formats the warning 
    type, message and inconsistent values.

    If no warnings are avalilable, the section indicate that no warnings
    were found.

    Args:
        warnings: List of dictionaries containing non-critical validation
            warnings.

    Returns:
        A formatted string containing the detected warnings.
    """
    summary = []
    summary.append("WARNINGS")
    if len(warnings) < 1:
        summary.append("No warnings found.\n")
        return "\n".join(summary)
    sorted_warnings = sorted(warnings, key=lambda x: x["affected_value"])
    for warning in sorted_warnings:
        summary_warning = f"""
- producto_id {warning["affected_value"]} | {warning["warning_type"]} | {warning["message"]} 
  Details: {", ".join(warning["details"])}"""
        summary.append(summary_warning)
    return "\n".join(summary)

def generate_report(
        analysis_result: Dict[str, Any],
        errors: List[Dict[str, Any]],
        warnings: List[Dict[str, Any]],
        source_filename: Path
)-> str:
    """Generate the complete plain-text sales report.

    Creates the report header and includes the source filename and generation
    date. It then coordinates the report helper functions to add general
    metrics, highest-performing records, product and category summaries,
    validation errors, and warnings.

    Args:
        analysis_result: Dicnionary containing the metrics, summaries, and 
            highest-performing records produced by the analysis process.
        errors: List of dictionaries containing detailed validation errors.
        warnings: List of dictionaries containing non-critical validation
            warnings
        source_filename: Path object representing the original CSV file.
    
    Returns:
        A complete plain-text sales report ready to be displated or saved.
    """
    summary = []
    summary.append("SALES REPORT")
    summary.append(f"""
Source file: {source_filename.name}
Generated at: {date.today()}""")
    summary.append(get_general_summary(analysis_result))
    summary.append(get_best_selling_product(analysis_result))
    summary.append(get_highest_income_product(analysis_result))
    summary.append(get_highest_income_category(analysis_result))
    summary.append(get_product_summary(analysis_result))
    summary.append(get_category_summary(analysis_result))
    summary.append(get_errors(errors))
    summary.append(get_warnings(warnings))
    return "\n".join(summary)