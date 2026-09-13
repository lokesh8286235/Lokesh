# LinkedIn Optimizer

**Evidence-first career intelligence for engineers.**

Turn a real resume/profile and a target job description into a measurable alignment report, calibrated quality signals, and **truth-constrained rewrite recommendations**.

> **Optimize representation. Never manufacture qualifications.**

This project is deliberately built as an engineering system—not a prompt wrapper. The core scoring path is deterministic, inspectable, testable, and usable without an API key. Optional semantic and LLM layers sit outside that baseline.

## Why this exists

Most profile optimizers reward keyword density. That creates a bad failure mode: a profile can look optimized while saying very little about what the engineer actually built.

LinkedIn Optimizer treats a profile as evidence:

```text
Profile / Resume + Target Role
             │
             ▼
       Normalize inputs
             │
             ▼
   ┌───────────────────────┐
   │ Role alignment        │
   │ Evidence quality      │
   │ Ownership             │
   │ Technical depth       │
   │ Business impact       │
   │ Seniority alignment   │
   └───────────┬───────────┘
               ▼
       Explainable report
               │
        ┌──────┴──────┐
        ▼             ▼
   Gap analysis   Safe rewrites
                      │
                      ▼
              Missing evidence
              stays explicit
```

## What is engineered here

- **Transparent scoring** — independent quality dimensions instead of one opaque keyword score.
- **Anti-gaming calibration** — fixed evaluation cases test strong evidence against keyword stuffing, generic profiles, and technically dense but outcome-poor profiles.
- **Evidence-backed rewrites** — the weakest experience statements are selected first and strengthened without inventing facts.
- **Claim preservation** — existing metrics and technologies must survive a rewrite; missing facts become explicit `[add verified ...]` slots.
- **Role alignment** — deterministic matching with technical aliases, plus optional embedding similarity.
- **Versioned scoring** — v1 remains the compatibility baseline; v2 is opt-in and evaluated independently.
- **Document ingestion** — TXT/Markdown in core; optional PDF/DOCX adapters.
- **Before/after comparison** — profile changes can be measured instead of judged by feel.
- **Developer interfaces** — machine-readable CLI output and an optional FastAPI/local UI.
- **Provider-neutral AI** — optional OpenAI/Anthropic adapters; deterministic analysis does not require credentials.
- **Privacy by default** — no LinkedIn credentials, scraping, impersonation, or automatic publishing.

## Quickstart

```bash
python -m pip install -e '.[dev]'
linkedin-optimizer profile.json --role "ML Engineer" --job job.md --scoring v2
linkedin-optimizer --resume resume.md --role "ML Engineer" --job job.md --scoring v2
linkedin-optimizer --compare before.json after.json --role "ML Engineer" --job job.md
```

The CLI emits JSON. The deterministic analyzer sends no profile data anywhere.

### Example output shape

```json
{
  "overall_score": 84.7,
  "signals": [
    {"name": "ownership", "score": 72.0},
    {"name": "technical_depth", "score": 81.0},
    {"name": "business_impact", "score": 94.0}
  ],
  "matched_keywords": ["python", "rag", "postgresql"],
  "missing_keywords": ["kafka"],
  "rewrite_candidates": [
    {
      "original": "Worked on an application.",
      "rewritten": "Worked on an application. [add your verified ownership/action]. [add verified outcome: latency, cost, reliability, scale, or user impact].",
      "missing_evidence": ["personal ownership", "measurable outcome", "scope/scale"]
    }
  ]
}
```

The example demonstrates the important guarantee: **the tool does not invent the missing result.**

## Scoring model

The v2 engine separates dimensions so one signal family cannot dominate the entire report:

| Dimension | Purpose |
| --- | --- |
| Headline specificity | Is the target positioning immediately clear? |
| About depth | Does the summary provide enough context to be useful? |
| Evidence quality | Are actions, metrics, and scope observable? |
| Ownership | Is personal contribution explicit? |
| Technical depth | Are concrete technologies and systems present? |
| Business impact | Are outcomes tied to measurable effects? |
| Keyword coverage | Does the profile actually match the target role? |
| Seniority alignment | Does the profile communicate the level the role expects? |

The weighted score is intentionally inspectable in `src/linkedin_optimizer/analyzer_v2.py`.

## Truth-constrained rewriting

The rewrite layer is deterministic and evidence-first:

1. Split experience into candidate statements.
2. Score each statement using the same quality dimensions.
3. Rank the weakest evidence first.
4. Preserve the original claim.
5. Add only explicit evidence slots for facts that are missing.
6. Verify that original metrics and technologies remain present.

It will **not** invent a percentage, revenue number, user count, employer, technology, title, or outcome.

## Evaluation

Regression data lives in `eval/` and tests live in `tests/`.

```bash
python scripts/evaluate.py
python eval/benchmark_v2.py
python -m pytest
```

The calibration suite specifically checks that evidence-rich profiles beat keyword stuffing and that technical depth without impact is not mistaken for strong business evidence.

When scoring behavior changes intentionally, update the evaluation cases and tests in the same change.

## Optional capabilities

### Semantic matching

```bash
python -m pip install -e '.[semantic]'
```

Embedding similarity is optional and isolated from the deterministic baseline.

### API + local UI

```bash
python -m pip install -e '.[api]'
uvicorn linkedin_optimizer.api:app --reload
```

### PDF/DOCX

```bash
python -m pip install -e '.[documents]'
```

### LLM recommendations

```bash
python -m pip install -e '.[openai]'
python -m pip install -e '.[anthropic]'
```

Provider adapters are explicit opt-ins and keep credentials in environment variables.

## Repository map

```text
src/linkedin_optimizer/
├── analyzer.py          # v1 compatibility analyzer
├── analyzer_v2.py       # calibrated multi-dimensional scoring
├── evidence.py          # deterministic evidence signals
├── matching.py          # role/profile alignment
├── rewriter.py          # truth-constrained rewrite candidates
├── scoring.py           # anti-gaming quality primitives
├── models.py            # typed report contracts
├── documents.py         # optional document ingestion
├── semantic.py          # optional embeddings
├── providers.py         # optional LLM adapters
├── api.py               # optional FastAPI surface
└── cli.py               # command-line entry point

eval/
├── cases.json           # baseline regression cases
├── v2_cases.json        # v2 calibration fixtures
└── benchmark_v2.py      # v1/v2 comparison

tests/
├── test_scoring.py
├── test_calibration.py
└── test_rewriter.py
```

## Engineering principles

1. **Evidence over hype.** Every recommendation should trace back to observable text.
2. **No fabrication.** Missing evidence is surfaced, never guessed.
3. **Human-controlled.** The user reviews every change; nothing is published automatically.
4. **Deterministic baseline.** Core analysis is reproducible without an LLM.
5. **Evaluation before optimization.** Scoring changes are tested against fixed cases.
6. **Privacy-first.** Local processing is the default.
7. **Provider-neutral.** AI providers are optional implementation details.

## Non-goals

This is not a LinkedIn scraper, impersonation tool, credential collector, or auto-publisher. It does not require LinkedIn login credentials.

## Status

**0.1.x — active engineering project.** The repository currently focuses on deterministic role alignment, calibrated profile quality scoring, evidence-backed rewrites, evaluation, and developer tooling. The roadmap favors deeper evaluation and extraction quality over adding superficial features.

## Contributing

See `CONTRIBUTING.md` for development expectations. Quality changes should include tests. Security-sensitive issues should follow `SECURITY.md`.

## License

MIT
