"""Compare the legacy and v2 scoring engines on deterministic fixtures."""

import json
from pathlib import Path

from linkedin_optimizer.analyzer import analyze
from linkedin_optimizer.analyzer_v2 import analyze_v2
from linkedin_optimizer.models import Profile, Role


CASES = [
    {
        "name": "strong evidence + seniority",
        "profile": {
            "headline": "Senior AI Engineer | Python | RAG",
            "about": "I build production AI systems with measurable outcomes.",
            "experience": [
                "Architected and deployed a RAG service for 10K users, reducing latency by 35%."
            ],
            "skills": ["Python", "RAG", "PostgreSQL"],
        },
        "role": {
            "title": "Senior AI Engineer",
            "description": "Build Python RAG systems with PostgreSQL and production services.",
        },
    },
    {
        "name": "weak evidence + seniority gap",
        "profile": {
            "headline": "AI Engineer",
            "about": "Software engineer interested in AI.",
            "experience": ["Worked on software."],
            "skills": ["Python"],
        },
        "role": {
            "title": "Staff AI Engineer",
            "description": "Lead production Python RAG systems with PostgreSQL.",
        },
    },
]


def main() -> None:
    rows = []
    for case in CASES:
        profile = Profile.model_validate(case["profile"])
        role = Role.model_validate(case["role"])
        v1 = analyze(profile, role)
        v2 = analyze_v2(profile, role)
        rows.append(
            {
                "case": case["name"],
                "v1": v1.overall_score,
                "v2": v2.overall_score,
                "delta": round(v2.overall_score - v1.overall_score, 1),
            }
        )

    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
