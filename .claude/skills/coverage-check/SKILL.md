---
name: coverage-check
description: Cross-check an issue's acceptance criteria (or a PRD section) against the existing test suite to find behaviors that aren't actually tested. Use when user wants to verify regression coverage, check whether acceptance criteria are backed by tests, or find test gaps before/after implementation.
---

# Coverage Check

Find behaviors described in an issue or PRD that have no corresponding test in the suite — without writing any tests yourself. This is a read-only audit; gaps get handed off to `/tdd`.

## When to use

- After an issue's `Status:` moves to `done`, to confirm its acceptance criteria are backed by real tests.
- Before a refactor, to confirm the area you're about to touch has a regression net.
- Periodically across all `done` issues, to catch criteria that were checked off without a matching test.

## Workflow

### 1. Determine scope

Ask the user (or infer from context) what to check:

- A single issue: `.scratch/<feature>/issues/NN-*.md`
- All `done` issues in a feature
- A section of `docs/PRD-v3-consolidated.md`

### 2. Extract expected behaviors

Read the acceptance criteria (`- [ ]` / `- [x]` lines) from the issue, or the relevant behavioral statements from the PRD section. Each becomes one row to check.

### 3. List the existing test suite

Get the full list of test names with their locations:

```
npx vitest list --reporter=json
```

If that's unavailable or too noisy, fall back to grepping `describe(` / `it(` / `test(` strings across `**/*.test.ts`, preserving `describe > it` nesting so each test has a full descriptive path (e.g. `UnlockService.isQuizUnlocked > second quiz unlocked when first is passed`).

### 4. Match criteria to tests

For each acceptance criterion, decide — by semantic match, not string match — whether an existing test's full path plausibly exercises that behavior. A criterion like "İlk Quiz her zaman açık" matches a test named `"first quiz in any phase is always unlocked"` even though no words overlap.

Classify each criterion as:

- **Covered** — a clear matching test exists. Record `file:line`.
- **Not covered** — no test plausibly exercises this behavior.
- **Ambiguous** — a test exists nearby but doesn't clearly assert this specific criterion; explain the gap.

### 5. Flag suspicious checked boxes

If a criterion is checked (`- [x]`) but classified as **not covered** or **ambiguous**, call this out specifically — it means the issue was marked done without a regression test backing it.

### 6. Report

Produce a table:

| Criterion | Status | Test | Notes |
|-----------|--------|------|-------|
| ... | Covered / Not covered / Ambiguous | `path:line` or — | ... |

End with a summary count (covered / not covered / ambiguous) and, for gaps, a one-line suggestion of what behavior a new test should describe — phrased as a test name, not implementation steps, so `/tdd` can pick it up directly.

## Rules

- **Never write or modify test files.** This skill audits; `/tdd` fills gaps.
- **Never modify issue files** beyond what the user explicitly asks (e.g. don't silently uncheck boxes — report the discrepancy and let the user decide).
- Match semantically. Acceptance criteria are written in product language; test names are written in implementation/behavior language. Exact string matching will produce false negatives.
- If `npx vitest list` output is too large, scope it to the test files under the module(s) the issue touches rather than the whole suite.
