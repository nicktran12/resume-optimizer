import pymupdf

from app.services.normalizer import normalize_text

class PageText:
    def __init__(self, page_number: int, text: str):
        self.page_number = page_number
        self.text = text

def extract_text_by_page(pdf_bytes: bytes) -> list[PageText]:
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Could not open PDF: {e}") from e

    if doc.is_encrypted:
        doc.close()
        raise ValueError("PDF is password-protected and cannot be processed.")

    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()
        pages.append(PageText(page_number=page_number, text=text))

    doc.close()

    if not any(p.text.strip() for p in pages):
        raise ValueError(
            "No extractable text found in PDF. It may be a scanned image without OCR."
        )

    return pages

def extract_full_text(pdf_bytes: bytes) -> str:
    pages = extract_text_by_page(pdf_bytes)
    return normalize_text([p.text for p in pages])