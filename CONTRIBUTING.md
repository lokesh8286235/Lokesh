# Contributing

Thanks for improving LinkedIn Optimizer.

## Development

```bash
python -m pip install -e '.[dev]'
ruff check .
pytest -q
```

## What makes a good change?

- Improves analysis quality, correctness, privacy, or developer experience.
- Includes deterministic tests for scoring or parsing changes.
- Avoids fabricated career claims or opaque scoring rules.
- Keeps the core dependency-light and provider-neutral.

For larger changes, open an issue first so the design can be discussed before implementation.
