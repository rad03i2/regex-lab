import test from 'node:test';
import assert from 'node:assert/strict';
import { analyze, compile, findMatches, replaceMatches, splitInput, RegexLabError } from '../src/index.js';

test('finds all matches even when g is not supplied', () => {
  const r = findMatches('\\b\\w{3}\\b', 'one two four six');
  assert.equal(r.count, 3);
  assert.deepEqual(r.matches.map(m => m.value), ['one','two','six']);
});

test('reports captures, named captures and offsets', () => {
  const r = findMatches('(?<key>[a-z]+)=(\\d+)', 'age=42', 'i');
  assert.equal(r.matches[0].index, 0);
  assert.deepEqual(r.matches[0].groups, ['age','42']);
  assert.equal(r.matches[0].namedGroups.key, 'age');
});

test('zero-length expressions terminate safely', () => {
  const r = findMatches('^|$', 'abc', 'm');
  assert.ok(r.count <= 4);
});

test('respects match cap', () => {
  const r = findMatches('.', 'abcdef', '', { maxMatches: 2 });
  assert.equal(r.count, 2); assert.equal(r.truncated, true);
});

test('rejects duplicate and unsupported flags', () => {
  assert.throws(() => compile('a', 'gg'), RegexLabError);
  assert.throws(() => compile('a', 'z'), RegexLabError);
});

test('replace follows JavaScript regex semantics', () => {
  assert.equal(replaceMatches('(\\w+)', 'hello world', '[$1]', 'g'), '[hello] [world]');
});

test('split works with a regex delimiter', () => {
  assert.deepEqual(splitInput('[,;]\\s*', 'a, b;c'), ['a','b','c']);
});

test('analysis warns about nested repetition', () => {
  assert.ok(analyze('(a+)+$').warnings.length > 0);
});

test('invalid regex produces domain error', () => {
  assert.throws(() => compile('['), e => e instanceof RegexLabError && e.code === 'INVALID_REGEX');
});
