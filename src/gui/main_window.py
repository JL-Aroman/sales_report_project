"""Sales Report graphical user interface module.

This module provides the main desktop window for the Sales Report application
using PySide6.

It builds the graphical interface for selecting a source CSV file, choosing
an output directory, generating sales reports through the backend controller,
displaying the current application status, and presenting the paths of the
generated output files.

The interface is organized into independent layout-building methods to keep
the window structure modular, maintainable, and easy to extend.

The module integrates the graphical interface with the Sales Report controller
and handles application-specific and unexpected errors during report
generation.
"""

from src import controller as control
from src.errors import AppError

from PySide6.QtWidgets import(
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFileDialog,
    QScrollArea
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
        txt_file_label: Label reserved for the generated TXT report path.
        json_file_label: Label reserved for the generated JSON report path.
        csv_title_label: Label identifying the generated CSV summaries section.
        csv_summaries_layout: Layout containing dynamically generated labels
            for CSV summary file paths.
        button_create_report: Button used to start the report-generation
            workflow.
    """
    def __init__(self) -> None:
        """Initialize the main Sales Report application window.

        Sets the initial application state, defines the default output directory,
        configures the window title and fixes size, creates the central widget,
        and builds the main vertical layout.

        The interface sections are created through independent layout-building
        methods and added to the main window.
        """
        super().__init__()
        self.file_path = None
        self.output_folder = "reports/"

        self.setWindowTitle("Generador de Reportes de Ventas")
        self.setFixedSize(900,700)

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
        self.output_folder_label = QLabel(f"Carpeta no seleccionada. Se usará: {self.output_folder}")
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
        """Build the generated-files display section.

        Creates a group box containing labels for the generated TXT report and
        JSON analysis file, together with a scrollable area for dynamically
        displaying CSV summary file paths.

        The CSV paths are added to `csv_summaries_layout` after a successful
        report-generation process.

        Returns:
            A QGroupBox containing the generated-file display controls.
        """
        group = QGroupBox("Archivos Generados")
        layout = QVBoxLayout()
        self.txt_file_label = QLabel("- TXT:")
        self.json_file_label = QLabel("- JSON:")
        self.csv_title_label = QLabel("- Resúmenes CSV:")
        layout.addWidget(self.txt_file_label)
        layout.addWidget(self.json_file_label)
        layout.addWidget(self.csv_title_label)
        csv_container = QWidget()
        self.csv_summaries_layout = QVBoxLayout()
        csv_container.setLayout(self.csv_summaries_layout)
        scroll = QScrollArea()
        scroll.setWidget(csv_container)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(200)
        layout.addWidget(scroll)
        group.setLayout(layout)
        return group

    def selected_file_path(self) -> None:
        """Open a dialog for selecting the source CSV file.

        Displays a file-selection dialog restricted to files with the `.csv`
        extension.

        When a file is selected, its path is stored in `file_path` and displayed
        in the interface. The status message is also updated according to whether
        the default or a custom output folder is currently configured.

        If the dialog is canceled, the current application state remains unchanged.
        """
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos CSV (*.csv)")
        if file:
            self.file_path = file
            self.selected_file_label.setText(self.file_path)
            if self.output_folder == "reports/":
                self.status_label.setText(f"Archivo seleccionado correctamente, carpeta predefinida: {self.output_folder}")
            else:
                self.status_label.setText(f"Archivo y carpeta seleccionados correctamente.")
       

    def selected_folder_path(self) -> None:
        """Open a dialog for selecting the output directory.

        Displays a directory-selection dialog that allows the user to choose where
        generated report files will be stored.

        When a folder is selected, the `output_folder` attribute and its associated
        label are updated. The status message is also changed according to whether
        a source CSV file has already been selected.

        If the dialog is canceled, the current output directory remains unchanged.
        """
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida.")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(self.output_folder)
            if self.file_path is not None:
                self.status_label.setText(f"Archivo y carpeta seleccionados correctamente.")
            else:
                self.status_label.setText(f"Carpeta seleccionada correctamente... Esperando archivo CSV.")

    def generate_reports(self) -> None:
        """Generate sales reports using the configured file and output folder.

        Verifies that a source CSV file has been selected before starting the
        report-generation workflow.

        When a file is available, the method clears previously displayed CSV
        results and calls `controller.generate_sales_report()` using the selected
        CSV path and output directory.

        The generated TXT and JSON paths are displayed in their corresponding
        labels. CSV summary paths are dynamically added to the scrollable CSV
        results layout.

        The application status is updated according to the result of the operation.
        Application-specific errors derived from `AppError` and unexpected
        exceptions are displayed through the status label.

        Returns:
            None.
        """
        self.status_label.setText("Proceso iniciado...")
        if self.file_path is None:
            self.status_label.setText("Seleccione un archivo CSV antes de generar el reporte.")
            return
        else:
            try:
                self.txt_file_label.setText("- TXT:")
                self.json_file_label.setText("- JSON:")
                self.clean_layout(self.csv_summaries_layout)
                data_analysis = control.generate_sales_report(self.file_path, self.output_folder)
                self.txt_file_label.setText(f"- TXT: {str(data_analysis['report_path_txt'])}")
                self.json_file_label.setText(f"- JSON: {str(data_analysis['report_path_json'])}")
                for path, name_path in data_analysis["reports_path_csv"].items():
                    path_label = QLabel(f"{path}: {str(name_path)}")
                    self.csv_summaries_layout.addWidget(path_label)
                self.status_label.setText("Reporte generado correctamente")
            except AppError as error:
                self.status_label.setText(str(error))
            except Exception as error:
                self.status_label.setText(str(error))

    def clean_layout(self, layout) -> None:
        """Remove all widgets from a layout.

        Iterates through the layout in reverse order and schedules each contained
        widget for deletion.

        This method is used before displaying new CSV summary paths so that results
        from a previous report generation are removed from the interface.

        Args:
            layout: Qt layout containing widgets to remove.

        Returns:
            None.
        """
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()