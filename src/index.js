const MAX_INPUT = 1_000_000;

export class RegexLabError extends Error {
  constructor(message, code = 'REGEX_LAB_ERROR') { super(message); this.name = 'RegexLabError'; this.code = code; }
}

export function compile(pattern, flags = '') {
  if (typeof pattern !== 'string') throw new RegexLabError('Pattern must be a string.', 'INVALID_PATTERN');
  if (typeof flags !== 'string') throw new RegexLabError('Flags must be a string.', 'INVALID_FLAGS');
  if (/[^dgimsuvy]/.test(flags) || new Set(flags).size !== flags.length) throw new RegexLabError(`Invalid or duplicate flags: ${flags}`, 'INVALID_FLAGS');
  try { return new RegExp(pattern, flags); }
  catch (error) { throw new RegexLabError(`Invalid regular expression: ${error.message}`, 'INVALID_REGEX'); }
}

export function analyze(pattern, flags = '') {
  const regex = compile(pattern, flags);
  const warnings = [];
  if (/\([^)]*[+*][^)]*\)[+*{]/.test(pattern)) warnings.push('Nested repetition detected; review for excessive backtracking on untrusted input.');
  if (/\.\*[+*{]/.test(pattern)) warnings.push('A repeated wildcard is followed by another quantifier; review performance.');
  if (pattern.length > 500) warnings.push('Pattern is unusually long; keep complex expressions documented and tested.');
  return { source: regex.source, flags: regex.flags, unicode: regex.unicode, global: regex.global, sticky: regex.sticky, warnings };
}

function assertInput(input) {
  if (typeof input !== 'string') throw new RegexLabError('Input must be a string.', 'INVALID_INPUT');
  if (input.length > MAX_INPUT) throw new RegexLabError(`Input exceeds the ${MAX_INPUT.toLocaleString()} character safety limit.`, 'INPUT_TOO_LARGE');
}

export function findMatches(pattern, input, flags = '', options = {}) {
  assertInput(input);
  const maxMatches = options.maxMatches ?? 1000;
  if (!Number.isInteger(maxMatches) || maxMatches < 1 || maxMatches > 10000) throw new RegexLabError('maxMatches must be an integer from 1 to 10000.', 'INVALID_LIMIT');
  const requested = compile(pattern, flags);
  const scanFlags = requested.global ? requested.flags : `${requested.flags}g`;
  const regex = new RegExp(requested.source, scanFlags);
  const matches = [];
  let match;
  while ((match = regex.exec(input)) !== null && matches.length < maxMatches) {
    matches.push({ value: match[0], index: match.index, end: match.index + match[0].length, groups: match.slice(1), namedGroups: match.groups ?? null });
    if (match[0] === '') regex.lastIndex += 1;
  }
  return { pattern, flags: requested.flags, inputLength: input.length, count: matches.length, truncated: matches.length === maxMatches && regex.exec(input) !== null, matches };
}

export function replaceMatches(pattern, input, replacement, flags = '') {
  assertInput(input);
  if (typeof replacement !== 'string') throw new RegexLabError('Replacement must be a string.', 'INVALID_REPLACEMENT');
  const regex = compile(pattern, flags);
  return input.replace(regex, replacement);
}

export function splitInput(pattern, input, flags = '', limit) {
  assertInput(input);
  const regex = compile(pattern, flags);
  if (limit !== undefined && (!Number.isInteger(limit) || limit < 0 || limit > 10000)) throw new RegexLabError('Split limit must be an integer from 0 to 10000.', 'INVALID_LIMIT');
  return input.split(regex, limit);
}
