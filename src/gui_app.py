"""Graphical application entry point for the Sales Report project.

This module initializes the PySide6 application environment and launches
the main Sales Report desktop window.

It creates the QApplication instance, initializes the
`SalesReportWindow`, displays the window, starts the Qt event loop, and
returns the application exit status to the operating system.

The graphical interface implementation is provided by the `gui.main_windows`
module.
"""

import sys

from PySide6.QtWidgets import QApplication
from src.gui import main_window

app = QApplication(sys.argv)
m = main_window.SalesReportWindow()
m.show()
sys.exit(app.exec())