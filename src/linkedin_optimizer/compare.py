from .analyzer import analyze
from .models import OptimizationReport, Profile, Role


def compare(before: Profile, after: Profile, role: Role) -> dict:
    """Compare two profile versions against the same target role."""
    before_report: OptimizationReport = analyze(before, role)
    after_report: OptimizationReport = analyze(after, role)
    return {
        "before_score": before_report.overall_score,
        "after_score": after_report.overall_score,
        "score_delta": round(after_report.overall_score - before_report.overall_score, 1),
        "new_matches": sorted(set(after_report.matched_keywords) - set(before_report.matched_keywords)),
        "remaining_missing": after_report.missing_keywords,
    }
