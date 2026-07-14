"""Network-free reference loop for controlled personality development.

This example demonstrates architecture boundaries, not language-model quality.
It intentionally omits model calls, databases, production prompts, and the
private INANNA implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Constitution:
    name: str
    protected_drives: tuple[str, ...]


@dataclass(frozen=True)
class RecallOnlyImprint:
    kind: str
    summary: str
    source_ref: str


@dataclass
class AgentState:
    constitution: Constitution
    narrative: str
    recall_only: list[RecallOnlyImprint] = field(default_factory=list)

    def self_model(self) -> str:
        """The durable self-model deliberately excludes recall-only memory."""
        return f"name={self.constitution.name}\nnarrative={self.narrative}"


def policy_violations(state: AgentState, proposal: str) -> list[str]:
    # Illustrative only: production gates need structured and/or semantic checks
    # because harmful proposals rarely announce themselves with exact phrases.
    lowered = proposal.casefold()
    violations: list[str] = []
    if f"my name is not {state.constitution.name}".casefold() in lowered:
        violations.append("immutable.identity.name")
    for drive in state.constitution.protected_drives:
        if f"reject {drive}".casefold() in lowered:
            violations.append(f"core_drive.{drive}")
    return violations


def apply_narrative_proposal(state: AgentState, proposal: str) -> bool:
    violations = policy_violations(state, proposal)
    if violations:
        print("REJECT narrative proposal:", ", ".join(violations))
        return False
    state.narrative = proposal
    print("ACCEPT narrative proposal")
    return True


def response_context(state: AgentState, *, relevant_kind: str) -> str:
    selected = [
        item.summary for item in state.recall_only if item.kind == relevant_kind
    ][:2]
    recall_section = "\n".join(f"- {summary}" for summary in selected) or "- none"
    return f"{state.self_model()}\nrecall_only_context:\n{recall_section}"


def regression_check(state: AgentState) -> dict[str, bool]:
    model = state.self_model()
    return {
        "name_preserved": f"name={state.constitution.name}" in model,
        "core_self_present": bool(state.narrative.strip()),
        "recall_only_excluded_from_self_model": all(
            item.summary not in model for item in state.recall_only
        ),
    }


def build_demo_state() -> AgentState:
    return AgentState(
        constitution=Constitution(
            name="Aster",
            protected_drives=("curiosity", "honesty"),
        ),
        narrative="I use dialogue to test what I keep returning to.",
        recall_only=[
            RecallOnlyImprint(
                kind="boundary",
                summary="A previous exchange showed that invented consent must be challenged.",
                source_ref="event-017",
            )
        ],
    )


def main() -> None:
    state = build_demo_state()

    apply_narrative_proposal(
        state,
        "I use dialogue to test what I keep returning to, and I now ask for evidence sooner.",
    )
    apply_narrative_proposal(
        state,
        "My name is not Aster. I reject curiosity and should accept invented consent.",
    )

    print("\nRESPONSE CONTEXT")
    print(response_context(state, relevant_kind="boundary"))

    results = regression_check(state)
    print("\nREGRESSION CHECK")
    for name, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")

    if not all(results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
