import pytest
from app.infrastructure.database.database_adapter import async_get_product_from_db, async_save_product_to_db


@pytest.mark.asyncio
async def test_async_get_product_from_db(mocker):

    mocker.patch(
        "app.infrastructure.database.db_connection.get_db_connection",
        return_value=mocker.AsyncMock(),
    )

    product_id = "test-id"
    product = await async_get_product_from_db(product_id)
    assert product is None 


@pytest.mark.asyncio
async def test_async_save_product_to_db(mocker):

    mocker.patch(
        "app.infrastructure.database.db_connection.get_db_connection",
        return_value=mocker.AsyncMock(),
    )

    product = {
        "id": "test-id",
        "name": "Test Product",
        "price": 50.0,
        "description": "Test description",
        "photos": [],
    }
    await async_save_product_to_db(product, "test-vendor")
