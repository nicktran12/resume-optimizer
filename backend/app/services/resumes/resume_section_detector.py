import re

KNOWN_SECTIONS = {
    "summary": "Summary",
    "professional summary": "Summary",
    "objective": "Summary",
    "about": "Summary",
    "education": "Education",
    "experience": "Experience",
    "work experience": "Experience",
    "professional experience": "Experience",
    "employment history": "Experience",
    "projects": "Projects",
    "personal projects": "Projects",
    "skills": "Skills",
    "technical skills": "Skills",
    "core competencies": "Skills",
    "leadership": "Leadership",
    "leadership experience": "Leadership",
    "activities": "Activities",
    "extracurricular activities": "Activities",
    "certifications": "Certifications",
    "awards": "Awards",
    "honors and awards": "Awards",
    "publications": "Publications",
    "volunteer": "Volunteer",
    "volunteer experience": "Volunteer",
    "interests": "Interests",
}

MAX_HEADER_LINE_LENGTH = 40

def _match_section_header(line: str) -> str | None:
    candidate = line.strip().rstrip(":").lower()
    if not candidate or len(candidate) > MAX_HEADER_LINE_LENGTH:
        return None

    candidate = re.sub(r"\s+", " ", candidate)
    return KNOWN_SECTIONS.get(candidate)

def detect_sections(pages: list[tuple[int, str]]) -> list[dict]:
    sections: list[dict] = []
    current_section = "Summary"
    current_page = pages[0][0] if pages else 1
    current_lines: list[str] = []

    def flush():
        text = "\n".join(current_lines).strip()
        if text:
            sections.append({"section": current_section, "text": text, "page": current_page})

    for page_number, page_text in pages:
        for line in page_text.split("\n"):
            header = _match_section_header(line)
            if header:
                flush()
                current_section = header
                current_page = page_number
                current_lines = []
            else:
                current_lines.append(line)

    flush()
    return sections