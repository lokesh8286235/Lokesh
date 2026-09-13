from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role


def _signal(report, name):
    return next(signal for signal in report.signals if signal.name == name)


def test_v2_separates_ownership_technical_depth_and_impact() -> None:
    profile = Profile(
        headline="Senior AI Engineer | Python | RAG",
        about="Build production systems.",
        experience=[
            "Owned and deployed a Python RAG service for 10K users, reducing latency by 35% and manual lookup time by 40%."
        ],
        skills=["Python", "FastAPI", "PostgreSQL", "Kubernetes"],
    )
    role = Role(title="Senior AI Engineer", description="Build Python RAG systems with PostgreSQL.")

    report = analyze_v2(profile, role)

    assert _signal(report, "ownership").score >= 40
    assert _signal(report, "technical_depth").score >= 40
    assert _signal(report, "business_impact").score >= 60


def test_v2_penalizes_generic_experience() -> None:
    profile = Profile(
        headline="AI Engineer",
        about="Software engineer.",
        experience=["Worked on projects and helped the team."],
        skills=["Python"],
    )
    role = Role(title="Senior AI Engineer", description="Build production Python systems.")

    report = analyze_v2(profile, role)

    assert _signal(report, "ownership").score == 0
    assert _signal(report, "business_impact").score == 0
    assert _signal(report, "seniority_alignment").score < 80
