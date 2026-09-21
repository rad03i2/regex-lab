import pytest
from regex_lab.core import RegexLabError, find_matches, full_match, pattern_info, replace, split


def test_find_matches_with_named_group():
    matches = find_matches(r"(?P<user>[\w.-]+)@(?P<host>[\w.-]+)", "mail a@example.com now")
    assert len(matches) == 1
    assert matches[0].value == "a@example.com"
    assert matches[0].groupdict == {"user": "a", "host": "example.com"}


def test_flags_and_fullmatch():
    assert full_match(r"hello", "HELLO", "i") is not None
    assert full_match(r"hello", "hello!") is None


def test_replace_reports_count():
    value, count = replace(r"\d+", "A12 B34", "#")
    assert value == "A# B#"
    assert count == 2


def test_split_and_info():
    assert split(r"\s*,\s*", "a, b,c") == ["a", "b", "c"]
    info = pattern_info(r"(?P<id>\d+)-(\w+)")
    assert info["groups"] == 2
    assert info["named_groups"] == {"id": 1}


def test_invalid_pattern_becomes_user_error():
    with pytest.raises(RegexLabError, match="Invalid regular expression"):
        find_matches("[", "text")


def test_unknown_flag_rejected():
    with pytest.raises(RegexLabError, match="Unknown flag"):
        find_matches("x", "x", "z")


def test_limits_are_validated():
    with pytest.raises(RegexLabError):
        find_matches("x", "x", limit=0)
