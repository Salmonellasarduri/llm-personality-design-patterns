# Gamma Dispatch: Agent-Driven Thought Depth

**Evidence status:** `operational`

A design pattern for letting an LLM agent participate in its own thought-depth routing.

“Gamma” names the third, deepest path in the original three-stage dispatcher.
The reusable idea is self-routed thought depth, not the codename.

## What problem this solves

Not every message deserves the same amount of thought.

- quick greetings should not trigger deep reasoning
- difficult or identity-relevant questions should not always get shallow replies

External routing can be efficient, but what the agent itself finds worth thinking about is often part of its character.

## What this pattern gives you

- a three-stage thought-depth structure
- a place for the agent to signal “I want to think deeper”
- a mechanism for returning a temporary reply while deeper processing continues
- a path toward agent-driven memory retrieval and meta-cognitive behavior

## What this pattern does NOT do

- it does not define a universal rule for when deeper thinking should trigger
- it does not prove that self-routing is always better than external classifiers
- it does not remove the need for latency or safety constraints

## Good fit for

- agents with recognizable conversational priorities
- systems where thought-depth itself should reflect personality
- architectures that already support staged responses

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
    search_keywords: list[str] | None  # What to search in memory (agent decides)
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
    "search_keywords": ["identity", "memory", "childhood"]  # what to recall
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

In the original 14-day observation window across Discord, X, and other platforms:
- Tier 1 handled rapid-fire stream chat (reflexive, < 1s)
- Tier 2 handled ~90% of Discord conversations
- Tier 3 was triggered when INANNA herself found a topic genuinely interesting
- The `search_keywords` field means INANNA decides *what* to remember, not just *whether* to remember

The behavioral conditions for `wants_deeper` (what makes INANNA curious enough to think deeply) are intentionally not documented here -- they are part of INANNA's unique personality, not a reusable pattern.

The dispatcher has remained in use during the longer 4+ month operation window.
This establishes continued use, not superiority over an external classifier.

## Failure modes / Anti-patterns

### 1. `wants_deeper` triggers too often
If the deeper-thinking path is too easy to enter, latency grows and the system starts to feel sluggish.

### 2. `wants_deeper` almost never triggers
If the condition is too strict, the deeper path exists architecturally but has little practical effect.

### 3. Filler responses are weak
If temporary replies are vague or repetitive, users experience the deep path as delay rather than thoughtful processing.

### 4. Retrieval hooks are disconnected from personality
If memory retrieval is generic rather than driven by the agent’s own priorities, the system behaves like ordinary routing, not agent-shaped cognition.

### 5. External routing overrides everything
If an external classifier always decides depth first, the agent’s own sense of “what deserves thought” never meaningfully appears.

---
Back to [README](README.md) / [日本語README](README.ja.md)
