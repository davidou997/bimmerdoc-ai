import pytest
from pydantic import ValidationError

from schemas import ExtractedEntities


class TestExtractedEntities:
    def test_defaults(self):
        entities = ExtractedEntities()

        assert entities.detected_fault_codes == []
        assert entities.symptom_category is None
        assert entities.operating_condition is None
        assert entities.perceived_location is None

    def test_default_fault_code_lists_are_independent(self):
        first = ExtractedEntities()
        second = ExtractedEntities()

        first.detected_fault_codes.append("P0300")

        assert second.detected_fault_codes == []

    def test_accepts_extracted_values(self):
        entities = ExtractedEntities(
            detected_fault_codes=["P0300", "30FF"],
            symptom_category="rough_idle",
            operating_condition="cold_start",
            perceived_location="engine_bay",
        )

        assert entities.detected_fault_codes == ["P0300", "30FF"]
        assert entities.symptom_category == "rough_idle"
        assert entities.operating_condition == "cold_start"
        assert entities.perceived_location == "engine_bay"

    @pytest.mark.parametrize(
        "values",
        [
            {"detected_fault_codes": "P0300"},
            {"symptom_category": {"invalid": "value"}},
        ],
    )
    def test_rejects_invalid_field_types(self, values):
        with pytest.raises(ValidationError):
            ExtractedEntities(**values)