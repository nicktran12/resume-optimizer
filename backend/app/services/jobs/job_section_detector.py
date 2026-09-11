import re

KNOWN_SECTIONS = {
    "responsibilities": "Responsibilities",
    "what you'll do": "Responsibilities",
    "the role": "Responsibilities",
    "about the role": "Responsibilities",
    "requirements": "Requirements",
    "qualifications": "Requirements",
    "what you'll need": "Requirements",
    "minimum qualifications": "Requirements",
    "basic qualifications": "Requirements",
    "required skills": "Requirements",
    "required skills and experience": "Requirements",
    "preferred qualifications": "Preferred Qualifications",
    "nice to have": "Preferred Qualifications",
    "bonus points": "Preferred Qualifications",
    "skills": "Skills",
    "technical skills": "Skills",
    "about us": "Ignore",
    "about the company": "Ignore",
    "who we are": "Ignore",
    "benefits": "Ignore",
    "perks": "Ignore",
    "compensation": "Ignore",
    "benefits for u.s. employees": "Ignore",
    "equal opportunity employer": "Ignore",
    "pay transparency notice": "Ignore",
    "accommodations": "Ignore",
    "disclosures": "Ignore",
    "application limit": "Ignore",
    "know your rights": "Ignore",
    "e-verify": "Ignore",
}

MAX_HEADER_LINE_LENGTH = 60

def _match_section_header(line: str) -> str | None:
    candidate = line.strip().rstrip(":").lower()
    if not candidate or len(candidate) > MAX_HEADER_LINE_LENGTH:
        return None

    candidate = re.sub(r"\s+", " ", candidate)
    return KNOWN_SECTIONS.get(candidate)

def detect_sections(text: str) -> list[dict]:
    sections: list[dict] = []
    current_section = "Description"
    current_lines: list[str] = []

    def flush():
        section_text = "\n".join(current_lines).strip()
        if section_text and current_section != "Ignore":
            sections.append({"section": current_section, "text": section_text})

    for line in text.split("\n"):
        header = _match_section_header(line)
        if header:
            flush()
            current_section = header
            current_lines = []
        else:
            current_lines.append(line)

    flush()
    return sections