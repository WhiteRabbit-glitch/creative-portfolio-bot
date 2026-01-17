"""
PDF processing utilities for text extraction.
"""
import PyPDF2
from typing import Optional


class PDFProcessor:
    """Handles PDF text extraction and processing."""

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract text from PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")

    @staticmethod
    def get_page_count(pdf_path: str) -> Optional[int]:
        """
        Get the number of pages in a PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages or None if error
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception:
            return None

    @staticmethod
    def validate_pdf(pdf_path: str) -> bool:
        """
        Validate if file is a readable PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if valid, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                PyPDF2.PdfReader(file)
            return True
        except Exception:
            return False
