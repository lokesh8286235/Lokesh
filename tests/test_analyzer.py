from linkedin_optimizer import analyze
from linkedin_optimizer.models import Profile, Role


def test_role_alignment_and_metrics():
    profile = Profile(
        headline="Software Engineer | Python | FastAPI",
        about="I build reliable backend systems and data platforms.",
        experience=["Reduced API latency by 35% while supporting 10K daily requests."],
        skills=["Python", "FastAPI", "PostgreSQL"],
    )
    report = analyze(profile, Role(title="Python Backend Engineer", description="Python FastAPI PostgreSQL"))

    assert report.overall_score > 0
    assert "python" in report.matched_keywords
    assert any(signal.name == "measurable_evidence" and signal.score > 0 for signal in report.signals)


def test_generic_job_posting_words_do_not_count_as_target_keywords():
    profile = Profile(headline="Python Developer")
    report = analyze(
        profile,
        Role(title="Software Engineer", description="We are looking for an engineer to join our team."),
    )

    assert report.matched_keywords == []
    assert report.missing_keywords == []


def test_empty_profile_is_safe():
    report = analyze(Profile(), Role(title="Software Engineer"))
    assert report.overall_score == 25.0
    assert report.signals
