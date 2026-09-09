import re
from collections import Counter

def normalize_text(pages: list[str]) -> str:
    pages = _strip_repeated_headers_footers(pages)
    cleaned_pages = [_clean_page(p) for p in pages]
    return "\n\n".join(cleaned_pages)

def _clean_page(text: str) -> str:
    # Normalize Windows/Mac line endings to \n
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse runs of horizontal whitespace (spaces/tabs), but not newlines
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse 3+ blank lines down to a max of 2 (preserves paragraph/section
    # breaks without leaving huge gaps from PDF layout quirks)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip trailing whitespace on each line
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    # Remove common encoding artifacts PyMuPDF sometimes leaves behind
    text = text.replace("\uf0b7", "•")  # private-use-area bullet glyphs -> real bullet
    text = text.replace("\u2022", "•")  # normalize existing bullet variants
    text = text.replace("\xa0", " ")  # non-breaking space -> regular space

    return text.strip()

def _strip_repeated_headers_footers(pages: list[str]) -> str:
    if len(pages) < 3:
        return pages

    line_counts = Counter()
    for page in pages:
        lines = [line.strip() for line in page.split("\n") if line.strip()]
        edge_lines = lines[:2] + lines[-2:]
        line_counts.update(set(edge_lines))

    threshold = max(2, int(len(pages) * 0.6))
    repeated_lines = {line for line, count in line_counts.items() if count >= threshold}

    if not repeated_lines:
        return pages

    cleaned = []
    for page in pages:
        lines = [line for line in page.split("\n") if line.strip() not in repeated_lines]
        cleaned.append("\n".join(lines))

    return cleaned