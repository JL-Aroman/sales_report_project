"""Sales Report graphical user interface module.

This module provides the main desktop window for the Sales Report application
using PySide6.

It allows users to select a source CSV file and output directory, generate
sales reports through the backend controller, display generated file paths,
open TXT, JSON, and CSV reports in dedicated viewer windows, and open the
configured output directory using the operating system file manager.

The interface is organized into independent layout-building and event-handling
methods to keep the graphical layer modular, maintainable, and easy to extend.

Application-specific and unexpected errors produced during report generation
are presented to the user through status messages and critical message boxes.
"""

import os
import sys
import subprocess

from src import controller as control
from src.errors import AppError
from src.gui import file_viewer_window as fwindow

from PySide6.QtWidgets import(
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFileDialog,
    QScrollArea,
    QMessageBox,
    QHBoxLayout,
    QComboBox

)

class SalesReportWindow(QMainWindow):
    """Main desktop window for the Sales Report application.

    Provides the graphical interface used to select the source CSV file and
    output directory, initiate report generation, display application status,
    and present generated file information.

    The window is divided into independent group boxes for file selection,
    output-folder selection, report generation, status message, and generated
    files paths.

    Attributes:
        file_path: Path of the CSV file selected by the user, or `None` when
            no file has been selected.
        output_folder: Directory where generated reports will be stored.
            Defaults to `reports/`.
        selected_file_label: Label displaying the selected CSV file path.
        output_folder_label: Label displaying the selected output directory.
        status_label: Label displaying the current interface status.
        txt_file_label: Label identifying the generated TXT report section.
        txt_file_path_label: Label displaying the generated TXT report path.
        json_file_label: Label identifying the generated JSON analysis section.
        json_file_path_label: Label displaying the generated JSON file path.
        csv_title_label: Label identifying the generated CSV summaries section.
        csv_summaries_layout: Layout containing dynamically generated labels
            for CSV summary file paths.
        csv_combobox: Combo box used to select a generated CSV summary.
        button_create_report: Button used to start report generation.
        button_txt_show_report: Button used to open the TXT report viewer.
        button_json_show_report: Button used to open the JSON report viewer.
        button_csv_show_report: Button used to open the selected CSV report.
        button_open_output_folder: Button used to open the configured output
            directory.
        txt_path: Path of the most recently generated TXT report, or `None`
            when no report is available.
        json_path: Path of the most recently generated JSON file, or `None`
            when no report is available.
        csv_paths: Dictionary mapping CSV summary names to their generated
            file paths.
    """
    def __init__(self) -> None:
        """Initialize the main Sales Report application window.

        Sets the initial source-file and output-folder state, initializes storage for
        generated TXT, JSON, and CSV paths, configures the window title and fixed
        size, creates the central widget, and builds the main vertical layout.

        The interface sections are created through independent layout-building
        methods and added to the main window.
        """
        super().__init__()
        self.file_path = None
        self.output_folder = "reports/"
        self.txt_path = None
        self.json_path = None
        self.csv_paths = {}

        self.setWindowTitle("Generador de Reportes de Ventas")
        self.setFixedSize(900,800)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        main_layout = QVBoxLayout()

        main_layout.addWidget(self.build_selected_file_layout())
        main_layout.addWidget(self.build_selected_folder_layout())
        main_layout.addWidget(self.build_generate_report_layout())
        main_layout.addWidget(self.build_status_layout())
        main_layout.addWidget(self.build_generated_files_layout())

        widget_central.setLayout(main_layout)

    def build_selected_file_layout(self) -> QGroupBox:
        """Build the source CSV file selection section.

        Creates a group box containing a label that displays the selected file
        path and button that opens the CSV file selection dialog.

        The selection button is connected to `selected_file_path()`

        Returns:
            A QGroupBox containing the source-file selection controls.
        """
        group = QGroupBox("Archivo CSV de Origen")
        layout = QVBoxLayout()
        self.selected_file_label = QLabel("Archivo no seleccionado.")
        self.button_selected_file = QPushButton("Seleccionar archivo")
        self.button_selected_file.setFixedSize(200,30)
        self.button_selected_file.clicked.connect(self.selected_file_path)
        layout.addWidget(self.selected_file_label)
        layout.addWidget(self.button_selected_file)
        group.setLayout(layout)
        return group

    def build_selected_folder_layout(self) -> QGroupBox:
        """Build the output-folder selection section.

        Creates a group box containing a label that displays the current output
        directory and a button that allows the user to select another folder.

        The default output directory is displayed when no custom folder has been
        selected. The selection button is connected to `selected_folder_path()`.    

        Returns:
            A QGroupBox containing the output-folder selection controls.
        """
        group = QGroupBox("Carpeta de Salida")
        layout = QVBoxLayout()
        self.output_folder_label = QLabel(f"Carpeta de salida: {self.output_folder}")
        self.button_output_folder = QPushButton("Seleccionar carpeta")
        self.button_output_folder.setFixedSize(200,30)
        self.button_output_folder.clicked.connect(self.selected_folder_path)
        layout.addWidget(self.output_folder_label)
        layout.addWidget(self.button_output_folder)
        group.setLayout(layout)
        return group

    def build_generate_report_layout(self) -> QGroupBox:
        """Build the report generation section.

        Creates a group box containing the button used to start the report
        generation process.

        The button is connected to `generate_reports()`

        Returns:
            A QGroupBox containing the report generation button.
        """
        group = QGroupBox("Crear Reporte")
        layout = QVBoxLayout()
        self.button_create_report = QPushButton("Crear reporte")
        self.button_create_report.clicked.connect(self.generate_reports)
        layout.addWidget(self.button_create_report)
        group.setLayout(layout)
        return group

    def build_status_layout(self) -> QGroupBox:
        """Build the application status section.

        Creates a group box containing a label used to display status messages
        during file selection, folder selection, and report generation.

        The initial message instructs the user to select a CSV file.

        Returns:
            A QGroupBox containing the application status label.
        """
        group = QGroupBox("Estado")
        layout = QVBoxLayout()
        self.status_label = QLabel("Seleccione un archivo CSV para comenzar.")
        layout.addWidget(self.status_label)
        group.setLayout(layout)
        return group

    def build_generated_files_layout(self) -> QGroupBox:
        """Build the generated-files display and navigation section.

        Creates a group box containing dedicated labels for TXT and JSON file paths,
        buttons for opening those reports, a combo box for selecting generated CSV
        summaries, a button for opening the selected CSV report, and a scrollable
        area displaying all generated CSV paths.

        Report-viewing controls are initially disabled and become available after a
        successful report-generation process.

        The section also provides a button for opening the configured output
        directory in the operating system file manager.

        Returns:
            A QGroupBox containing the generated-file display and navigation controls.
        """
        group = QGroupBox("Archivos Generados")
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.txt_file_label = QLabel("- TXT:")
        self.txt_file_path_label = QLabel("")
        self.button_txt_show_report = QPushButton("Reporte TXT")
        self.button_txt_show_report.setFixedSize(200,30)
        self.button_txt_show_report.clicked.connect(self.open_report_txt)
        self.json_file_label = QLabel("- JSON:")
        self.json_file_path_label = QLabel("")
        self.button_json_show_report = QPushButton("Análisis JSON")
        self.button_json_show_report.setFixedSize(200,30)
        self.button_json_show_report.clicked.connect(self.open_report_json)
        self.csv_title_label = QLabel("- Resúmenes CSV:")
        self.csv_combobox = QComboBox()
        self.button_csv_show_report = QPushButton("Ver resumen CSV")
        self.button_csv_show_report.clicked.connect(self.open_report_csv)
        self.button_open_output_folder = QPushButton("Abrir carpeta de salida")
        self.button_open_output_folder.clicked.connect(self.open_output_folder)
        self.off_buttons()
        layout.addWidget(self.txt_file_label)
        layout.addWidget(self.txt_file_path_label)
        layout.addWidget(self.button_txt_show_report)
        layout.addWidget(self.json_file_label)
        layout.addWidget(self.json_file_path_label)
        layout.addWidget(self.button_json_show_report)
        layout.addWidget(self.csv_title_label)
        button_layout.addWidget(self.csv_combobox)
        button_layout.addWidget(self.button_csv_show_report)
        layout.addLayout(button_layout)
        csv_container = QWidget()
        self.csv_summaries_layout = QVBoxLayout()
        csv_container.setLayout(self.csv_summaries_layout)
        scroll = QScrollArea()
        scroll.setWidget(csv_container)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(150)
        layout.addWidget(scroll)
        layout.addWidget(self.button_open_output_folder)
        group.setLayout(layout)
        return group

    def selected_file_path(self) -> None:
        """Open a dialog for selecting the source CSV file.

        Displays a file-selection dialog restricted to files with the `.csv`
        extension.

        When a new file is selected, previously generated report references and
        displayed results are cleared. Report-viewing controls and the CSV selector
        are disabled until a new report-generation process completes successfully.

        The selected path is stored in `file_path`, displayed in the interface,
        and the application status is updated according to the currently configured
        output folder.

        If the dialog is canceled, the current application state remains unchanged.

        Returns:
            None.
        """
        
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if file:
            self.off_buttons()
            self.clean_labels()
            self.clean_paths()
            self.file_path = file
            self.selected_file_label.setText(self.file_path)
            if self.output_folder == "reports/":
                self.status_label.setText(f"Archivo seleccionado correctamente, carpeta predefinida: {self.output_folder}")       
            else:
                self.status_label.setText(f"Archivo y carpeta seleccionados correctamente")

    def selected_folder_path(self) -> None:
        """Open a dialog for selecting the output directory.

        Displays a directory-selection dialog that allows the user to choose where
        generated report files will be stored.

        When a new folder is selected, previously generated report references and
        displayed results are cleared. Report-viewing controls and the CSV selector
        are disabled until a new report-generation process completes successfully.

        The selected directory is stored in `output_folder`, displayed in the
        interface, and the application status is updated according to whether a
        source CSV file has already been selected.

        If the dialog is canceled, the current application state remains unchanged.

        Returns:
            None.
        """
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida.")
        if folder:
            self.off_buttons()
            self.clean_paths()
            self.clean_labels()
            self.output_folder = folder
            self.output_folder_label.setText(self.output_folder)
            if self.file_path is not None:
                self.status_label.setText(f"Archivo y carpeta seleccionados correctamente.")
            else:
                self.status_label.setText(f"Carpeta seleccionada correctamente... Esperando archivo CSV.")
                

    def generate_reports(self) -> None:
        """Generate sales reports using the selected file and output folder.

        Temporarily disables the report-generation button and verifies that a source
        CSV file has been selected.

        Before starting a new generation process, previously stored TXT, JSON, and
        CSV paths are reset. Previously displayed file paths, CSV selector entries,
        and dynamically generated CSV labels are also cleared from the interface. 
        The method then delegates the complete backend workflow to 
        `controller.generate_sales_report()`.

        After a successful operation, the generated TXT and JSON paths are stored
        and displayed, CSV summary paths are added to the scrollable layout and CSV
        selector, and the report-viewing and output-folder controls are enabled.

        If an application-specific or unexpected error occurs, the status label is
        updated and a critical message box displays the corresponding error message.

        Returns:
            None.
        """
        self.button_create_report.setEnabled(False)
        self.status_label.setText("Proceso iniciado...")
        if self.file_path is None:
            self.status_label.setText("Seleccione un archivo CSV antes de generar el reporte.")
            self.button_create_report.setEnabled(True)
            return
        else:
            try:
                self.off_buttons()
                self.clean_paths()
                self.clean_labels()
                data_analysis = control.generate_sales_report(self.file_path, self.output_folder)
                self.txt_file_path_label.setText(str(data_analysis['report_path_txt']))
                self.txt_path = str(data_analysis['report_path_txt'])
                self.json_file_path_label.setText(str(data_analysis['report_path_json']))
                self.json_path = str(data_analysis["report_path_json"])
                for path, name_path in data_analysis["reports_path_csv"].items():
                    self.csv_combobox.addItem(path)
                    path_label = QLabel(f"{path}: {str(name_path)}")
                    self.csv_summaries_layout.addWidget(path_label)
                    self.csv_paths[path] = name_path
                self.status_label.setText("Archivos guardados en la carpeta seleccionada.")
                self.on_buttons()
            except AppError as error:
                self.status_label.setText("Error en el proceso")
                QMessageBox.critical(self, "Error", str(error))
            except Exception as error:
                self.status_label.setText("Error en el proceso")
                QMessageBox.critical(self, "Error", str(error))
        self.button_create_report.setEnabled(True)

    def clean_layout(self, layout) -> None:
        """Remove all widgets currently contained in a layout.

        Iterates through the layout in reverse order and schedules each contained
        widget for deletion.

        This method is used before displaying new CSV summary paths so that results
        from a previous report-generation process are removed from the interface.

        Args:
            layout: Qt layout containing the widgets to remove.

        Returns:
            None.
        """
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def open_output_folder(self) -> None:
        """Open the configured output directory in the system file manager.

        Converts the configured output folder into an absolute path and opens it
        using the platform-specific operating system command.

        Windows uses `os.startfile()`, macOS uses the `open` command, and other
        platforms use `xdg-open`.

        Returns:
            None.
        """
        open_folder = os.path.abspath(self.output_folder)
        if sys.platform == "win32":
            os.startfile(open_folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", open_folder])
        else:
            subprocess.Popen(["xdg-open", open_folder])

    def open_report_txt(self) -> None:
        """Open the generated TXT report in a file viewer window.

        Creates a `FileViewerWindow` using the path stored in `txt_path`, keeps a
        reference to the viewer window, and displays it.

        Returns:
            None.
        """
        self.txt_window = fwindow.FileViewerWindow("Reporte TXT", self.txt_path)
        self.txt_window.show()

    def open_report_json(self) -> None:
        """Open the generated JSON analysis file in a file viewer window.

        Creates a `FileViewerWindow` using the path stored in `json_path`, keeps a
        reference to the viewer window, and displays it.

        Returns:
            None.
        """
        self.json_window = fwindow.FileViewerWindow("Análisis JSON", self.json_path)
        self.json_window.show()

    def open_report_csv(self) -> None:
        """Open the selected CSV summary in a file viewer window.

        Reads the currently selected summary name from `csv_combobox`, retrieves its
        corresponding file path from `csv_paths`, creates a `FileViewerWindow`, and
        displays the selected CSV report.

        Returns:
            None.
        """
        csv_selected = self.csv_combobox.currentText()
        self.csv_window = fwindow.FileViewerWindow(f"Reporte CSV: {csv_selected}", self.csv_paths[csv_selected])
        self.csv_window.show()

    def on_buttons(self) -> None:
        """Enable controls associated with generated report results.

        Enables the output-folder button, TXT and JSON report viewer buttons,
        CSV summary selector, and CSV report viewer button.

        This method is called after a successful report-generation process so
        the user can access the newly generated files.

        Returns:
            None.
        """
        self.button_open_output_folder.setEnabled(True)
        self.button_txt_show_report.setEnabled(True)
        self.button_json_show_report.setEnabled(True)
        self.csv_combobox.setEnabled(True)
        self.button_csv_show_report.setEnabled(True)

    def off_buttons(self) -> None:
        """Disable controls associated with generated report results.

        Disables the output-folder button, TXT and JSON report viewer buttons,
        CSV report viewer button, and CSV summary selector.

        This method is used when previously generated results are no longer
        considered valid or while a new report-generation process is prepared.

        Returns:
            None.
        """
        self.button_open_output_folder.setEnabled(False)
        self.button_txt_show_report.setEnabled(False)
        self.button_json_show_report.setEnabled(False)
        self.button_csv_show_report.setEnabled(False)
        self.csv_combobox.setEnabled(False)

    def clean_labels(self) -> None:
        """Clear generated report information displayed in the interface.

        Removes the displayed TXT and JSON file paths, clears all entries from
        the CSV summary selector, and removes dynamically generated CSV path
        labels from the CSV summaries layout.

        This method is used before displaying the results of a new report
        generation or after changing the selected source file or output folder.

        Returns:
            None.
        """
        self.txt_file_path_label.setText("")
        self.json_file_path_label.setText("")
        self.csv_combobox.clear()
        self.clean_layout(self.csv_summaries_layout)

    def clean_paths(self) -> None:
        """Reset stored paths for previously generated report files.

        Resets the TXT and JSON report paths to `None` and replaces the stored
        CSV path mapping with an empty dictionary.

        This prevents previously generated files from remaining associated with
        the interface after changing the input configuration or starting a new
        report-generation process.

        Returns:
            None.
        """
        self.txt_path = None
        self.json_path = None
        self.csv_paths = {}