from http import HTTPStatus
from json import JSONDecodeError

import httpx
from client_module.src.services.requests_client.requests_schema import ResponseSchema


class RequestsClient:

    @staticmethod
    def post(url: str, data: dict | None) -> ResponseSchema:
        response = httpx.post(url, json=data)
        return ResponseSchema(status_code=HTTPStatus(response.status_code))

    @staticmethod
    def delete(url: str, data: dict | None) -> ResponseSchema:
        # Using request method because HTTPX lib doesn't support body arguments with 'delete' method
        response = httpx.request(method="DELETE", url=url, json=data)
        return ResponseSchema(status_code=HTTPStatus(response.status_code))

    @staticmethod
    def get(url: str) -> ResponseSchema:
        response = httpx.get(url)
        try:
            data = response.json()
        except JSONDecodeError:
            data = None

        return ResponseSchema(status_code=HTTPStatus(response.status_code), data=data)
