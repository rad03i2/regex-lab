from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .core import RegexLabError, find_matches, full_match, pattern_info, replace, split

VERSION = "1.0.0"

def _read_text(args: argparse.Namespace) -> str:
    if getattr(args, "file", None):
        try:
            return Path(args.file).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise RegexLabError(f"Cannot read input file: {exc}") from exc
    if getattr(args, "text", None) is not None:
        return args.text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise RegexLabError("Provide --text, --file, or pipe UTF-8 text on stdin.")

def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("pattern", help="Python regular expression")
    parser.add_argument("--flags", default="", help="Regex flags: i,m,s,x,a")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="Input text")
    source.add_argument("--file", help="UTF-8 input file")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="regex-lab", description="Local regular-expression workbench")
    parser.add_argument("--version", action="version", version=f"Regex Lab {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = parser.add_subparsers(dest="command", required=True)

    find = sub.add_parser("find", help="Find non-overlapping matches")
    _common(find); find.add_argument("--limit", type=int, default=100); find.add_argument("--json", action="store_true")
    full = sub.add_parser("fullmatch", help="Require the whole input to match")
    _common(full); full.add_argument("--json", action="store_true")
    repl = sub.add_parser("replace", help="Replace matches")
    _common(repl); repl.add_argument("replacement"); repl.add_argument("--count", type=int, default=0); repl.add_argument("--output"); repl.add_argument("--force", action="store_true")
    spl = sub.add_parser("split", help="Split input around matches")
    _common(spl); spl.add_argument("--maxsplit", type=int, default=0); spl.add_argument("--json", action="store_true")
    info = sub.add_parser("info", help="Inspect groups and named groups")
    info.add_argument("pattern"); info.add_argument("--flags", default=""); info.add_argument("--json", action="store_true")
    return parser

def _write_output(value: str, output: str | None, force: bool) -> None:
    if not output:
        print(value, end="" if value.endswith("\n") else "\n"); return
    path = Path(output)
    if path.exists() and not force:
        raise RegexLabError(f"Output already exists: {path}. Use --force to overwrite.")
    try:
        path.write_text(value, encoding="utf-8")
    except OSError as exc:
        raise RegexLabError(f"Cannot write output file: {exc}") from exc

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "info":
            data = pattern_info(args.pattern, args.flags)
            print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else f"Groups: {data['groups']}\nNamed groups: {data['named_groups']}")
            return 0
        text = _read_text(args)
        if args.command == "find":
            matches = find_matches(args.pattern, text, args.flags, args.limit)
            if args.json:
                print(json.dumps([m.to_dict() for m in matches], ensure_ascii=False, indent=2))
            else:
                for index, m in enumerate(matches, 1): print(f"{index}: [{m.start}:{m.end}] {m.value!r}")
            return 0 if matches else 1
        if args.command == "fullmatch":
            match = full_match(args.pattern, text, args.flags)
            if args.json: print(json.dumps(match.to_dict() if match else None, ensure_ascii=False, indent=2))
            else: print("MATCH" if match else "NO MATCH")
            return 0 if match else 1
        if args.command == "replace":
            result, count = replace(args.pattern, text, args.replacement, args.flags, args.count)
            _write_output(result, args.output, args.force)
            if args.output: print(f"Replaced {count} occurrence(s).", file=sys.stderr)
            return 0
        if args.command == "split":
            parts = split(args.pattern, text, args.flags, args.maxsplit)
            print(json.dumps(parts, ensure_ascii=False, indent=2) if args.json else "\n".join(parts))
            return 0
        return 2
    except RegexLabError as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
