# LinkedIn Optimizer

Open-source, local-first tooling for turning real career evidence into a clearer, more searchable professional profile.

> **Optimize representation, never qualifications.**

## What it does

- Scores headline, About, measurable evidence, and target-role alignment.
- Matches job descriptions against a profile with transparent lexical rules and technical aliases.
- Loads TXT/Markdown resumes into the same normalized profile model.
- Compares before/after profile versions so improvements are measurable.
- Exposes an optional JSON API and a small local browser UI.
- Ships evaluation cases, tests, CI, and contribution/security policies.

## Quickstart

```bash
python -m pip install -e '.[dev]'
linkedin-optimizer profile.json --role "ML Engineer" --job job.md
linkedin-optimizer --resume resume.md --role "ML Engineer" --job job.md
linkedin-optimizer --compare before.json after.json --role "ML Engineer" --job job.md
```

The CLI emits machine-readable JSON. The core analyzer requires no API key and does not send profile data anywhere.

### Optional API + UI

```bash
python -m pip install -e '.[api]'
uvicorn linkedin_optimizer.api:app --reload
```

Open the local server in a browser to use the UI, or call `POST /analyze` with `profile` and `role` JSON objects. `GET /health` provides a health check.

## Architecture

```text
Profile JSON / Resume ──┐
                        ▼
                 ┌──────────────┐
Job description ─► Normalizer   │
                 └──────┬───────┘
                        ▼
              ┌───────────────────┐
              │ Signal + Matcher  │
              └─────────┬─────────┘
                        ▼
              ┌───────────────────┐
              │ Evidence Report   │
              └─────────┬─────────┘
                        ▼
            CLI / JSON API / Local UI
```

## Scoring philosophy

The baseline is intentionally deterministic. A reviewer can inspect the text, reproduce the result, and understand why a recommendation appeared. Technical aliases such as `K8s → Kubernetes`, `Postgres → PostgreSQL`, and `ML → machine-learning` improve recall without pretending that keyword overlap is true semantic understanding.

The roadmap can add embeddings or LLM providers behind explicit adapters; the core will remain usable without them.

## Evaluation

Regression cases live in `eval/cases.json` and can be run with:

```bash
python scripts/evaluate.py
```

Changes to scoring/parsing should add tests and, when behavior changes intentionally, update the evaluation cases.

## Design principles

1. **Evidence over hype** — recommendations should be traceable to profile text.
2. **Human-controlled** — suggestions never publish changes automatically.
3. **No fabrication** — never invent employers, metrics, skills, titles, or credentials.
4. **Role-aware** — quality is measured against a target role.
5. **Privacy-first** — local processing by default.
6. **Provider-neutral** — advanced AI is optional, not a core dependency.

## Non-goals

This is not a scraper, impersonation tool, credential collector, or auto-publisher. It does not require LinkedIn login credentials.

## Project status

`0.1.0` is a working deterministic foundation. PDF/DOCX adapters, embedding-backed semantic matching, provider adapters, and richer evaluation suites are natural next layers rather than hidden assumptions.

## Contributing

See `CONTRIBUTING.md`. Quality changes should include tests. Security-sensitive issues should follow `SECURITY.md`.

## License

MIT
