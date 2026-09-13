from pathlib import Path

from .resume import parse_resume_text
from .models import Profile


def load_document(path: str | Path) -> Profile:
    """Load a resume from TXT/Markdown, PDF, or DOCX using optional adapters."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        return parse_resume_text(path.read_text(encoding="utf-8"))
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install the documents extra: pip install 'linkedin-optimizer[documents]'") from exc
        text = "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
        return parse_resume_text(text)
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise RuntimeError("Install the documents extra: pip install 'linkedin-optimizer[documents]'") from exc
        text = "\n".join(paragraph.text for paragraph in Document(path).paragraphs)
        return parse_resume_text(text)
    raise ValueError("Unsupported resume format; use TXT, Markdown, PDF, or DOCX.")
