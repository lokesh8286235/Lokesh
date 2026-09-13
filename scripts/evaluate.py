import json
from pathlib import Path

from linkedin_optimizer.analyzer import analyze
from linkedin_optimizer.models import Profile, Role


def main() -> None:
    cases = json.loads(Path("eval/cases.json").read_text(encoding="utf-8"))
    scores = []
    for case in cases:
        report = analyze(Profile.model_validate(case["profile"]), Role.model_validate(case["role"]))
        score = report.overall_score
        scores.append(score)
        if "min_score" in case and score < case["min_score"]:
            raise SystemExit(f"{case['name']}: {score} < {case['min_score']}")
        if "max_score" in case and score > case["max_score"]:
            raise SystemExit(f"{case['name']}: {score} > {case['max_score']}")
        print(f"{case['name']}: {score:.1f}")
    print(f"mean: {sum(scores) / len(scores):.1f}")


if __name__ == "__main__":
    main()
