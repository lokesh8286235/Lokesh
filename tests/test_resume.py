import pytest

from linkedin_optimizer.resume import load_resume, parse_resume_text


def test_parse_resume_sections():
    profile = parse_resume_text("""Lokesh — AI Software Engineer
Summary
Builds production AI systems with measurable outcomes.
Experience
- Reduced p95 latency by 35%
- Supported 1,000 queries/day
Skills
Python, FastAPI, PostgreSQL, RAG
""")
    assert profile.headline.startswith("Lokesh")
    assert "latency" in profile.experience[0]
    assert "Python" in profile.skills


def test_resume_extension_is_explicit(tmp_path):
    path = tmp_path / "resume.pdf"
    path.write_text("not actually a pdf", encoding="utf-8")
    with pytest.raises(ValueError, match="supports"):
        load_resume(path)
