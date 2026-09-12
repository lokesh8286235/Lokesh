# LinkedIn Optimizer

Open-source tooling for turning a LinkedIn profile into a clearer, more searchable, and more credible professional profile.

## What it does

LinkedIn Optimizer analyzes profile text and gives **evidence-based recommendations** across:

- **Headline** — clarity, role targeting, keywords, and specificity
- **About** — positioning, proof, readability, and structure
- **Experience** — impact, ownership, metrics, and action-oriented language
- **Skills** — relevance and keyword coverage against a target role
- **Profile consistency** — alignment between headline, summary, experience, and target role

The goal is not to manufacture buzzwords or spam keywords. It is to help people communicate real experience more effectively.

## Design principles

1. **Evidence over hype** — recommendations should point to the text that caused them.
2. **Human-controlled** — the tool suggests changes; the user decides what is true.
3. **No fabricated experience** — never invent employers, metrics, skills, titles, or credentials.
4. **Role-aware** — optimization should be evaluated against a target role, not a generic score.
5. **Privacy-first** — profile text should be processed locally by default whenever possible.

## Planned architecture

```text
LinkedIn profile text
        │
        ▼
┌───────────────────┐
│ Profile Parser    │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Signal Extraction │─── keywords / metrics / claims / structure
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Role Matcher      │─── target role / job description
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ Recommendation    │─── issue → evidence → suggestion
│ Engine            │
└─────────┬─────────┘
          ▼
     Actionable report
```

## MVP roadmap

- [ ] Profile input schema
- [ ] Deterministic profile-quality analyzer
- [ ] Target-role keyword coverage
- [ ] Evidence-backed recommendations
- [ ] Before/after comparison
- [ ] JSON API
- [ ] Web interface
- [ ] Automated evaluation set
- [ ] GitHub Actions CI

## Important boundary

This project is an **optimization assistant**, not a LinkedIn automation bot. It should not scrape private data, impersonate users, fabricate credentials, or automatically publish changes without explicit user control.

## License

MIT