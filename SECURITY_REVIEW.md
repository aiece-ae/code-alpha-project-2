# Security review: configuration parsing

## Finding

**Severity: Critical** — User-supplied configuration was passed to Python's
`eval()` function. `eval()` treats input as code rather than data, enabling an
attacker to run arbitrary Python expressions under the application's account.

## Remediation

The replacement in `safe_config.py` uses `ast.literal_eval()`, which accepts
only Python literals such as dictionaries, strings, numbers, lists, and booleans.
It will reject function calls, imports, attribute access, and other executable
expressions. The parsed value is then checked against a strict allow-list and
type/range rules before the program uses it.

## Security controls included

- Input size limit to prevent oversized configuration payloads.
- Dictionary-only format and an explicit set of permitted settings.
- Type validation that excludes Python's `bool` values from integer settings.
- Bounded refresh interval and a fixed theme allow-list.
- Tests for an attempted code-execution payload and invalid configuration.

## Example

Accepted input:

```python
{'theme': 'dark', 'refresh_seconds': 60, 'notifications': True}
```

Rejected input:

```python
__import__('os').system('whoami')
```

For data exchanged with external systems, JSON or a schema-validated format is
usually preferable to Python-literal input. This example retains a literal
format only to demonstrate a safe direct replacement for the vulnerable code.
