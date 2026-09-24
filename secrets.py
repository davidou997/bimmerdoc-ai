import os
import boto3
import json
from botocore.exceptions import ClientError

def load_aws_secrets():
    """
    Fetches the OpenAI API key from AWS Secrets Manager and injects 
    it into the local environment variables at runtime.
    """
    secret_name = "bimmerdoc/openai-key"
    region_name = "us-east-1" # Update to match your AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(f"Failed to fetch secret: {e}")
        raise e

    # Parse the secret string
    secret = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret)

    # Inject into environment variables for langchain-openai to use
    os.environ["OPENAI_API_KEY"] = secret_dict["OPENAI_API_KEY"]
    print("Successfully loaded AWS secrets into environment.")