# CodeAlpha Task 2 — Safe configuration review

An original security-review and remediation project. It shows how to replace
unsafe evaluation of configuration input with literal-only parsing plus schema
validation.

## Run the demo

```bash
python3 safe_config.py "{'theme': 'dark', 'refresh_seconds': 60}"
```

## Run tests

```bash
python3 -m unittest -v
```

## Included files

- `safe_config.py` — safe parser, validation rules, and CLI demo
- `test_safe_config.py` — automated security and validation tests
- `SECURITY_REVIEW.md` — review finding and remediation rationale
