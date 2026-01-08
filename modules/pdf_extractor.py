"""
PDF Resume Extractor Module
Extracts text content from PDF resumes using pdfplumber
"""

import pdfplumber
from typing import Dict, Optional


class PDFExtractor:
    """Extract text content from PDF resumes"""

    @staticmethod
    def extract_text(pdf_path: str) -> Dict[str, any]:
        """
        Extract text from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract text from all pages
                full_text = ""
                page_texts = []

                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        page_texts.append({
                            "page": page_num,
                            "text": page_text
                        })
                        full_text += page_text + "\n\n"

                return {
                    "success": True,
                    "text": full_text.strip(),
                    "pages": len(pdf.pages),
                    "page_texts": page_texts,
                    "metadata": pdf.metadata
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": None
            }

    @staticmethod
    def validate_pdf(pdf_path: str) -> bool:
        """
        Validate if the file is a readable PDF

        Args:
            pdf_path: Path to the PDF file

        Returns:
            True if valid, False otherwise
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return len(pdf.pages) > 0
        except:
            return False
