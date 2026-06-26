import pytest
from services.ai_service import BedrockAIService
from database.models import PaymentMethod
from models.schemas import PaymentOption
import json

def test_parse_response_valid_json():
    service = BedrockAIService.__new__(BedrockAIService)
    options = [PaymentOption(method=PaymentMethod.UPI, cashback=5, savings=50, score=1)]
    raw = json.dumps({"recommended_payment": "UPI", "reasoning": "Test reasoning"})
    
    res = service._parse_response(raw, options)
    assert res.recommended_payment == PaymentMethod.UPI

def test_parse_response_invalid_json():
    service = BedrockAIService.__new__(BedrockAIService)
    options = [
        PaymentOption(method=PaymentMethod.UPI, cashback=3, savings=30, score=0.6),
        PaymentOption(method=PaymentMethod.CREDIT_CARD, cashback=10, savings=100, score=1)
    ]
    raw = "Not a json"
    
    res = service._parse_response(raw, options)
    assert res.recommended_payment == PaymentMethod.CREDIT_CARD # Highest savings
    assert "Fallback" in res.reasoning

def test_build_prompt():
    service = BedrockAIService.__new__(BedrockAIService)
    options = [PaymentOption(method=PaymentMethod.UPI, cashback=5, savings=50, score=1)]
    prompt = service._build_prompt(1000, "electronics", options)
    assert "electronics" in prompt
    assert "1000" in prompt
    assert "UPI: 50.0 savings" in prompt
