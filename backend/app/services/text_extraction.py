"""
Text extraction service — extracts plain text from uploaded resume files.
Supported formats: PDF, DOCX, TXT.
"""

from pathlib import Path


def extract_text_from_file(file_path: str | Path, filename: str) -> str:
    """
    Extract plain text from a resume file based on its extension.

    Args:
        file_path: Absolute path to the saved file.
        filename: Original filename (used to detect format).

    Returns:
        Extracted text content.

    Raises:
        ValueError: If the file format is not supported.
        RuntimeError: If extraction fails.
    """
    ext = Path(filename).suffix.lower()

    try:
        if ext == ".pdf":
            return _extract_pdf(file_path)
        elif ext == ".docx":
            return _extract_docx(file_path)
        elif ext == ".txt":
            return _extract_txt(file_path)
        else:
            raise ValueError(
                f"Unsupported file type: '{ext}'. "
                "Supported types: .pdf, .docx, .txt"
            )
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from '{filename}': {e}") from e


def _extract_pdf(file_path: str | Path) -> str:
    """Extract text from a PDF file using pdfplumber."""
    import pdfplumber

    text_parts: list[str] = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)


def _extract_docx(file_path: str | Path) -> str:
    """Extract text from a DOCX file using python-docx."""
    from docx import Document

    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def _extract_txt(file_path: str | Path) -> str:
    """Read a plain text file."""
    return Path(file_path).read_text(encoding="utf-8")
