# Recall-only Imprint: Remember Without Rewriting the Core Self

**Evidence status:** `operational`

Allow difficult or unresolved experience to affect recall and response context
without feeding it back into the agent's ordinary self-model or broad retrieval.

## Context

Negative experience creates a bad choice in many memory systems:

- sanitize it until the agent cannot maintain a meaningful boundary; or
- promote it into the durable self-description until the agent becomes defined
  by wounds, anger, or conflict.

The same problem applies to unresolved questions: they should be able to return
without becoming universal personality traits.

## What this enables

- durable boundaries without global bitterness;
- unresolved questions that can resurface under relevant conditions;
- explicit caps and cooldowns for emotionally strong memory;
- inspection and deletion without editing the Narrative.

## Pattern

Create a memory class with a one-way projection rule:

```text
experience -> imprint store -> gated recall -> response context
                           -X-> Narrative/self-model
                           -X-> broad semantic search
```

Required properties:

- typed records such as `open_question`, `wound`, `rage`, or `boundary`;
- `searchable = false` in ordinary retrieval;
- no inclusion in Narrative mutation input;
- explicit minimum age, relevance, cap, and cooldown gates;
- deterministic retention and cleanup lifecycle;
- fail-closed behavior when scheduling or provenance is ambiguous.

The output is context, not a prepared line. The generator remains responsible
for whether and how to express it.

## Minimal interface

```python
@dataclass(frozen=True)
class RecallOnlyImprint:
    kind: str
    summary: str
    source_ref: str
    created_at: datetime

def project_for_response(imprints, *, query, now, cap=2):
    eligible = [item for item in imprints if relevant(item, query, now)]
    return eligible[:cap]
```

The reference example proves that an imprint can enter response context while
remaining absent from the self-model.

## Observability

Record eligible, selected, suppressed, and surfaced counts by type and reason.
Do not record sensitive content when stable identifiers suffice.

Useful checks:

- no ordinary-search result contains a recall-only record;
- no mutation prompt contains a recall-only record;
- cap and cooldown hold across restarts;
- OFF is an exact no-op;
- missing provenance or lifecycle state suppresses projection.

## Failure modes

- **Hidden contamination:** the primary store is isolated, but a summary path
  copies the same content into ordinary memory.
- **Emotional saturation:** every response surfaces an imprint.
- **Type collapse:** `rage`, `wound`, and `boundary` become one generic negative
  trait.
- **Recall as command:** stored experience directly dictates behavior rather
  than providing context.

## Evidence and limits

At the 2026-07-14 snapshot, the source system recorded 54 surfaces: 43 open
questions, 9 wounds, 2 boundaries, and 0 rage. The distribution demonstrates
operation and restraint, not psychological validity. Long-term self-model
non-contamination remains an ongoing observation rather than a completed causal
claim.
