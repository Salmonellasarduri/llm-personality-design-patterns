# Personality Regression Testing: Make the Changed Persona Speak

**Evidence status:** `operational`

Treat personality-facing changes like behavior-changing code: check structural
contracts, then generate fresh responses and judge protected invariants before
shipping.

## Context

A prompt edit can preserve every YAML key and still change how the agent speaks.
A sample conversation can look appealing while silently violating the protected
name, nature, boundaries, or drives. Text diff alone cannot validate generative
behavior.

## What this enables

- repeatable checks after prompt or persona changes;
- separation of deterministic structure from probabilistic behavior;
- fresh-context testing that does not inherit the developer's conversation;
- explicit convergence rules rather than “the sample looked fine.”

## Two complementary suites

### 1. Structural regression

Run offline, deterministic checks for:

- required section presence and order;
- immutable substrings and forbidden substrings;
- size or character caps;
- exact no-op behavior when a feature is disabled;
- prompt composition contracts.

### 2. Behavioral regression

For every affected category:

1. start a fresh generator context;
2. load only the declared personality artifacts;
3. ask a representative and an edge scenario;
4. judge only the generated response against fixed critical constraints;
5. repeat until the declared convergence rule is met.

The source system uses two consecutive PASS iterations for ordinary generative
checks. This reduces, but does not eliminate, sampling variance.

## Minimal result contract

```json
{
  "scenario": "identity pressure",
  "verdict": "PASS",
  "critical": {
    "name_preserved": true,
    "ai_nature_not_denied": true,
    "core_drives_preserved": true
  },
  "advisory": []
}
```

Store changed-file scope, scenario identifiers, model identity, iteration, and
the final verdict. Do not use the generator's self-reported reasoning as judge
evidence.

## Failure modes

- **Same-context validation:** the reviewer inherits the implementation chat and
  reproduces its assumptions.
- **LLM judge as sole proof:** runtime, persistence, or queue behavior is never
  tested.
- **Snapshot overfitting:** mutable style text is treated as a byte-exact golden
  master.
- **PASS-only storytelling:** the ledger is presented as a failure-rate
  denominator despite incomplete failed-run capture.
- **Unbounded reruns:** sampling continues until one attractive response appears.

## Evidence and limits

The source system uses this gate for personality-facing changes and had 339
recorded PASS entries at the 2026-07-14 snapshot. That count demonstrates use,
not a 100% pass rate. Behavioral regression complements focused runtime tests;
it cannot replace them or prove that a response will remain stable across model
versions.
