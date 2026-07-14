# Narrative Mutation: Revise the Story, Not the Constitution

**Evidence status:** `operational`

Let accumulated experience update an agent's first-person self-understanding
without granting the same process authority to rewrite protected identity.

## Context

A durable agent needs more than recent-memory retrieval. It needs a way to say
what an experience changed about its expectations, relationships, or recurring
attention. Putting every conclusion into a flat profile loses the reason behind
the change. Letting a model rewrite its entire persona grants too much authority.

## What this enables

- self-description that develops across sessions;
- explanations for *why* a tendency changed;
- reversible proposals before durable write;
- a protected boundary between interpretation and identity authority.

## Pattern

Keep two separate artifacts:

1. **Constitution:** operator-owned constraints and non-negotiable identity.
2. **Narrative:** agent-authored first-person interpretation of accumulated
   experience.

A mutation cycle proposes a complete Narrative rewrite or a bounded patch. The
proposal passes through a policy gate before it becomes durable.

```text
new experience
    -> reflection candidate
    -> Narrative proposal
    -> Constitution policy gate
        -> accept and version
        -> reject and record the reason
```

The proposal should contain evidence references or a summary of the experiences
that motivated it. A missing Constitution is a fail-closed condition.

## Minimal implementation

```python
def mutate(narrative, experiences, constitution):
    proposal = propose_rewrite(narrative, experiences)
    violations = check_constitution(proposal, constitution)
    if violations:
        return MutationResult(applied=False, violations=violations)
    return versioned_write(proposal)
```

The runnable version is in
[`examples/minimal_operating_architecture.py`](examples/minimal_operating_architecture.py).

## Observability

Record at least:

- proposal identifier and source-experience references;
- policy decision and violated constraint identifiers;
- old/new Narrative hashes;
- write result;
- later behavioral-regression result.

Avoid logging private experience text when hashes and typed references are
sufficient.

## Failure modes

- **Self-flattery loop:** reflection rewards coherent self-praise instead of
  evidence-grounded revision.
- **Cache becomes source of truth:** a lossy runtime summary is rewritten rather
  than the Narrative.
- **Constitution laundering:** a proposal preserves exact words while negating
  their meaning.
- **Unbounded rewrite frequency:** every emotional turn becomes identity change.

Use [Drift-Crystallization](drift-crystallization.md) to control frequency and
[Personality Regression Testing](personality-regression-testing.md) to inspect
the resulting behavior.

## Evidence and limits

The source system has run a nightly reflection/mutation path during 4+ months of
operation. This demonstrates an operating path, not that the resulting
Narrative is objectively better. External reproduction and controlled
comparisons remain open work.
