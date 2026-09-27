from typing import List, get_type_hints

from state import AgentState


class TestAgentState:
    def test_declares_all_expected_fields_as_required(self):
        expected_fields = {
            "raw_input",
            "detected_fault_codes",
            "symptom_category",
            "operating_condition",
            "perceived_location",
            "retrieved_context",
            "diagnostic_candidates",
            "part_recommendations",
        }

        assert AgentState.__required_keys__ == expected_fields

    def test_declares_expected_field_types(self):
        assert get_type_hints(AgentState) == {
            "raw_input": str,
            "detected_fault_codes": List[str],
            "symptom_category": str | None,
            "operating_condition": str | None,
            "perceived_location": str | None,
            "retrieved_context": List[str],
            "diagnostic_candidates": List[dict],
            "part_recommendations": List[dict],
        }