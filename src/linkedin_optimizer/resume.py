import re
from pathlib import Path

from .models import Profile

_SECTION_MAP = {
    "summary": "about", "professional summary": "about", "about": "about",
    "profile": "about", "experience": "experience", "work experience": "experience",
    "professional experience": "experience", "skills": "skills", "technical skills": "skills",
}


def _header(line: str) -> str | None:
    normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
    return _SECTION_MAP.get(normalized)


def parse_resume_text(text: str) -> Profile:
    """Deterministically map common resume sections into a Profile."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return Profile()
    headline = lines[0]
    sections: dict[str, list[str]] = {"about": [], "experience": [], "skills": []}
    current: str | None = None
    for line in lines[1:]:
        section = _header(line)
        if section:
            current = section
            continue
        if current:
            sections[current].append(line.lstrip("-•* "))
    skills = []
    for line in sections["skills"]:
        skills.extend(x.strip() for x in re.split(r"[,|;]", line) if x.strip())
    return Profile(
        headline=headline,
        about=" ".join(sections["about"]),
        experience=sections["experience"],
        skills=skills,
    )


def load_resume(path: str | Path) -> Profile:
    """Load TXT/Markdown resumes without requiring heavyweight parsers."""
    suffix = Path(path).suffix.lower()
    if suffix not in {".txt", ".md", ".markdown"}:
        raise ValueError("MVP resume ingestion supports .txt, .md, and .markdown; PDF/DOCX adapters are planned.")
    return parse_resume_text(Path(path).read_text(encoding="utf-8"))
