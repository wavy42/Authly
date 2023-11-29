from authly.api import api_router
import httpx
import pytest
from fastapi import status


class TestHelloWorld:
    @pytest.mark.asyncio
    async def test_hello_world(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"msg": "Hello World"}

    @pytest.mark.asyncio
    async def test_api_hello_world(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"msg": "Hello World"}

    @pytest.mark.asyncio
    async def test_api_v1_hello_world(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/api/v1/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"msg": "Hello World"}

    @pytest.mark.asyncio
    async def test_api_v1_user_hello_world(
        self, test_client: httpx.AsyncClient
    ):
        response = await test_client.get("/api/v1/user/")

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"msg": "Hello World"}


class TestApiPaths:
    @pytest.mark.asyncio
    async def test_api_paths_dup(self):
        result = api_router.check_api_paths("Test", "Test")
        assert result is False

    @pytest.mark.asyncio
    async def test_api_paths(self):
        result = api_router.check_api_paths("Test", "Test2")
        assert result is True
