import boto3
import json
from config.settings import settings
from botocore.exceptions import BotoCoreError
from database.models import PaymentMethod
from models.schemas import RecommendResponse

class BedrockAIService:
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.model_id = settings.BEDROCK_MODEL_ID

    async def recommend(self, amount, category, options) -> RecommendResponse:
        prompt = self._build_prompt(amount, category, options)
        try:
            raw = self._invoke(prompt)
            return self._parse_response(raw, options)
        except Exception:
            # Fallback if Bedrock is not configured or fails
            return self._parse_response("{}", options)

    def _build_prompt(self, amount, category, options):
        options_text = "\n".join([f"{opt.method.value}: {opt.savings} savings" for opt in options])
        return f"""
Transaction amount: {amount}
Category: {category}

Payment options and savings:
{options_text}

Return ONLY a JSON object with 'recommended_payment' and 'reasoning'. No markdown, no preamble.
"""

    def _invoke(self, prompt):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body
            )
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
        except BotoCoreError as e:
            raise RuntimeError("AI service unavailable") from e

    def _parse_response(self, raw, options):
        best_option = max(options, key=lambda x: x.savings) if options else None
        
        try:
            data = json.loads(raw)
            rec_method_str = data.get("recommended_payment")
            
            rec_method = None
            if rec_method_str:
                for pm in PaymentMethod:
                    if pm.value.lower() == rec_method_str.lower():
                        rec_method = pm
                        break
            
            if not rec_method:
                raise ValueError("Missing or invalid key")

            cashback_amount = 0.0
            for opt in options:
                if opt.method == rec_method:
                    cashback_amount = opt.savings
                    break

            return RecommendResponse(
                recommended_payment=rec_method,
                estimated_savings=cashback_amount,
                cashback_amount=cashback_amount,
                all_options=options,
                reasoning=data.get("reasoning", "Selected optimally.")
            )

        except (json.JSONDecodeError, ValueError):
            return RecommendResponse(
                recommended_payment=best_option.method if best_option else PaymentMethod.UPI,
                estimated_savings=best_option.savings if best_option else 0.0,
                cashback_amount=best_option.savings if best_option else 0.0,
                all_options=options,
                reasoning="Fallback: selected highest savings option."
            )

bedrock_service = BedrockAIService()
