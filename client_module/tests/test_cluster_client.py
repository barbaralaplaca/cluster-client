from http import HTTPStatus
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

import pytest

from client_module.src.cluster_client import ClusterClient
from client_module.src.services.requests_client.requests_schema import ResponseSchema


class TestClusterClient:
    @pytest.fixture(autouse=True)
    def _prepare_test(self) -> None:
        self._nodes = ["node1", "node2", "node3"]
        self._base_url = "example.com"
        self._client_request = Mock()
        self._cluster_client = ClusterClient(self._base_url, self._nodes, self._client_request)

    def test_create_group_happy_path(self) -> None:
        # Group successfully created for all nodes
        self._client_request.post.return_value = ResponseSchema(status_code=HTTPStatus.CREATED)
        self._cluster_client.create_group("test_group")

        self._client_request.post.assert_called()  # Ensure the POST request was made
        self._client_request._validate_group_id.assert_not_called()  # Assert that _validate_group_id was not called
        self._client_request._create_group_rollback.assert_not_called()  # Ensure rollback was not called

    @patch.object(ClusterClient, "_create_group_rollback")
    @patch.object(ClusterClient, "_validate_group_id")
    def test_create_group(self, mock_validate_group_id: Mock, mock_create_group_rollback: Mock) -> None:
        # Try to create group for all nodes
        self._client_request.post.side_effect = [
            ResponseSchema(status_code=HTTPStatus.BAD_REQUEST),  # node1
            ResponseSchema(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),  # node2
        ]
        mock_validate_group_id.side_effect = [True, False]
        self._cluster_client.create_group("test_group")

        # Ensure the request was made for only 2 nodes
        assert self._client_request.post.call_count == 2
        # Assert that _validate_group_id was called for node1 and node2
        mock_validate_group_id.assert_has_calls([call("node1", "test_group"), call("node2", "test_group")])
        # Ensure rollback was called for node1 when node2 fails
        mock_create_group_rollback.assert_called_once_with(["node1"], "test_group")

    def test_delete_group_happy_path(self) -> None:
        # Group successfully deleted for all nodes. The third is never called
        self._client_request.delete.return_value = ResponseSchema(status_code=HTTPStatus.OK)
        self._cluster_client.delete_group("test_group")

        self._client_request.delete.assert_called()  # Ensure the POST request was made
        self._client_request._validate_group_id.assert_not_called()  # Assert that _validate_group_id was not called
        self._client_request._delete_group_rollback.assert_not_called()  # Ensure rollback was not called

    @patch.object(ClusterClient, "_delete_group_rollback")
    @patch.object(ClusterClient, "_validate_group_id")
    def test_delete_group(self, mock_validate_group_id: Mock, mock_delete_group_rollback: Mock) -> None:
        # Try to delete group for all nodes
        self._client_request.post.side_effect = [
            ResponseSchema(status_code=HTTPStatus.BAD_REQUEST),  # node1
            ResponseSchema(status_code=HTTPStatus.INTERNAL_SERVER_ERROR),  # node2
        ]
        mock_validate_group_id.side_effect = [True, False]
        self._cluster_client.delete_group("test_group")

        # Ensure the request was made for only 2 nodes. The third is never called
        assert self._client_request.delete.call_count == 2
        # Assert that _validate_group_id was called for node1 and node2
        mock_validate_group_id.assert_has_calls([call("node1", "test_group"), call("node2", "test_group")])
        # Ensure rollback was called for node1 when node2 fails
        mock_delete_group_rollback.assert_called_once_with(["node1"], "test_group")

    def test_get_group(self) -> None:
        data = {"test": "test"}
        self._client_request.get.return_value = ResponseSchema(status_code=HTTPStatus.OK, data=data)
        result = self._cluster_client.get_group("node1", "test_group")

        assert result == data

    @pytest.mark.parametrize(
        "group_response, group_exists",
        [
            pytest.param({"groupId": "test"}, True, id="Group exists"),
            pytest.param(None, False, id="Group not found"),
        ],
    )
    @patch.object(ClusterClient, "get_group")
    def test_validate_group_id(self, mock_get_group: Mock, group_response: dict | None, group_exists: bool) -> None:
        mock_get_group.return_value = group_response
        result = self._cluster_client._validate_group_id("node1", "test_group")

        assert result == group_exists
