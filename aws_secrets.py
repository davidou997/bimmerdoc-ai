import json
import os

import boto3
from botocore.exceptions import ClientError


def load_aws_secrets():
    """Fetch the OpenAI API key from AWS Secrets Manager into the environment."""
    secret_name = "bimmerdoc/openai-key"
    region_name = "ca-central-1"

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as error:
        print(f"Failed to fetch secret: {error}")
        raise

    secret_dict = json.loads(response["SecretString"])
    os.environ["OPENAI_API_KEY"] = secret_dict["OPENAI_API_KEY"]
    print("Successfully loaded AWS secrets into environment.")