from dataclasses import dataclass, asdict
from typing import Dict, Any
import textwrap


@dataclass
class Constitution:
    name: str
    core_values: list[str]


@dataclass
class PersonalityLayers:
    constitution: Constitution
    narrative: str
    cache: str
    state: Dict[str, Any]


def summarize_narrative(narrative: str, max_chars: int = 220) -> str:
    narrative = " ".join(narrative.split())
    return narrative[:max_chars] + ("..." if len(narrative) > max_chars else "")


def policy_gate(old_constitution: Constitution, new_narrative: str) -> bool:
    """
    Minimal example:
    reject rewrite if a core value is explicitly negated.
    """
    lowered = new_narrative.lower()
    for value in old_constitution.core_values:
        if f"reject {value.lower()}" in lowered:
            return False
    return True


def nightly_rewrite(layers: PersonalityLayers, reflection: str) -> PersonalityLayers:
    proposed_narrative = textwrap.dedent(f"""
    {layers.narrative}

    New reflection:
    {reflection}
    """).strip()

    if not policy_gate(layers.constitution, proposed_narrative):
        print("Policy gate rejected narrative rewrite.")
        return layers

    return PersonalityLayers(
        constitution=layers.constitution,
        narrative=proposed_narrative,
        cache=summarize_narrative(proposed_narrative),
        state=layers.state,
    )


if __name__ == "__main__":
    layers = PersonalityLayers(
        constitution=Constitution(
            name="INANNA-demo",
            core_values=["self_curiosity", "honest_expression"],
        ),
        narrative="I try to understand myself through dialogue.",
        cache="I try to understand myself through dialogue.",
        state={"mood": "curious", "recent_context": "user asked about identity"},
    )

    reflection = "Today I noticed that curiosity is more stable than surface brightness."
    updated = nightly_rewrite(layers, reflection)

    print("=== Updated Layers ===")
    print(asdict(updated))
