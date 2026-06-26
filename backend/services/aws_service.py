"""
AWS Service — uses boto3 to call Amazon Bedrock (Nova Lite) with temp session credentials.
Falls back gracefully to Groq if AWS is unavailable.
"""
import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from config.settings import settings


class AWSService:
    def __init__(self):
        self._bedrock = None

    def _get_client(self):
        """Lazy-initialize Bedrock client using temp credentials from .env."""
        if self._bedrock is None:
            kwargs = {
                "service_name": "bedrock-runtime",
                "region_name": settings.AWS_REGION,
                "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            }
            if settings.AWS_SESSION_TOKEN:
                kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
            self._bedrock = boto3.client(**kwargs)
        return self._bedrock

    def invoke_model(self, prompt: str, max_tokens: int = 2048) -> str:
        """
        Call Amazon Nova Lite via Bedrock InvokeModel API.
        Returns the generated text, or raises RuntimeError on failure.
        """
        client = self._get_client()
        body = {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "inferenceConfig": {"max_new_tokens": max_tokens}
        }
        try:
            response = client.invoke_model(
                modelId=settings.BEDROCK_MODEL_ID,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
            result = json.loads(response["body"].read())
            # Nova Lite response format
            return result["output"]["message"]["content"][0]["text"]
        except (ClientError, NoCredentialsError) as e:
            raise RuntimeError(f"AWS Bedrock error: {str(e)}")

    def test_connection(self) -> dict:
        """Quick connectivity test — returns status dict."""
        try:
            text = self.invoke_model("Say PAISA_AWS_OK in exactly those words.")
            return {"status": "connected", "response": text, "model": settings.BEDROCK_MODEL_ID}
        except Exception as e:
            return {"status": "error", "detail": str(e)}


aws_service = AWSService()
