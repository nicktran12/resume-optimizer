import re

LINES_PER_CHUNK = 8
OVERLAP_LINES = 2
MAX_LINE_LENGTH = 300

def _split_into_units(text: str) -> list[str]:
    units = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        if len(line) <= MAX_LINE_LENGTH:
            units.append(line)
        else:
            sentences = re.split(r"(?<=[.!?])\s+", line)
            units.extend(s.strip() for s in sentences if s.strip())

    return units

def chunk_sections(sections: list[dict]) -> list[dict]:
    chunks = []
    chunk_index = 0
    step = LINES_PER_CHUNK - OVERLAP_LINES

    for sec in sections:
        units = _split_into_units(sec["text"])
        if not units:
            continue

        i = 0
        while i < len(units):
            window = units[i : i + LINES_PER_CHUNK]
            content = "\n".join(window).strip()
            if content:
                chunks.append(
                    {
                        "content": content,
                        "section": sec["section"],
                        "page": sec["page"],
                        "chunk_index": chunk_index,
                    }
                )
                chunk_index += 1

            if i + LINES_PER_CHUNK >= len(units):
                break

            i += step

    return chunks