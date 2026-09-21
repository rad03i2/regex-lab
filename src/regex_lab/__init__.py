"""Regex Lab public API."""
from .core import MatchResult, RegexLabError, find_matches, full_match, pattern_info, replace, split

__all__ = ["MatchResult", "RegexLabError", "find_matches", "full_match", "pattern_info", "replace", "split"]
__version__ = "1.0.0"
