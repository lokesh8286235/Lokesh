from .analyzer import analyze
from .models import ComparisonReport, Profile, Role


def compare(before: Profile, after: Profile, role: Role) -> ComparisonReport:
    """Compare two profile versions against the same target role."""
    old = analyze(before, role)
    new = analyze(after, role)
    return ComparisonReport(
        before_score=old.overall_score,
        after_score=new.overall_score,
        score_delta=round(new.overall_score - old.overall_score, 1),
        newly_matched_keywords=sorted(set(new.matched_keywords) - set(old.matched_keywords)),
        resolved_missing_keywords=sorted(set(old.missing_keywords) - set(new.missing_keywords)),
        remaining_missing_keywords=new.missing_keywords,
    )
