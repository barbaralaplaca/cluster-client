import logging
from http import HTTPStatus

import httpx
from client_module.src.services.requests_client.requests_schema import ResponseSchema


class RequestsClient:

    @staticmethod
    def post(url: str, data: dict | None) -> ResponseSchema:
        try:
            response = httpx.post(url, json=data)
            response.raise_for_status()
            return ResponseSchema(status_code=HTTPStatus(response.status_code))
        except httpx.HTTPStatusError as e:
            logging.warning(f"Error occurred when requesting 'post'-{url}-{data}: {e}")
            return ResponseSchema(status_code=HTTPStatus(e.response.status_code))
        except Exception as e:  # pylint: disable=W0718
            logging.warning(f"Error occurred when requesting 'post'-{url}-{data}: {e}")
            return ResponseSchema(status_code=None)

    @staticmethod
    def delete(url: str, data: dict | None) -> ResponseSchema:
        try:
            # Using request method because HTTPX lib doesn't support body arguments with 'delete' method
            response = httpx.request(method="DELETE", url=url, json=data)
            response.raise_for_status()
            return ResponseSchema(status_code=HTTPStatus(response.status_code))
        except httpx.HTTPStatusError as e:
            logging.warning(f"Error occurred when requesting 'delete'-{url}-{data}: {e}")
            return ResponseSchema(status_code=HTTPStatus(e.response.status_code))
        except Exception as e:  # pylint: disable=W0718
            logging.warning(f"Error occurred when requesting 'delete'-{url}-{data}: {e}")
            return ResponseSchema(status_code=None)

    @staticmethod
    def get(url: str) -> ResponseSchema:
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return ResponseSchema(status_code=HTTPStatus(response.status_code), data=response.json())
        except httpx.HTTPStatusError as e:
            logging.warning(f"Error occurred when requesting 'get'-{url}: {e}")
            return ResponseSchema(status_code=HTTPStatus(e.response.status_code))
        except Exception as e:  # pylint: disable=W0718
            logging.warning(f"Error occurred when requesting 'get'-{url}: {e}")
            return ResponseSchema(status_code=None)
