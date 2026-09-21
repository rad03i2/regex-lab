from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Iterable

MAX_PATTERN_LENGTH = 10_000
MAX_TEXT_LENGTH = 5_000_000

FLAG_MAP = {
    "i": re.IGNORECASE,
    "m": re.MULTILINE,
    "s": re.DOTALL,
    "x": re.VERBOSE,
    "a": re.ASCII,
}

class RegexLabError(ValueError):
    """User-facing validation or regular-expression error."""

@dataclass(frozen=True)
class MatchResult:
    value: str
    start: int
    end: int
    groups: tuple[str | None, ...]
    groupdict: dict[str, str | None]

    def to_dict(self) -> dict:
        data = asdict(self)
        data["groups"] = list(self.groups)
        return data


def parse_flags(value: str = "") -> re.RegexFlag:
    flags = re.NOFLAG
    unknown = sorted(set(value.lower()) - set(FLAG_MAP))
    if unknown:
        raise RegexLabError(f"Unknown flag(s): {', '.join(unknown)}. Supported: im sxa".replace(" ", ""))
    for char in value.lower():
        flags |= FLAG_MAP[char]
    return flags


def compile_pattern(pattern: str, flags: str = "") -> re.Pattern[str]:
    if not pattern:
        raise RegexLabError("Pattern must not be empty.")
    if len(pattern) > MAX_PATTERN_LENGTH:
        raise RegexLabError(f"Pattern exceeds {MAX_PATTERN_LENGTH} characters.")
    try:
        return re.compile(pattern, parse_flags(flags))
    except re.error as exc:
        raise RegexLabError(f"Invalid regular expression: {exc}") from exc


def validate_text(text: str) -> None:
    if len(text) > MAX_TEXT_LENGTH:
        raise RegexLabError(f"Input exceeds {MAX_TEXT_LENGTH} characters.")


def find_matches(pattern: str, text: str, flags: str = "", limit: int = 100) -> list[MatchResult]:
    validate_text(text)
    if limit < 1 or limit > 10_000:
        raise RegexLabError("Limit must be between 1 and 10000.")
    rx = compile_pattern(pattern, flags)
    results: list[MatchResult] = []
    for match in rx.finditer(text):
        results.append(MatchResult(match.group(0), match.start(), match.end(), match.groups(), match.groupdict()))
        if len(results) >= limit:
            break
    return results


def full_match(pattern: str, text: str, flags: str = "") -> MatchResult | None:
    validate_text(text)
    match = compile_pattern(pattern, flags).fullmatch(text)
    if not match:
        return None
    return MatchResult(match.group(0), match.start(), match.end(), match.groups(), match.groupdict())


def replace(pattern: str, text: str, replacement: str, flags: str = "", count: int = 0) -> tuple[str, int]:
    validate_text(text)
    if count < 0:
        raise RegexLabError("Count must be zero or greater.")
    try:
        return compile_pattern(pattern, flags).subn(replacement, text, count=count)
    except re.error as exc:
        raise RegexLabError(f"Invalid replacement: {exc}") from exc


def split(pattern: str, text: str, flags: str = "", maxsplit: int = 0) -> list[str]:
    validate_text(text)
    if maxsplit < 0:
        raise RegexLabError("maxsplit must be zero or greater.")
    return compile_pattern(pattern, flags).split(text, maxsplit=maxsplit)


def pattern_info(pattern: str, flags: str = "") -> dict:
    rx = compile_pattern(pattern, flags)
    return {
        "pattern": rx.pattern,
        "flags": flags,
        "groups": rx.groups,
        "named_groups": dict(rx.groupindex),
    }
