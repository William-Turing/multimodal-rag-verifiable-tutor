from io import BytesIO
import pytest
from source_viewer import pdf_page_count, render_pdf_page


def test_pdf_page_navigation_with_synthetic_test_fixture(tmp_path):
    fitz = pytest.importorskip("fitz")
    pil = pytest.importorskip("PIL.Image")
    output = tmp_path / "test_fixture_not_real_course_content.pdf"
    with fitz.open() as doc:
        for i in range(2):
            page = doc.new_page()
            page.insert_text((70, 80), f"Synthetic test page {i+1}")
        doc.save(str(output))
    assert pdf_page_count(output) == 2
    for page in (1, 2):
        png = render_pdf_page(output, page)
        assert png.startswith(b"\x89PNG")
        im = pil.open(BytesIO(png))
        assert im.width > 0 and im.height > 0
    with pytest.raises(ValueError, match="outside"):
        render_pdf_page(output, 0)
    with pytest.raises(ValueError, match="outside"):
        render_pdf_page(output, 3)
