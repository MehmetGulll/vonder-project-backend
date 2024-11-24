import pytest


@pytest.mark.asyncio
async def test_health_check(test_client):
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_products(test_client):
    response = await test_client.get("/products?limit=5&offset=0")
    assert response.status_code == 200
    assert "data" in response.json()  


@pytest.mark.asyncio
async def test_get_product_not_found(test_client):
    response = await test_client.get("/product/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
