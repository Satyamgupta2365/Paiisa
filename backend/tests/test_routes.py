import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_offers_crud(client):
    res = await client.post("/api/v1/offers", json={
        "payment_method": "UPI",
        "cashback_percentage": 5.0
    })
    assert res.status_code == 201
    offer_id = res.json()["id"]

    res = await client.get("/api/v1/offers")
    assert len(res.json()) == 1
    
    res = await client.delete(f"/api/v1/offers/{offer_id}")
    assert res.status_code == 204

@pytest.mark.asyncio
async def test_user_creation(client):
    res = await client.post("/api/v1/users", json={
        "name": "Test",
        "email": "test@test.com"
    })
    assert res.status_code == 201
    
    res2 = await client.post("/api/v1/users", json={
        "name": "Test2",
        "email": "test@test.com"
    })
    assert res2.status_code == 409

@pytest.mark.asyncio
@patch('services.payment_service.pine_labs_service.initiate_payment')
async def test_process_payment(mock_initiate, client):
    mock_initiate.return_value = {"status": "SUCCESS", "txnId": "12345"}
    
    user_res = await client.post("/api/v1/users", json={"name": "P", "email": "p@p.com"})
    user_id = user_res.json()["id"]
    
    res = await client.post("/api/v1/process-payment", json={
        "user_id": user_id,
        "amount": 100,
        "payment_method": "UPI",
        "category": "food"
    })
    
    assert res.status_code == 200
    assert res.json()["status"] == "success"
    
    insights = await client.get(f"/api/v1/users/{user_id}/insights")
    assert insights.status_code == 200
    assert insights.json()["total_spent"] == 100
