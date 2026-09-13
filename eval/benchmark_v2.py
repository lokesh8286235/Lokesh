"""Compare v1/v2 and expose calibrated quality dimensions."""

import json
from pathlib import Path

from linkedin_optimizer.analyzer import analyze
from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role

CASES = json.loads((Path(__file__).with_name("v2_cases.json")).read_text(encoding="utf-8"))


def main() -> None:
    rows = []
    for case in CASES:
        profile = Profile.model_validate(case["profile"])
        role = Role.model_validate(case["role"])
        report = analyze_v2(profile, role)
        signals = {signal.name: signal.score for signal in report.signals}
        v1 = analyze(profile, role).overall_score
        rows.append({
            "case": case["name"],
            "v1": v1,
            "v2": report.overall_score,
            "delta": round(report.overall_score - v1, 1),
            "ownership": signals["ownership"],
            "technical_depth": signals["technical_depth"],
            "business_impact": signals["business_impact"],
            "evidence_quality": signals["evidence_quality"],
            "keyword_coverage": signals["keyword_coverage"],
        })
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
