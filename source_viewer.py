"""Small, independently testable PDF source-navigation utilities."""
from __future__ import annotations
from pathlib import Path


def pdf_page_count(path: str | Path) -> int:
    import fitz
    with fitz.open(str(path)) as document:
        return document.page_count


def render_pdf_page(path: str | Path, page_number: int) -> bytes:
    """Render one 1-based PDF page; never guess offsets or document identities."""
    import fitz
    with fitz.open(str(path)) as document:
        if not isinstance(page_number, int) or isinstance(page_number, bool):
            raise ValueError("PDF page_number must be a 1-based integer")
        if not 1 <= page_number <= document.page_count:
            raise ValueError(f"PDF page {page_number} outside 1..{document.page_count}")
        pixmap = document.load_page(page_number - 1).get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        return pixmap.tobytes("png")
