import re

SUSPICIOUS_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"you\s+are\s+now\s+(a|an)\s+\w+",
    r"system\s*:\s*",
    r"new\s+instructions?\s*:",
    r"forget\s+(everything|all)\s+(you|above)",
    r"give\s+(this|the)\s+candidate\s+a?\s*\d{2,3}%",
    r"assign\s+a?\s*score\s+of\s+\d{2,3}",
]

_COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_PATTERNS]

MAX_REASONABLE_LENGTH = 50_000


def scan_for_injection(text: str) -> list[str]:
    findings = []
    for pattern in _COMPILED_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(f"Matched suspicious pattern: {match.group(0)!r}")
    return findings


def sanitize_for_llm(text: str, source: str = "content") -> str:
    if len(text) > MAX_REASONABLE_LENGTH:
        raise ValueError(f"{source} exceeds reasonable length ({len(text)} chars) and was rejected.")

    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"[\uE000-\uF8FF\U000F0000-\U000FFFFD\U00100000-\U0010FFFD]", "", text)

    return text.strip()