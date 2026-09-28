import json

import pytest
from botocore.exceptions import ClientError

import aws_secrets


class TestLoadAwsSecrets:
    def test_loads_secret_into_environment(self, monkeypatch):
        calls = []

        class FakeSecretsClient:
            def get_secret_value(self, **kwargs):
                calls.append(("get_secret_value", kwargs))
                return {
                    "SecretString": json.dumps(
                        {"OPENAI_API_KEY": "test-api-key"}
                    )
                }

        class FakeSession:
            def client(self, **kwargs):
                calls.append(("client", kwargs))
                return FakeSecretsClient()

        monkeypatch.setattr(aws_secrets.boto3.session, "Session", FakeSession)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        aws_secrets.load_aws_secrets()

        assert calls == [
            (
                "client",
                {"service_name": "secretsmanager", "region_name": "ca-central-1"},
            ),
            ("get_secret_value", {"SecretId": "bimmerdoc/openai-key"}),
        ]
        assert aws_secrets.os.environ["OPENAI_API_KEY"] == "test-api-key"

    def test_propagates_secrets_manager_client_error(self, monkeypatch):
        expected_error = ClientError(
            {"Error": {"Code": "AccessDeniedException", "Message": "denied"}},
            "GetSecretValue",
        )

        class FakeSecretsClient:
            def get_secret_value(self, **kwargs):
                raise expected_error

        class FakeSession:
            def client(self, **kwargs):
                return FakeSecretsClient()

        monkeypatch.setattr(aws_secrets.boto3.session, "Session", FakeSession)

        with pytest.raises(ClientError) as error:
            aws_secrets.load_aws_secrets()

        assert error.value is expected_error