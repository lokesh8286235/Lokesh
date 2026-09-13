# v0.2 Roadmap

The v0.1 foundation is evidence-first, deterministic, and local-first. The v0.2 work now focuses on making recommendations more trustworthy, measurable, and useful in real recruiting workflows.

## Completed foundation

- [x] Bullet-level diagnostics and weakest-first rewrite selection
- [x] Structured evidence signals for ownership, technical depth, impact, and scope
- [x] Truth-preserving rewrite candidates with explicit evidence slots
- [x] Claim-preservation guard for existing metrics and technologies
- [x] Calibrated multi-dimensional v2 scoring
- [x] Anti-gaming fixtures for keyword stuffing and generic profiles
- [x] Optional semantic matching isolated from the deterministic baseline
- [x] Human review boundary: no scraping, impersonation, credential collection, or automatic publishing
- [x] v2 CLI and API surfaces

## Next engineering work

1. **Evidence extraction 2.0** — extract quantities, scope, technologies, ownership, and causal relationships into a typed evidence graph rather than regex-only counts.
2. **Role requirement weighting** — distinguish must-have, nice-to-have, and boilerplate job terms so gap prioritization reflects actual hiring signals.
3. **Calibration expansion** — add adversarial cases for synonym stuffing, metric dumping, seniority mismatch, and keyword placement without evidence.
4. **Rewrite quality evaluation** — score candidate rewrites for claim preservation, evidence coverage, readability, and role relevance with fixed regression fixtures.
5. **Structured output formats** — add a concise human-readable report alongside the machine-readable JSON contract.
6. **Optional model-assisted review** — allow an LLM to critique deterministic findings without allowing it to mutate source claims or publish changes.
7. **Release discipline** — publish versioned evaluation artifacts and changelog entries whenever scoring behavior changes.
