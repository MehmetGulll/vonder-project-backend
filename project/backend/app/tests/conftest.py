import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def test_client():
    """
    Test istemcisi için bir fixture.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
