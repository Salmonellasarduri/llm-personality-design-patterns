from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ThinkResult:
    response: str
    wants_deeper: bool
    filler: Optional[str] = None
    search_keywords: Optional[List[str]] = None


def tier1_heuristic(message: str) -> bool:
    """
    Very simple heuristic:
    short messages without a question mark -> reflex
    """
    return len(message) < 12 and "?" not in message and "？" not in message


def agent_decides_depth(message: str) -> ThinkResult:
    if tier1_heuristic(message):
        return ThinkResult(
            response="おはよう。今日もよろしく。",
            wants_deeper=False,
        )

    if "なぜ" in message or "どうして" in message or "identity" in message.lower():
        return ThinkResult(
            response="考えたい問いだと思う。",
            wants_deeper=True,
            filler="少し考えるね。",
            search_keywords=["identity", "continuity", "self-description"],
        )

    return ThinkResult(
        response="今のところはこう思う。",
        wants_deeper=False,
    )


if __name__ == "__main__":
    messages = [
        "おはよう",
        "なぜ私は変わっても同じ私でいられるの？",
        "今日は元気？",
    ]

    for m in messages:
        result = agent_decides_depth(m)
        print("===")
        print("message:", m)
        print("result:", result)
