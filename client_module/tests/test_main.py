from unittest.mock import Mock, patch

import pytest
from client_module.src.main import main as main_method


class TestMain:
    @patch('src.main.RequestsClient')
    @patch('src.main.ClusterClient')
    @pytest.fixture
    def _prepare_test(self, mock_cluster_client: Mock, mock_requests_client: Mock) -> None:
        self._cluster_client = mock_cluster_client
        self._requests_client = mock_requests_client

    def test_main_create(self) -> None:
        main_method("group id", 'create')

        self._requests_client.assert_called_once()
        self._cluster_client.assert_called_once_with("url", ["node1", "node2"], self._requests_client)
        self._cluster_client.create_group.assert_called_once_with("group id")

    def test_main_delete(self) -> None:
        main_method("group id", 'delete')

        self._requests_client.assert_called_once()
        self._cluster_client.assert_called_once_with("url", ["node1", "node2"], self._requests_client)
        self._cluster_client.delete_group.assert_called_once_with("group id")

    def test_wrong_mode(self) -> None:
        main_method("group id", 'mode')

        self._requests_client.assert_not_called()
        self._cluster_client.assert_not_called()

    @patch('client_module.src.main.os.getenv')
    def test_invalid_nodes(self, mock_getenv: Mock) -> None:
        mock_getenv.side_effect = ["url", ""]
        main_method("group id", 'create')

        self._requests_client.assert_not_called()
        self._cluster_client.assert_not_called()
