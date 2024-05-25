from http import HTTPStatus

import pytest
from pytest_httpx import HTTPXMock

from client_module.src.services.requests_client.requests_client import RequestsClient
from client_module.src.services.requests_client.requests_schema import ResponseSchema


class TestRequestsClient:
    @pytest.fixture(autouse=True)
    def _prepare_test(self):
        self._client = RequestsClient()

    def test_post(self, httpx_mock: HTTPXMock):
        url = "https://test/url"
        data = {"test": "test"}
        httpx_mock.add_response(method="POST", status_code=HTTPStatus.CREATED)

        result: ResponseSchema = self._client.post(url, data)
        assert result.status_code == 201

    def test_delete(self, httpx_mock: HTTPXMock):
        url = "https://test/url"
        data = {"test": "test"}
        httpx_mock.add_response(method="DELETE", status_code=HTTPStatus.OK)

        result: ResponseSchema = self._client.delete(url, data)
        assert result.status_code == 200

    def test_get(self, httpx_mock: HTTPXMock):
        data = {"test": "test"}
        url = "https://test/url"
        httpx_mock.add_response(method="GET", json=data)

        result: ResponseSchema = self._client.get(url)
        assert result.data == data

    def test_get_raises(self, httpx_mock: HTTPXMock):
        url = "https://test/url"
        httpx_mock.add_response(method="GET", status_code=HTTPStatus.NOT_FOUND)

        result: ResponseSchema = self._client.get(url)
        assert result.status_code == 404
        assert result.data is None
