from pathlib import Path
from regex_lab.cli import main


def test_find_json(capsys):
    code = main(["find", r"\d+", "--text", "x12 y34", "--json"])
    out = capsys.readouterr().out
    assert code == 0
    assert '"value": "12"' in out


def test_find_no_match_returns_one():
    assert main(["find", "z+", "--text", "abc"]) == 1


def test_fullmatch_exit_codes():
    assert main(["fullmatch", r"\d+", "--text", "123"]) == 0
    assert main(["fullmatch", r"\d+", "--text", "x123"]) == 1


def test_replace_file_and_overwrite_protection(tmp_path, capsys):
    output = tmp_path / "out.txt"
    assert main(["replace", r"\d+", "#", "--text", "A12", "--output", str(output)]) == 0
    assert output.read_text(encoding="utf-8") == "A#"
    assert main(["replace", r"\d+", "#", "--text", "B34", "--output", str(output)]) == 2
    assert output.read_text(encoding="utf-8") == "A#"


def test_input_file(tmp_path, capsys):
    source = tmp_path / "in.txt"
    source.write_text("مرحبا 123", encoding="utf-8")
    assert main(["find", r"\d+", "--file", str(source)]) == 0
    assert "123" in capsys.readouterr().out
