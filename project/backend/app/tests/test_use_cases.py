import pytest
from app.application.use_cases.get_product import get_product_by_id


@pytest.mark.asyncio
async def test_get_product_by_id_found(mocker):

    mocker.patch(
        "app.infrastructure.database.database_adapter.async_get_product_from_db",
        return_value={"id": "test-id", "name": "Test Product", "price": 10.0, "description": "Test", "photos": []},
    )

    product = await get_product_by_id("test-id")
    assert product["id"] == "test-id"
    assert product["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(mocker):

    mocker.patch(
        "app.infrastructure.database.database_adapter.async_get_product_from_db",
        return_value=None,
    )

    product = await get_product_by_id("nonexistent-id")
    assert "error" in product
