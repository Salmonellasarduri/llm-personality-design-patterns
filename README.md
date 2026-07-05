# LLM Personality Design Patterns

> 日本語README: [README.ja.md](README.ja.md)

Reusable design patterns for building long-running LLM agents that can evolve through experience while maintaining a stable core identity.

This repository contains an **initial set** of reusable design patterns extracted from one long-running agent system.

They should currently be read as **reusable hypotheses and implementation patterns**, not as fully generalized results.

This repository does **not** contain the full source code of INANNA.  
It publishes the **reusable patterns, templates, and minimal implementation ideas** extracted from that project.

## Who this is for

This repository is for developers building:

- AI companions
- AITubers or character-driven assistants
- long-running conversational agents
- systems that need both **consistency** and **controlled change**

## What this repository contains

The focus is not “how to imitate a fixed character,” but how to design an agent that can:

- keep core values stable
- change gradually through experience
- avoid uncontrolled drift
- decide when deeper thinking is needed

## Patterns

| Pattern | Problem it solves | Docs |
|---------|-------------------|------|
| **Four-Layer Personality** | Consistency vs. evolution trade-off | [four-layer-personality.md](four-layer-personality.md) |
| **Drift-Crystallization** | Controlling the rate of personality change | [drift-crystallization.md](drift-crystallization.md) |
| **Gamma Dispatch** | Agent-driven thought depth selection | [gamma-dispatch.md](gamma-dispatch.md) |

## Pattern dependencies

| Pattern | Can be used alone? | Depends on | Recommended order |
|---|---|---|---|
| **Four-Layer Personality** | Yes | none | 1 |
| **Drift-Crystallization** | Partly | works best with a mutable Narrative-like layer | 2 |
| **Gamma Dispatch** | Yes | none | 3 |
| **Expression Layer** | Partly | works best with Four-Layer Personality | 2-3 |

### Dependency notes

- **Four-Layer Personality** is the best starting point if you want both stability and controlled change.
- **Drift-Crystallization** can be adapted independently, but works best when your system already has a mutable long-term layer such as Narrative.
- **Gamma Dispatch** can be introduced on its own in systems that already support multi-stage responses.
- **Expression Layer** is conceptually separate, but becomes more useful when value-level identity and style-level behavior are already separated.

## Field Notes (2026-07)

The source system has kept running since the initial extraction. Four more patterns have been battle-tested over ~4 months of continuous operation and are being distilled into pattern documents:

| Pattern (working name) | Problem it solves | Status |
|---|---|---|
| **Dialogue Resilience** | Hostile or existential interrogation ("you're just a program") destabilizes the persona | Keeps identity stable by shifting the *phase* of the response, not the values. Staged rollout in operation |
| **Recall-only Imprint Layer** | Negative experiences (wounds, rage, boundaries) either get sanitized away or contaminate self-definition | A memory layer that can be recalled but never feeds back into the self-model. In operation |
| **Memory Mis-attribution Guard** | A fake conversation log shown to the agent becomes a "lived" memory | Attribution rules injected into all summarization prompts: quotable evidence outranks semantic plausibility. In operation |
| **Behavioral Regression Testing** | Any change to personality definitions can silently break identity constraints | After each change, a blank-context agent speaks as the persona and hard constitution constraints are checked until 2 consecutive passes. In daily use |

These will land as full pattern documents as they stabilize. The operating notes behind them are published on [Zenn](https://zenn.dev/nabaaatee).

## Quick Start

Minimal runnable examples are available in the [`examples/`](examples/) directory.

1. Copy [`examples/constitution-template.yaml`](examples/constitution-template.yaml)
2. Define your agent’s non-negotiable core values
3. Pick the pattern(s) relevant to your use case
4. Start from the minimal config / pseudocode in each pattern document

Each pattern document includes:

- the problem it addresses
- the design idea
- a minimal configuration
- pseudocode or implementation guidance

## Repository Scope

This repository is intentionally scoped to **patterns and templates**.

It includes:

- design documents
- reusable templates
- pseudocode / minimal implementation ideas
- pattern-level explanations

It does **not** include:

- the entire private codebase of INANNA
- all runtime infrastructure
- private conversation logs
- project-specific secrets or deployment details

## Context

These patterns were extracted from **INANNA**, an autonomous agent designed for long-term dialogue, narrative memory, and controlled personality change.

In the first observation window (2026-03):

- 14+ days of operation
- 1,200+ conversation records
- repeated nightly mutation
- no crystallization event triggered yet

As of 2026-07 the system has been in continuous operation for 4+ months; the newer patterns listed in [Field Notes](#field-notes-2026-07) come from that longer window.

The accompanying technical article (Japanese) explains the design rationale and observations in more detail:

- **Zenn article (Japanese)**: https://zenn.dev/nabaaatee/articles/b4e90b7ef39026

## Design Principles

Across the patterns in this repository, the recurring principles are:

- **Narrative-first personality** rather than flat numeric traits
- **Stable core + mutable layers** instead of all-or-nothing updates
- **Controlled change** rather than unrestricted drift
- **Agent-driven cognition** where possible, instead of routing everything externally

## Suggested Reading Order

If you are new to the project, a good order is:

1. **Four-Layer Personality**
2. **Drift-Crystallization**
3. **Gamma Dispatch**
4. `examples/constitution-template.yaml`

## License

[MIT](LICENSE)
