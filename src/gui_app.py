"""Graphical application entry point for the Sales Report project.

This module initializes the PySide6 application environment and launches
the main Sales Report desktop window.

It creates the QApplication instance, initializes the
`SalesReportWindow`, displays the window, starts the Qt event loop, and
returns the application exit status to the operating system.

The graphical interface implementation is provided by the `src.gui.main_window`
module.
"""

import sys

from PySide6.QtWidgets import QApplication
from src.gui import main_window

def main() -> None:
    """Initialize and run the Sales Report graphical application.

    Creates the PySide6 `QApplication` instance, initializes the main
    `SalesReportWindow`, displays the window, and starts the Qt event loop.

    When the graphical application closes, the Qt exit status is passed
    to `sys.exit()` and returned to the operating system.

    Returns:
        None.
    """
    app = QApplication(sys.argv)
    window = main_window.SalesReportWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()