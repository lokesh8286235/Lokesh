# LinkedIn Optimizer

Open-source tooling for turning a LinkedIn profile into a clearer, more searchable, and more credible professional profile.

## What it does

LinkedIn Optimizer analyzes profile text against a target role and produces **evidence-based recommendations** across:

- **Headline** — clarity, role targeting, keywords, and specificity
- **About** — positioning, proof, readability, and structure
- **Experience** — impact, ownership, metrics, and action-oriented language
- **Skills** — relevance and keyword coverage against a target role
- **Role alignment** — meaningful keyword coverage from a job description

The goal is not to manufacture buzzwords or spam keywords. It is to help people communicate real experience more effectively.

## Current MVP

The project is currently a deterministic Python toolkit. It accepts a structured profile plus either a role description string or a UTF-8 job-description file.

```bash
pip install -e '.[dev]'
careeropt profile.json --role "ML Engineer" --job job.md
```

The CLI emits JSON containing the overall score, individual signals, matched keywords, and missing keywords. No external API key is required for the deterministic analyzer.

## Design principles

1. **Evidence over hype** — recommendations should point to the text that caused them.
2. **Human-controlled** — the tool suggests changes; the user decides what is true.
3. **No fabricated experience** — never invent employers, metrics, skills, titles, or credentials.
4. **Role-aware** — optimization should be evaluated against a target role, not a generic score.
5. **Privacy-first** — profile and job text are processed locally by default.

## Architecture

```text
Profile JSON ───────────┐
                        ▼
                 ┌───────────────┐
Job description ─► Role Matcher  │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ Signal Engine │
                 └───────┬───────┘
                         ▼
                 ┌───────────────┐
                 │ Report / JSON  │
                 └───────────────┘
```

## Roadmap

- [x] Profile input schema
- [x] Deterministic profile-quality analyzer
- [x] Target-role keyword coverage
- [x] Evidence-backed recommendations
- [x] Job-description file input
- [ ] Resume document ingestion
- [ ] Semantic role matching
- [ ] Before/after comparison
- [ ] LLM-assisted recommendations with provider adapters
- [ ] Evaluation dataset and regression benchmarks
- [ ] JSON API
- [ ] Web interface
- [ ] First tagged release

## Important boundary

This project is an **optimization assistant**, not a LinkedIn automation bot. It should not scrape private data, impersonate users, fabricate credentials, or automatically publish changes without explicit user control.

## Contributing

Contributions should improve analysis quality, test coverage, documentation, or developer experience. New scoring rules should include deterministic tests and explain what evidence they use.

## License

MIT
