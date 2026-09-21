#!/usr/bin/env node
import fs from 'node:fs';
import process from 'node:process';
import { analyze, findMatches, replaceMatches, splitInput, RegexLabError } from './index.js';

const VERSION = '1.0.0';
const help = `Regex Lab ${VERSION}\n\nUsage:\n  regex-lab test <pattern> [text] [--flags gim] [--file path] [--max N] [--json]\n  regex-lab replace <pattern> <replacement> [text] [--flags g] [--file path]\n  regex-lab split <pattern> [text] [--flags i] [--file path] [--limit N] [--json]\n  regex-lab analyze <pattern> [--flags gim] [--json]\n\nUse --file for UTF-8 input. If text is omitted, stdin is read.\n`;

function parse(argv) {
  const positional = []; const options = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') options.json = true;
    else if (['--flags','--file','--max','--limit'].includes(a)) {
      if (argv[i + 1] === undefined) throw new RegexLabError(`${a} requires a value.`, 'INVALID_ARGUMENT');
      options[a.slice(2)] = argv[++i];
    } else if (a.startsWith('--')) throw new RegexLabError(`Unknown option: ${a}`, 'INVALID_ARGUMENT');
    else positional.push(a);
  }
  return { positional, options };
}

function readInput(text, file) {
  if (file && text !== undefined) throw new RegexLabError('Provide input text or --file, not both.', 'INVALID_ARGUMENT');
  if (file) return fs.readFileSync(file, 'utf8');
  if (text !== undefined) return text;
  if (!process.stdin.isTTY) return fs.readFileSync(0, 'utf8');
  throw new RegexLabError('Input text is required (argument, --file, or stdin).', 'MISSING_INPUT');
}

function print(value, json) {
  if (json || typeof value !== 'string') console.log(JSON.stringify(value, null, 2)); else process.stdout.write(value);
}

try {
  const argv = process.argv.slice(2);
  if (!argv.length || argv.includes('--help') || argv.includes('-h')) { console.log(help); process.exit(0); }
  if (argv.includes('--version') || argv.includes('-v')) { console.log(VERSION); process.exit(0); }
  const command = argv.shift(); const { positional, options } = parse(argv); const flags = options.flags ?? '';
  if (command === 'analyze') {
    if (positional.length !== 1) throw new RegexLabError('analyze requires exactly one pattern.', 'INVALID_ARGUMENT');
    print(analyze(positional[0], flags), true);
  } else if (command === 'test') {
    if (positional.length < 1 || positional.length > 2) throw new RegexLabError('test requires a pattern and optional text.', 'INVALID_ARGUMENT');
    const result = findMatches(positional[0], readInput(positional[1], options.file), flags, { maxMatches: options.max ? Number(options.max) : 1000 });
    print(result, true);
  } else if (command === 'replace') {
    if (positional.length < 2 || positional.length > 3) throw new RegexLabError('replace requires pattern, replacement, and optional text.', 'INVALID_ARGUMENT');
    print(replaceMatches(positional[0], readInput(positional[2], options.file), positional[1], flags), options.json);
  } else if (command === 'split') {
    if (positional.length < 1 || positional.length > 2) throw new RegexLabError('split requires a pattern and optional text.', 'INVALID_ARGUMENT');
    print(splitInput(positional[0], readInput(positional[1], options.file), flags, options.limit === undefined ? undefined : Number(options.limit)), true);
  } else throw new RegexLabError(`Unknown command: ${command}`, 'INVALID_ARGUMENT');
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`regex-lab: ${message}`);
  process.exitCode = error instanceof RegexLabError ? 2 : 1;
}
