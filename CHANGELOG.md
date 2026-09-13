# Changelog

## Unreleased

### Added

- Calibrated v2 scoring across headline specificity, evidence quality, ownership, technical depth, business impact, keyword coverage, and seniority alignment.
- Truth-constrained rewrite candidates that target the weakest experience statements first.
- Explicit evidence slots for missing ownership, technical detail, scope, and outcomes.
- Claim-preservation validation for source metrics and technologies.
- Anti-gaming calibration fixtures covering keyword stuffing, generic profiles, and outcome-poor technical profiles.
- `/v2/analyze` API endpoint while preserving the original `/analyze` contract.

### Improved

- Ownership scoring now rewards distinct signals with diminishing returns instead of rewarding repeated verbs.
- Impact scoring recognizes scaled quantities such as `500K+`, `10K+`, and `1,000+` while avoiding bare years.
- Causal impact detection no longer treats generic `to` phrasing as evidence.
- Roadmap now separates implemented capabilities from the next engineering milestones.

## 0.1.0

- Deterministic profile-quality scoring.
- Role keyword alignment with generic job-posting boilerplate filtering.
- UTF-8 job-description file input.
- TXT/Markdown resume ingestion.
- Normalized technical-term matching with common aliases.
- Before/after profile comparison.
- Optional FastAPI JSON API and local web interface.
- Evaluation cases and deterministic benchmark runner.
- CI, tests, MIT license, contribution and security documentation.
