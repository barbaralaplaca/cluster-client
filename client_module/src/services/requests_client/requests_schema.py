from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class ResponseSchema:
    status_code: HTTPStatus | None
    data: dict | None = None
