"""Sales chart generation and management module.

This module converts structured sales-analysis results into PNG chart images
using pandas and Matplotlib.

It provides a reusable chart-building helper and coordinates the generation
of multiple charts representing monthly sales performance, growth metrics,
product rankings, category results, and optional city and payment-method
analyses.

Generated charts are stored in the configured output directory using the
shared report base filename so that they remain associated with the report
files produced during the same workflow.

Chart-generation and supported file-system errors are converted into the
application-specific `ChartGenerationError` exception.

The main `save_chart_images()` function coordinates chart generation and
returns a dictionary mapping chart identifiers to generated PNG paths.
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from src.errors import ChartGenerationError
from typing import Dict, Any

def build_graph_image(
        df: pd.DataFrame, 
        x_str: str, 
        y_str: str,
        xlabel_str: str,
        ylabel_str: str, 
        title_str: str, 
        output_folder: str | Path, 
        file_name: str
        ) -> Path:
    """Generate and save a bar-chart image from a pandas DataFrame.

    Creates the destination directory when necessary and generates a bar
    chart using the specified DataFrame columns.

    The chart is configured with custom axis labels and a title. X-axis labels
    are rotated 90 degrees to improve readability, and `tight_layout()` is
    applied before saving the image.

    The generated chart is saved as a PNG file with a resolution of 150 DPI.
    The active Matplotlib figure is closed after the operation regardless of
    whether chart generation succeeds or fails.

    Args:
        df: DataFrame containing the data used to generate the chart.
        x_str: Name of the DataFrame column used for the x-axis.
        y_str: Name of the DataFrame column used for the y-axis.
        xlabel_str: Label displayed on the x-axis.
        ylabel_str: Label displayed on the y-axis.
        title_str: Title displayed at the top of the chart.
        output_folder: Directory where the PNG image will be stored.
        file_name: Output filename without the `.png` extension.

    Returns:
        Path to the generated PNG chart image.

    Raises:
        ChartGenerationError: If the output directory or chart image cannot
            be created, required DataFrame columns are unavailable, or invalid
            plotting data is provided.
    """
    output_filename = f"{file_name}.png"
    try:
        folder = Path(output_folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / output_filename
        df.plot(x=x_str, y=y_str, kind="bar", legend=False, title=title_str, color="#4472C4")
        plt.xlabel(xlabel_str)
        plt.ylabel(ylabel_str)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(path, dpi=150)
    except (OSError, KeyError, ValueError, TypeError) as error:
        raise ChartGenerationError() from error
    finally:
        plt.close()
    return path

def save_chart_images(analysis_result: Dict[str, Any], output_folder: str | Path, file_name_base: str) -> Dict[str, Path]:
    """Generate all supported sales-analysis chart images.

    Coordinates chart generation using the structured results produced by the
    sales-analysis module.

    Top 5 product rankings stored as lists of dictionaries are converted into
    pandas DataFrames before chart generation.

    Monthly product and category analyses are copied and extended with
    combined display columns so month and entity information can be shown
    together on chart x-axes.

    The function always generates charts for:

    - Monthly total income.
    - Monthly units sold.
    - Monthly income percentage variation.
    - Monthly unit-sales percentage variation.
    - Monthly best-selling products.
    - Monthly highest-income categories.
    - Top 5 highest-income products.
    - Top 5 best-selling products.
    - Income by category.
    - Units sold by category.

    When city analysis is available and contains data, it also generates:

    - Income by city.
    - Units sold by city.

    When payment-method analysis is available and contains data, it also
    generates:

    - Income by payment method.
    - Units sold by payment method.

    Every chart is saved as a PNG image through `build_graph_image()` using
    the shared report base filename and a descriptive suffix.

    Args:
        analysis_result: Dictionary containing the complete structured
            sales-analysis result.
        output_folder: Directory where generated PNG files will be stored.
        file_name_base: Shared base filename used to identify chart files
            belonging to the same report-generation workflow.

    Returns:
        A dictionary mapping chart identifiers to generated PNG file paths.

        The dictionary always contains:

        - `grafica_de_ingresos_mensuales`
        - `grafica_de_unidades_vendidas_mensualmente`
        - `grafica_crecimiento_porcentaje_mensual`
        - `grafica_crecimiento_porcentaje_unidades`
        - `grafica_producto_top_mensual`
        - `grafica_categoria_top_ingreso`
        - `grafica_producto_top_ingreso`
        - `grafica_unidades_producto_top`
        - `grafica_ingreso_categoria`
        - `grafica_unidades_categoria`

        When city information is available, it may also contain:

        - `grafica_ingreso_ciudad`
        - `grafica_unidades_ciudad`

        When payment-method information is available, it may also contain:

        - `grafica_ingreso_metodo_pago`
        - `grafica_unidades_metodo_pago`
    """
    top_5_best_selling_products = pd.DataFrame(analysis_result["top_5_best_selling_products"])
    top_5_highest_income_products = pd.DataFrame(analysis_result["top_5_highest_income_products"])
    save_paths = {}
    save_paths["grafica_de_ingresos_mensuales"] = build_graph_image(
        analysis_result["monthly_summary"],
        "mes",
        "ingreso_total",
        "Mes",
        "Ingreso total",
        "Ingreso mensual",
        output_folder,
        f"{file_name_base}_ingreso_por_mes"
    )
    save_paths["grafica_de_unidades_vendidas_mensualmente"] = build_graph_image(
        analysis_result["monthly_summary"],
        "mes",
        "unidades_vendidas",
        "Mes",
        "Unidades vendidas",
        "Unidades vendidas por mes",
        output_folder,
        f"{file_name_base}_unidades_vendidas_por_mes"
    )
    save_paths["grafica_crecimiento_porcentaje_mensual"] = build_graph_image(
        analysis_result["monthly_summary"],
        "mes",
        "crecimiento_ingreso_porcentaje",
        "Mes",
        "Variación de ingreso (%)",
        "Variación porcentual de ingreso por mes",
        output_folder,
        f"{file_name_base}_crecimiento_porcentaje_por_mes"
    )
    save_paths["grafica_crecimiento_porcentaje_unidades"] = build_graph_image(
        analysis_result["monthly_summary"],
        "mes",
        "crecimiento_unidades_porcentaje",
        "Mes",
        "Variación de unidades (%)",
        "Variación porcentual de unidades por mes",
        output_folder,
        f"{file_name_base}_crecimiento_porcentaje_unidades"
    )
    df_copy_best_product_by_month = analysis_result["monthly_best_selling_product"].copy()
    df_copy_best_product_by_month["mes_producto"] = df_copy_best_product_by_month["mes"].astype(str) + " - " + df_copy_best_product_by_month["producto"].astype(str)
    save_paths["grafica_producto_top_mensual"] = build_graph_image(
        df_copy_best_product_by_month,
        "mes_producto",
        "unidades_vendidas",
        "Mes y Producto",
        "Unidades vendidas",
        "Unidades del producto más Vendido por mes",
        output_folder,
        f"{file_name_base}_producto_top_mensual"
    )
    df_copy_monthly_highest_income_category = analysis_result["monthly_highest_income_category"].copy()
    df_copy_monthly_highest_income_category["mes_categoria"] = df_copy_monthly_highest_income_category["mes"].astype(str) + " - " + df_copy_monthly_highest_income_category["categoria"].astype(str)
    save_paths["grafica_categoria_top_ingreso"] = build_graph_image(
        df_copy_monthly_highest_income_category,
        "mes_categoria",
        "ingreso_total",
        "Mes y Categoría",
        "Ingreso total",
        "Categoría con mejor ingreso por mes",
        output_folder,
        f"{file_name_base}_categoria_top_ingreso_mensual"
    )
    save_paths["grafica_producto_top_ingreso"] = build_graph_image(
        top_5_highest_income_products,
        "producto",
        "ingreso_total",
        "Producto",
        "Ingreso total",
        "Top 5 productos por ingreso",
        output_folder,
        f"{file_name_base}_ingreso_producto_top"
    )
    save_paths["grafica_unidades_producto_top"] = build_graph_image(
        top_5_best_selling_products,
        "producto",
        "unidades_vendidas",
        "Producto",
        "Unidades vendidas",
        "Top 5 productos por unidades vendidas",
        output_folder,
        f"{file_name_base}_unidades_producto_top"
    )
    save_paths["grafica_ingreso_categoria"] = build_graph_image(
        analysis_result["category_summary"],
        "categoria",
        "ingreso_total",
        "Categoría",
        "Ingreso total",
        "Ingreso por categoría",
        output_folder,
        f"{file_name_base}_ingreso_categoria"
    )
    save_paths["grafica_unidades_categoria"] = build_graph_image(
        analysis_result["category_summary"],
        "categoria",
        "unidades_vendidas",
        "Categoría",
        "Unidades vendidas",
        "Ventas por categoría",
        output_folder,
        f"{file_name_base}_unidades_categoria"
    )
    if "city_summary" in analysis_result and analysis_result["city_summary"] is not None and not analysis_result["city_summary"].empty:
        save_paths["grafica_ingreso_ciudad"] = build_graph_image(
            analysis_result["city_summary"],
            "ciudad",
            "ingreso_total",
            "Ciudad",
            "Ingreso total",
            "Ingreso por ciudad",
            output_folder,
            f"{file_name_base}_ingreso_ciudad"
        )
        save_paths["grafica_unidades_ciudad"] = build_graph_image(
            analysis_result["city_summary"],
            "ciudad",
            "unidades_vendidas",
            "Ciudad",
            "Unidades vendidas",
            "Ventas por ciudad",
            output_folder,
            f"{file_name_base}_unidades_ciudad"
        )
    if "payment_method_summary" in analysis_result and analysis_result["payment_method_summary"] is not None and not analysis_result["payment_method_summary"].empty:
        save_paths["grafica_ingreso_metodo_pago"] = build_graph_image(
            analysis_result["payment_method_summary"],
            "metodo_pago",
            "ingreso_total",
            "Método de pago",
            "Ingreso total",
            "Ingreso por método de pago",
            output_folder,
            f"{file_name_base}_ingreso_metodo_pago"
            )
        save_paths["grafica_unidades_metodo_pago"] = build_graph_image(
            analysis_result["payment_method_summary"],
                "metodo_pago",
                "unidades_vendidas",
                "Método de pago",
                "Unidades vendidas",
                "Ventas por método de pago",
                output_folder,
                f"{file_name_base}_unidades_metodo_pago"
                )
    return save_paths
