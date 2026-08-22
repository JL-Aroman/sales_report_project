"""Sales report generation module.

This module converts sales analysis results, validation errors, and warnings
into a structured plain-text- report.

Each report section is gnerated by an independent helper function to keep
the reportin workflow modular, maintainable, and easy to extend. The main
report function coordinates these helpers and combines their output into a
complete sales report.

The report can also include Top 5 product rankings and optional city-based
and payment-method-based sales information when these fields are available
in the analysis result.
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

def get_highest_income_city(analysis_result: Dict[str, Any]) -> str:
    """Generate the highest-income city section.

    Reads the city records stored in `highest_income_city` and formats 
    their names, total generated income, and total units sold.

    If multiple cities share the highest income, every tied city is included in the section.

    Args: 
        analysis_result: Dictionary containing the sale sanalysis results,
            including the highest-income city records.

    Returns:
        A formatted string containing all cities tied for the highest 
        generated income.
    """
    list_highest_income_city = analysis_result["highest_income_city"]
    summary = []
    summary.append("HIGHEST INCOME CITY")
    for highest_income_city in list_highest_income_city:
        summary_city = f"""
{highest_income_city["ciudad"]}
Income: ${highest_income_city["ingreso_total"]:,.2f}
Units sold: {highest_income_city["unidades_vendidas"]}
"""
        summary.append(summary_city)
    return "\n".join(summary)

def get_highest_income_payment_method(analysis_result: Dict[str, Any]) -> str:
    """Generate the highest-income payment method section.

    Reads the payment method records stored in `highest_income_payment_method`
    and formats their names, total generated income, and total units sold.

    If multiple payment methods share the highest inocme, every tied payment
    method is included in the section.

    Args:
        analysis_result: Dictionary containing the sales analysis results,
            including the highest-income payment method records.

    Returns:
        A formatted string containing all payment methods tied for the 
        highest generated income.
    """
    list_highest_income_payment_method = analysis_result["highest_income_payment_method"]
    summry = []
    summry.append("HIGHEST INCOME PAYMENT METHOD")
    for highest_income_pyment_method in list_highest_income_payment_method:
        summry_paymet_method = f"""
{highest_income_pyment_method["metodo_pago"]}
Income: ${highest_income_pyment_method["ingreso_total"]:,.2f}
Units sold: {highest_income_pyment_method["unidades_vendidas"]}"""
        summry.append(summry_paymet_method)
    return "\n".join(summry)


def get_top_5_best_selling_products(analysis_result: Dict[str, Any]) -> str:
    """Generate the Top 5 best-selling products section.

    Reads the ranked records stored in `top_5_best_selling_products` and
    formats each product with its ranking position, identifier, name, 
    units sold, and total income.

    The section contains up to five products.

    Args:
        analysis_result: Dictionary conatining the sales analysis results,
            including the Top 5 best-selling products.

    Returns:
        A formatted string containing the Top 5 best-selling products.
    """
    top_5_best_selling_products = analysis_result["top_5_best_selling_products"]
    summary = []
    summary.append("TOP 5 BEST SELLING PRODUCTS\n")
    for index in range(len(top_5_best_selling_products)):
        top_5 = top_5_best_selling_products[index]
        summary_top_5 = f"""
{index + 1}. {top_5["producto_id"]} - {top_5["producto"]} | Units sold: {top_5["unidades_vendidas"]} | Income: ${top_5["ingreso_total"]:,.2f}""".strip()
        summary.append(summary_top_5)
    summary = "\n".join(summary)
    return "\n" + summary.strip()

def get_top_5_highest_income_products(analysis_result: Dict[str, Any]) -> str:
    """Generate the Top 5 highest-income products section.

    Read the ranked records stored in `top_5_highest_income_products` and
    formats each product with its ranking position, identifier, name,
    total income, and units sold.

    The section contains up to five products.

    Args:
        analysis_result: Dictionary containing the sales analysis results,
            including the Top 5 highest-income products.

    Returns:
        A formatted string containing the Top 5 highest-income products.
    """
    top_5_highest_income_products = analysis_result["top_5_highest_income_products"]
    summary = []
    summary.append("TOP 5 HIGHEST INCOME PRODUCTS\n")
    for index in range(len(top_5_highest_income_products)):
        top_5 = top_5_highest_income_products[index]
        summary_top_5 = f"""
{index + 1}. {top_5["producto_id"]} - {top_5["producto"]} | Income: ${top_5["ingreso_total"]:,.2f} | Units sold: {top_5["unidades_vendidas"]}
""".strip()
        summary.append(summary_top_5)
    summary = "\n".join(summary)
    return "\n" + summary.strip() + "\n"

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
    product_summary_for_display = analysis_result["product_summary"].copy()
    product_summary_for_display["ingreso_total"] = product_summary_for_display["ingreso_total"].map(lambda x: f"${x:,.2f}")
    summary = []
    summary.append("PRODUCT SUMMARY")
    summary.append(f"\n{product_summary_for_display.to_string(index=False)}\n")
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
    category_summary_for_display = analysis_result["category_summary"].copy()
    category_summary_for_display["ingreso_total"] = category_summary_for_display["ingreso_total"].map(lambda x: f"${x:,.2f}")
    summary = []
    summary.append("CATEGORY SUMMARY")
    summary.append(f"\n{category_summary_for_display.to_string(index=False)}\n")
    return "\n".join(summary)

def get_city_summary(analysis_result: Dict[str, Any]) -> str:
    """Generate the city summary section.

    Creates a display copy of the city summary DataFrame and formats the
    `ingreso_total` column as currency before converting the data into a
    plain-text table without the pandas index.

    Args:
        analysis_result: Dictionary containing the `city_summary`
            DataFrame produced by the sales analysis process.

    Returns:
        A formatted string containing the aggregated city summary.
    """
    city_summary_for_display = analysis_result["city_summary"].copy()
    city_summary_for_display["ingreso_total"] = city_summary_for_display["ingreso_total"].map(lambda x: f"${x:,.2f}")
    summary = []
    summary.append("CITY SUMMARY")
    summary.append(f"\n{city_summary_for_display.to_string(index=False)}\n")
    return "\n".join(summary)

def get_payment_method_summary(analysis_result: Dict[str, Any]) -> str:
    """Generate the payment method summary section.

    Creates a display copy of the payment method summary DataFrame and formats 
    the `ingreso_total` column as currency before converting the data into a
    plain-text table without the pandas index.

    Args:
        analysis_result: Dictionary containing the `payment_method_summary`
            DataFrame produced by the sales analysis process.

    Returns:
        A formatted string containing the aggregated payment method summary.
    """
    payment_method_summary_for_display = analysis_result["payment_method_summary"].copy()
    payment_method_summary_for_display["ingreso_total"] = payment_method_summary_for_display["ingreso_total"].map(lambda x: f"${x:,.2f}")
    summary = []
    summary.append("PAYMENT METHOD SUMMARY")
    summary.append(f"\n{payment_method_summary_for_display.to_string(index=False)}\n")
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
    metrics, highest-perfoming records, Top 5 product rankings, product
    and category summaries, optional city and pyment method summaries,
    validation errors, and warnings.

    When city analysis is available, the report also includes the
    highest-income city and the complete city summary.

    When payment method analysis is available, the report also includes the 
    highest-income payment method and the complete payment method summary.

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
    if "highest_income_city" in analysis_result.keys():
        summary.append(get_highest_income_city(analysis_result))
    if "highest_income_payment_method" in analysis_result.keys():
        summary.append(get_highest_income_payment_method(analysis_result))
    summary.append(get_top_5_best_selling_products(analysis_result))
    summary.append(get_top_5_highest_income_products(analysis_result))
    summary.append(get_product_summary(analysis_result))
    summary.append(get_category_summary(analysis_result))
    if "city_summary" in analysis_result.keys():
        summary.append(get_city_summary(analysis_result))
    if "payment_method_summary" in analysis_result.keys():
        summary.append(get_payment_method_summary(analysis_result))
    summary.append(get_errors(errors))
    summary.append(get_warnings(warnings))
    return "\n".join(summary)