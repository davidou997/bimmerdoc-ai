from schemas import ExtractedEntities
from nodes import input_normalizer


class TestInputNormalizerNode:
    def test_loads_secrets_and_invokes_structured_llm(self, monkeypatch):
        events = []
        prompts = []

        extracted = ExtractedEntities(
            detected_fault_codes=["P0300"],
            symptom_category="rough_idle",
            operating_condition="cold_start",
            perceived_location="engine_bay",
        )

        class FakeStructuredLlm:
            def invoke(self, prompt):
                prompts.append(prompt)
                return extracted

        class FakeLlm:
            def with_structured_output(self, schema):
                events.append(("structured_output", schema))
                return FakeStructuredLlm()

        def fake_load_aws_secrets():
            events.append("load_secrets")

        def fake_chat_openai(**kwargs):
            events.append(("construct_llm", kwargs))
            return FakeLlm()

        monkeypatch.setattr(input_normalizer, "llm", None)
        monkeypatch.setattr(
            input_normalizer, "load_dotenv", lambda: events.append("load_dotenv")
        )
        monkeypatch.setattr(
            input_normalizer, "load_aws_secrets", fake_load_aws_secrets
        )
        monkeypatch.setattr(input_normalizer, "ChatOpenAI", fake_chat_openai)

        first_result = input_normalizer.input_normalizer_node(
            {"raw_input": "The engine idles roughly on a cold start"}
        )
        second_result = input_normalizer.input_normalizer_node(
            {"raw_input": "Check engine fault P0300"}
        )

        assert events == [
            "load_dotenv",
            "load_secrets",
            ("construct_llm", {"model": "gpt-4o-mini", "temperature": 0}),
            ("structured_output", ExtractedEntities),
            ("structured_output", ExtractedEntities),
        ]
        assert prompts == [
            "Extract diagnostic parameters from this driver query: "
            "The engine idles roughly on a cold start",
            "Extract diagnostic parameters from this driver query: "
            "Check engine fault P0300",
        ]

        expected_result = {
            "detected_fault_codes": ["P0300"],
            "symptom_category": "rough_idle",
            "operating_condition": "cold_start",
            "perceived_location": "engine_bay",
        }
        assert first_result == expected_result
        assert second_result == expected_result