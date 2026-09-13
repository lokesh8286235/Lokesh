from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role


def test_analyzer_v2_rewards_evidence_and_matching() -> None:
    profile = Profile(
        headline="Senior AI Engineer | Python | RAG",
        about="I build production AI systems with measurable outcomes.",
        experience=["Architected and deployed a RAG service for 10K users, reducing latency by 35%."],
        skills=["Python", "RAG", "PostgreSQL"],
    )
    role = Role(
        title="Senior AI Engineer",
        description="Build Python RAG systems with PostgreSQL and production services.",
    )

    report = analyze_v2(profile, role)
    names = {signal.name for signal in report.signals}
    assert report.overall_score > 50
    assert "evidence_quality" in names
    assert "seniority_alignment" in names
    assert "python" in report.matched_keywords


def test_analyzer_v2_flags_missing_seniority_signal() -> None:
    profile = Profile(headline="AI Engineer", experience=["Worked on software."])
    role = Role(title="Staff AI Engineer", description="Lead production systems.")

    report = analyze_v2(profile, role)
    seniority = next(signal for signal in report.signals if signal.name == "seniority_alignment")
    assert seniority.score < 80
