"""A safe parser for a small, Python-literal configuration format.

This example demonstrates a remediation for code that previously evaluated
configuration input as executable Python. It accepts only literal values and
then validates the application's configuration schema.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass, asdict
from typing import Any


class ConfigurationError(ValueError):
    """Raised when configuration text is malformed or does not match the schema."""


@dataclass(frozen=True)
class ApplicationConfig:
    theme: str = "light"
    refresh_seconds: int = 30
    notifications: bool = True


ALLOWED_KEYS = {"theme", "refresh_seconds", "notifications"}
THEMES = {"light", "dark", "system"}
MAX_INPUT_LENGTH = 4_096


def parse_configuration(raw_text: str) -> ApplicationConfig:
    """Parse and validate an application configuration without executing input."""
    if not raw_text or len(raw_text) > MAX_INPUT_LENGTH:
        raise ConfigurationError("Configuration must contain 1 to 4096 characters.")

    try:
        candidate: Any = ast.literal_eval(raw_text)
    except (ValueError, SyntaxError) as exc:
        raise ConfigurationError("Configuration must be a valid literal dictionary.") from exc

    if not isinstance(candidate, dict):
        raise ConfigurationError("Configuration must be a dictionary.")

    unexpected = set(candidate) - ALLOWED_KEYS
    if unexpected:
        names = ", ".join(sorted(map(str, unexpected)))
        raise ConfigurationError(f"Unsupported setting(s): {names}.")

    theme = candidate.get("theme", "light")
    interval = candidate.get("refresh_seconds", 30)
    notifications = candidate.get("notifications", True)

    if theme not in THEMES:
        raise ConfigurationError("theme must be light, dark, or system.")
    if type(interval) is not int or not 5 <= interval <= 3_600:
        raise ConfigurationError("refresh_seconds must be an integer from 5 to 3600.")
    if type(notifications) is not bool:
        raise ConfigurationError("notifications must be true or false.")

    return ApplicationConfig(theme, interval, notifications)


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely validate configuration input.")
    parser.add_argument(
        "config",
        nargs="?",
        default="{'theme': 'dark', 'refresh_seconds': 60, 'notifications': True}",
        help="Python-literal dictionary, for example: {'theme': 'dark'}",
    )
    args = parser.parse_args()

    try:
        config = parse_configuration(args.config)
    except ConfigurationError as error:
        print(f"Configuration rejected: {error}")
        return 1

    print(json.dumps(asdict(config), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
