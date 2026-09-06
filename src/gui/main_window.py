"""Sales Report graphical user interface module.

This module provides the main desktop window for the Sales Report application 
using PySide6.

It builds the graphical interface for seleting a source CSV file, choosing 
an output directory, starting the report generation process, displaying the 
current application status, and presenting the paths of generated ouput
files.

The interface is organized into independent layout-building methods to keep
the window structure modula, maintainable, and easy to extend.

The report generation button is currently prepared in the interface but is
not yet connected to the backend repporting workflow.
"""

from PySide6.QtWidgets import(
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFileDialog
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
        csv_file_label: Label reserved for generated CSV summary paths
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
        self.setFixedSize(700,500)

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
            A QGroupBox containing the source-file selecton controls.
        """
        group = QGroupBox("Archivo CSV de Origen")
        layout = QVBoxLayout()
        self.selected_file_label = QLabel("Archivo no seleccionado.")
        self.button_selected_file = QPushButton("Seleccionar Archivo")
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
            A QGroupBox contianing the output-folder selection controls.
        """
        group = QGroupBox("Carpeta de Salida")
        layout = QVBoxLayout()
        self.output_folder_label = QLabel(f"Carpeta no seleccionada. Se usará: {self.output_folder}")
        self.button_output_folder = QPushButton("Seleccionar Carpeta")
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
        self.button_create_report = QPushButton("Crear Reporte")
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

        Creates a group box containing labels reserved for displaying the paths
        of the generated TXT report, JSON analysis file, and CSV summary files.

        Returns:
            A QGroupBox containing the generated-file labels.
        """
        group = QGroupBox("Archivos Generados")
        layout = QVBoxLayout()
        self.txt_file_label = QLabel("- TXT:")
        self.json_file_label = QLabel("- JSON:")
        self.csv_summaries_label = QLabel("- Resúmenes CSV:")
        layout.addWidget(self.txt_file_label)
        layout.addWidget(self.json_file_label)
        layout.addWidget(self.csv_summaries_label)
        group.setLayout(layout)
        return group

    def selected_file_path(self) -> None:
        """Open a dialog for selecting the source CSV file.

        Displays a file-selection dialog restricted to files whit the `.csv`
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
                self.status_label.setText(f"Archivo y Carpeta seleccionados correctamente.")
            else:
                self.status_label.setText(f"Carpeta seleccionada correctamente... Esperando archivo CSV.")

    def generate_reports(self) -> None:
        """Handle the report generation button action.

        Uppdates the application status to indicate that the report-generation
        button has not yet been connected to the backend reporting workflow.

        This method is currently a placeholder for the future integration whit
        the Sales Report controller.
        """
        self.status_label.setText("Falta conectar este botón.")