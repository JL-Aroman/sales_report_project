"""Generated report file viewer module.

This module provides a dedicated PySide6 window for displaying the contents
of generated report files.

It receives a window title and file path, reads the target file using UTF-8
encoding, displays its contents inside a read-only text area, and provides
a button for closing the viewer window.

The viewer is used by the main graphical interface to display generated
TXT, JSON, and CSV report files without modifying their contents.
"""

from pathlib import Path
from PySide6.QtWidgets import(
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit, 
    QGroupBox,
    QPushButton
)

class FileViewerWindow(QMainWindow):
    """Window used to display the contents of a generated report file.

    Creates an independent read-only report viewer using PySide6. The file
    specified by `file_path` is loaded from the file system and displayed
    inside a QTextEdit widget.

    The window also provides a button that allows the user to close the
    report viewer.

    Attributes:
        title: Title displayed in the viewer window.
        file_path: Path of the report file whose contents will be displayed.
        button_close: Button used to close the viewer window.
    """
    def __init__(self, title: str, file_path: str) -> None:
        """Initialize the report file viewer window.

        Stores the window title and target file path, configures the fixed
        window size, creates the central widget, and builds the text-display
        and close-button areas.

        Args:
            title: Title to display in the viewer window.
            file_path: Path of the report file to read and display.
        """
        super().__init__()
        self.title = title
        self.file_path = file_path

        self.setWindowTitle(self.title)
        self.setFixedSize(700,900)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        main_layout = QVBoxLayout()

        main_layout.addWidget(self.build_text_area())
        main_layout.addLayout(self.build_button_area())

        widget_central.setLayout(main_layout)

    def build_text_area(self) -> QGroupBox:
        """Build the read-only report display area.

        Creates a group box containing a read-only QTextEdit widget. The target
        file specified by `file_path` is read using UTF-8 encoding and its
        complete contents are displayed as plain text.

        Returns:
            A QGroupBox containing the read-only report text area.
        """
        group = QGroupBox("Contenido del archivo")
        layout = QVBoxLayout()
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text = Path(self.file_path).read_text(encoding="utf-8")
        text_area.setPlainText(text)
        layout.addWidget(text_area)
        group.setLayout(layout)
        return group

    def build_button_area(self) -> QHBoxLayout:
        """Build the report viewer button area.

        Creates a horizontal layout containing the `Cerrar reporte` button.
        The button is connected directly to the window's `close()` method.

        Returns:
            A QHBoxLayout containing the report viewer close button.
        """
        layout = QHBoxLayout()
        self.button_close = QPushButton("Cerrar reporte")
        self.button_close.clicked.connect(self.close)
        layout.addWidget(self.button_close)
        return layout

