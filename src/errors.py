"""Custom exception classes for the sales report project.

This module defines application-specific exceptions used across the
automatic sales report generator.

The goal of these custom errors is to make failures easier to understand,
handle, and report from the main application flow.
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
    def __init__(self, message: str = "File path is empty.") -> None:
        """
        Args:
            message: Descriptive message of the error. If 
                not specified, a generic message is used.
        """
        super().__init__(message)


class FileNotFoundAppError(AppError):
    """Raised when the provided file path does not exist."""
    def __init__(self, message: str = "File path does not exist.") -> None:
        """
        Args:
            message: Descriptive message of the error. If 
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidFilePathError(AppError):
    """Raised when the provided path is not a valid file."""
    def __init__(self, message: str = "Path not a valid file.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidFileExtensionError(AppError):
    """Raised when the file extension is not supported."""
    def __init__(self, message: str = "File extension is not supported.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyFileError(AppError):
    """Raised when the CSV file exists but has no content."""
    def __init__(self, message: str = "File exists but has no content.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class FileReadError(AppError):
    """Raised when the CSV file cannot be read correctly."""
    def __init__(self, message: str = "File cannot be read correctly.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class MissingColumnsError(AppError):
    """Raised when the CSV file does not contain required columns."""
    def __init__(self, message: str = "File does not contain required columns.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyHeadersError(AppError):
    """Raised when the CSV file has no valid headers."""
    def __init__(self, message: str = "File has no valid headers.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class InvalidCSVStructureError(AppError):
    """Raised when the CSV structure is invalid."""
    def __init__(self, message: str = "File structure is invalid.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class EmptyDataFrameError(AppError):
    """Raised when the DataFrame has no rows or usable data."""
    def __init__(self, message: str = "DataFrame has no rows or usable data.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class DataValidationError(AppError):
    """Raised when the DataFrame validation process fails."""
    def __init__(self, message: str = "DataFrame validation process failed.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class NoValidRowsError(AppError):
    """Raised when no valid rows are available for analysis."""
    def __init__(self, message: str = "No valid rows are available for analysis.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class ReportGenerationError(AppError):
    """Raised when the report text cannot be generated."""
    def __init__(self, message: str = "The report text cannot be generated.") -> None:
        """
        Args:
            message: Descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)


class ReportSaveError(AppError):
    """Raised when the report file cannot be saved."""
    def __init__(self, message: str = "The report file cannot be saved.") -> None:
        """
        Args:
            message: descriptive message of the error. If
                not specified, a generic message is used.
        """
        super().__init__(message)