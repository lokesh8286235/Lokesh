from linkedin_optimizer.compare import compare
from linkedin_optimizer.models import Profile, Role


def test_compare_reports_improvement():
    role = Role(title="Python Engineer", description="Python FastAPI PostgreSQL")
    before = Profile(headline="Developer")
    after = Profile(headline="Python Engineer", skills=["Python", "FastAPI", "PostgreSQL"])
    report = compare(before, after, role)
    assert report.after_score > report.before_score
    assert report.score_delta > 0
    assert "python" in report.newly_matched_keywords
