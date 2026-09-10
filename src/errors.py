"""Custom exception classes for the Sales Report project.

This module defines application-specific exceptions used across the
Sales Report application.

All custom exceptions inherit from `AppError`, providing a common exception
hierarchy that allows application-specific failures to be handled consistently.

Default error messages are written in Spanish because they are intended to
be displayed directly to users through the graphical interface.

The exceptions cover file validation, CSV structure, data validation,
sales analysis, report generation, and report file storage failures.
"""

class AppError(Exception):
    """Base exception class for all application-specific errors."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message


class EmptyPathError(AppError):
    """Raised when the provided file path is empty."""
    def __init__(self, message: str = "La ruta del archivo está vacía.") -> None:
        """
        Args:
            message: Descriptive message of the error. If 
                not specified, a generic message is used.
        """
        super().__init__(message)


class FileNotFoundAppError(AppError):
    """Raised when the provided file path does not exist."""
    def __init__(self, message: str = "La ruta del archivo no existe.") -> None:
        """
        Args:
            message: Descriptive message of the error. If 
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidFilePathError(AppError):
    """Raised when the provided path is not a valid file."""
    def __init__(self, message: str = "La ruta del archivo no corresponde a un archivo válido.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidFileExtensionError(AppError):
    """Raised when the file extension is not supported."""
    def __init__(self, message: str = "La extensión del archivo no es compatible.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyFileError(AppError):
    """Raised when the CSV file exists but has no content."""
    def __init__(self, message: str = "El archivo existe pero no tiene contenido.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class FileReadError(AppError):
    """Raised when the CSV file cannot be read correctly."""
    def __init__(self, message: str = "El archivo no se pudo leer correctamente.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class MissingColumnsError(AppError):
    """Raised when the CSV file does not contain required columns."""
    def __init__(self, message: str = "El archivo no contiene las columnas requeridas.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyHeadersError(AppError):
    """Raised when the CSV file has no valid headers."""
    def __init__(self, message: str = "El archivo no tiene encabezados válidos.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidCSVStructureError(AppError):
    """Raised when the CSV structure is invalid."""
    def __init__(self, message: str = "La estructura del archivo no es válida.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyDataFrameError(AppError):
    """Raised when the DataFrame has no rows or usable data."""
    def __init__(self, message: str = "No hay filas o datos utilizables.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class DataValidationError(AppError):
    """Raised when the DataFrame validation process fails."""
    def __init__(self, message: str = "El proceso de validación de datos falló.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class NoValidRowsError(AppError):
    """Raised when no valid rows are available for analysis."""
    def __init__(self, message: str = "No hay filas válidas disponibles para el análisis.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class ReportGenerationError(AppError):
    """Raised when the report text cannot be generated."""
    def __init__(self, message: str = "No se pudo generar el texto del reporte.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class ReportSaveError(AppError):
    """Raised when the report file cannot be saved."""
    def __init__(self, message: str = "No se pudo guardar el archivo del reporte.") -> None:
        """
        Args:
            message: descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)