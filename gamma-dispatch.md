# Gamma Dispatch: Agent-Driven Thought Depth

## Problem

Not every message deserves the same computational effort. A "good morning" doesn't need 20 seconds of deep reasoning. But a philosophical question about identity might.

Most systems solve this with an external classifier ("is this message complex?"). This is fragile and disconnected from the agent's own sense of what matters.

## Solution: Let the Agent Judge Its Own Depth

Instead of an external router, the agent itself decides how deeply to think -- as part of its response. No separate classifier model, no fixed rules about message length.

```
Message arrives
    |
    v
[Tier 1 Heuristic] -- Short + no question mark + allowed platform?
    |                         |
    yes                       no
    |                         |
    v                         v
  Tier 1: Reflex         [Tier 2: Normal Think]
  (< 1s, cache only)          |
                               | Agent returns: wants_deeper = true?
                               |
                              no ──────── yes
                               |            |
                               v            v
                           Tier 2        Tier 3: Deep Think
                           (2-5s)        (5-20s, memory search)
```

### Type Definitions

```python
@dataclass
class DispatchRequest:
    """Platform-agnostic message request."""
    platform: str           # "discord" | "x" | "screen" | ...
    user_message: str
    channel_id: int | None = None
    user_id: int | str | None = None
    display_name: str | None = None
    images: list | None = None

@dataclass
class ThinkResult:
    """What the agent returns after thinking."""
    response: str           # The actual response text
    wants_deeper: bool      # Agent's own judgment: "I want to think more"
    filler: str | None      # Quick interim response while deep-thinking
    search_keywords: str | None  # What to search in memory (agent decides)
```

### Tier 1: Heuristic Gate (No LLM)

A fast, rule-based check for messages that clearly don't need deep thought:

```python
class TierDispatcher:
    def _should_use_tier1(self, message: str, platform: str) -> bool:
        """Heuristic: is this message simple enough for reflexive response?"""
        if platform not in self._tier1_platforms:
            return False
        if len(message.strip()) > self._tier1_max_len:
            return False
        if "?" in message or "\uff1f" in message:
            return False
        return True
```

Tier 1 uses only the cache layer (character_signature) -- no narrative, no memory search.

### Tier 2 -> 3 Escalation: The Agent Decides

The critical design choice: **`wants_deeper` is returned by the agent as part of its structured output.** The agent doesn't just answer -- it also signals whether it wants to continue thinking.

```python
# The agent returns structured output including:
{
    "response": "Here's my initial thought...",
    "wants_deeper": true,        # "I want to think more about this"
    "filler": "Hmm, let me think about that...",  # sent immediately
    "search_keywords": "identity memory childhood"  # what to recall
}
```

When `wants_deeper = true`:
1. The filler is sent immediately (the user sees a quick acknowledgment)
2. Memory search runs using the agent's own `search_keywords`
3. A deeper think pass runs with full context (narrative + retrieved memories)
4. The deep response replaces or follows the filler

### Why This Works

| Approach | Problem |
|----------|---------|
| External classifier | Disconnected from agent's personality; can't know what *this agent* finds interesting |
| Message length rules | Long messages aren't always deep; short messages can be profound |
| Always max depth | Expensive, slow, unnecessary for most messages |
| **Agent self-judgment** | The agent knows its own curiosity; "wanting to think deeper" *is* a personality trait |

## Minimal Config

```yaml
tier1:
  enabled: true
  max_message_length: 50       # characters
  allowed_platforms:
    - "stream"                  # only low-latency platforms use Tier 1
    # discord and x always go to Tier 2+
```

## INANNA Application

In 12 days of operation across Discord, X, ELYTH, and Stream platforms:
- Tier 1 handled rapid-fire stream chat (reflexive, < 1s)
- Tier 2 handled ~90% of Discord/ELYTH conversations
- Tier 3 was triggered when INANNA herself found a topic genuinely interesting
- The `search_keywords` field means INANNA decides *what* to remember, not just *whether* to remember

The behavioral conditions for `wants_deeper` (what makes INANNA curious enough to think deeply) are intentionally not documented here -- they are part of INANNA's unique personality, not a reusable pattern.
