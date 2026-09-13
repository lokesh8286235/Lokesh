from eval.benchmark_v2 import CASES
from linkedin_optimizer.analyzer import analyze
from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role


def test_v2_benchmark_preserves_directional_behavior() -> None:
    scores = []
    for case in CASES:
        profile = Profile.model_validate(case["profile"])
        role = Role.model_validate(case["role"])
        scores.append((analyze(profile, role).overall_score, analyze_v2(profile, role).overall_score))

    assert scores[0][1] > scores[0][0]
    assert scores[1][1] < scores[0][1]


def test_architected_is_not_treated_as_seniority() -> None:
    profile = Profile(
        headline="AI Engineer",
        experience=["Architected a production service for 10K users."],
    )
    role = Role(title="Staff AI Engineer", description="Lead production systems.")

    report = analyze_v2(profile, role)
    seniority = next(signal for signal in report.signals if signal.name == "seniority_alignment")

    assert seniority.score == 35.0
