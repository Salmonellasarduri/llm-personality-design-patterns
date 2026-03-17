# LLM Personality Design Patterns

Design patterns for building LLM-based autonomous personalities that grow through experience while maintaining core identity.

## Patterns

| Pattern | Problem it solves | Docs |
|---------|------------------|------|
| **Four-Layer Personality** | Consistency vs. evolution trade-off | [four-layer-personality.md](four-layer-personality.md) |
| **Drift-Crystallization** | Controlling rate of personality change | [drift-crystallization.md](drift-crystallization.md) |
| **Gamma Dispatch** | Agent-driven thought depth selection | [gamma-dispatch.md](gamma-dispatch.md) |

## Quick Start

1. Copy [`examples/constitution-template.yaml`](examples/constitution-template.yaml) and fill in your agent's core values
2. Pick the pattern(s) relevant to your use case
3. Each pattern doc includes: Problem, Solution, Minimal Config, and pseudocode

## Context

These patterns were extracted from [INANNA](https://github.com/Salmonellasarduri/Artificial-Personality), an autonomous agent that has been running for 14+ days with 1,200+ conversations. The accompanying technical article (Japanese) will be published on [Zenn](https://zenn.dev/).

## License

[MIT](LICENSE)
