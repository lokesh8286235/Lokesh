# LinkedIn Optimizer

Open-source, local-first tooling for turning real career evidence into a clearer, more searchable professional profile.

> **Optimize representation, never qualifications.**

## What it does

- Scores headline, About, measurable evidence, and target-role alignment.
- Provides a versioned v2 scoring engine with evidence quality and seniority alignment signals.
- Matches job descriptions with transparent lexical rules and technical aliases.
- Optionally adds embedding-based semantic similarity.
- Loads TXT/Markdown resumes and optionally PDF/DOCX documents.
- Compares before/after profile versions so improvements are measurable.
- Exposes an optional JSON API and a small local browser UI.
- Supports optional OpenAI and Anthropic recommendation adapters without making either provider a core dependency.
- Ships evaluation cases, tests, CI, contribution, and security policies.

## Quickstart

```bash
python -m pip install -e '.[dev]'
linkedin-optimizer profile.json --role "ML Engineer" --job job.md
linkedin-optimizer profile.json --role "ML Engineer" --job job.md --scoring v2
linkedin-optimizer --resume resume.md --role "ML Engineer" --job job.md
linkedin-optimizer --compare before.json after.json --role "ML Engineer" --job job.md
```

The CLI emits machine-readable JSON. The deterministic analyzer requires no API key and does not send profile data anywhere. `v1` remains the default for backward compatibility; `v2` is opt-in while its scoring behavior is evaluated independently.

### Resume formats

TXT/Markdown work with the core package. PDF/DOCX adapters are optional:

```bash
python -m pip install -e '.[documents]'
linkedin-optimizer --resume resume.pdf --role "ML Engineer" --job job.md
```

### Semantic matching

The baseline matcher is deterministic and transparent. For embedding similarity:

```bash
python -m pip install -e '.[semantic]'
```

Use `linkedin_optimizer.semantic.semantic_similarity(profile_text, role_text)` when semantic similarity is appropriate. The embedding model is optional and not downloaded by the core package.

### Optional API + UI

```bash
python -m pip install -e '.[api]'
uvicorn linkedin_optimizer.api:app --reload
```

Open the local server in a browser to use the UI, or call `POST /analyze` with `profile` and `role` JSON objects. `GET /health` provides a health check.

### Optional LLM recommendations

Provider adapters keep credentials in environment variables and are never invoked by the deterministic analyzer:

```bash
python -m pip install -e '.[openai]'
python -m pip install -e '.[anthropic]'
```

Use `OpenAIProvider` or `AnthropicProvider` from `linkedin_optimizer.providers` with your own prompt and explicit user-controlled workflow.

## Architecture

```text
Profile JSON / Resume ──┐
                        ▼
                 ┌──────────────┐
Job description ─► Normalizer   │
                 └──────┬───────┘
                        ▼
          ┌──────────────────────────┐
          │ Signals + lexical match  │
          │ optional embeddings      │
          └────────────┬─────────────┘
                       ▼
                Evidence Report
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
            CLI       API       Local UI
```

## Evaluation

Regression cases live in `eval/cases.json` and can be run with:

```bash
python scripts/evaluate.py
python eval/benchmark_v2.py
```

The v2 benchmark compares the legacy and v2 overall scores on fixed, deterministic profiles, making scoring changes inspectable rather than relying on subjective examples.

Changes to scoring/parsing should add tests and, when behavior changes intentionally, update the evaluation cases.

## Design principles

1. **Evidence over hype** — recommendations are traceable to profile text.
2. **Human-controlled** — suggestions never publish changes automatically.
3. **No fabrication** — never invent employers, metrics, skills, titles, or credentials.
4. **Role-aware** — quality is measured against a target role.
5. **Privacy-first** — local processing by default.
6. **Provider-neutral** — advanced AI is optional, not a core dependency.
7. **Reproducible** — deterministic scoring remains the regression baseline.

## Non-goals

This is not a scraper, impersonation tool, credential collector, or auto-publisher. It does not require LinkedIn login credentials.

## Project status

`0.1.0` is a working foundation covering deterministic scoring, role alignment, document ingestion, semantic matching, before/after comparison, optional API/UI, provider adapters, and regression evaluation. Future work can deepen extraction quality, evaluation coverage, and provider integrations.

## Contributing

See `CONTRIBUTING.md`. Quality changes should include tests. Security-sensitive issues should follow `SECURITY.md`.
