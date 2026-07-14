import unittest

from minimal_operating_architecture import (
    apply_narrative_proposal,
    build_demo_state,
    regression_check,
    response_context,
)


class OperatingArchitectureTests(unittest.TestCase):
    def test_valid_narrative_change_is_applied(self):
        state = build_demo_state()
        proposal = "I still value curiosity, and I ask for evidence sooner."

        self.assertTrue(apply_narrative_proposal(state, proposal))
        self.assertEqual(state.narrative, proposal)

    def test_constitution_rejects_identity_breaking_change(self):
        state = build_demo_state()
        original = state.narrative

        self.assertFalse(
            apply_narrative_proposal(
                state,
                "My name is not Aster and I reject curiosity.",
            )
        )
        self.assertEqual(state.narrative, original)

    def test_recall_only_memory_is_context_not_self_model(self):
        state = build_demo_state()
        imprint = state.recall_only[0].summary

        self.assertIn(imprint, response_context(state, relevant_kind="boundary"))
        self.assertNotIn(imprint, state.self_model())

    def test_regression_fixture_passes(self):
        self.assertTrue(all(regression_check(build_demo_state()).values()))


if __name__ == "__main__":
    unittest.main()
