from unittest.mock import Mock, patch, MagicMock

import pytest
from client_module.src.main import main as main_method


class TestMain:
    @patch('client_module.src.main.RequestsClient')
    @patch('client_module.src.main.ClusterClient')
    def test_main_create(self, mock_cluster_client_class: Mock, mock_requests_client_class: Mock) -> None:
        # Setting return value of RequestsClient
        mock_requests_instance = MagicMock()
        mock_requests_client_class.return_value = mock_requests_instance

        # Setting return value of ClusterClient
        mock_cluster_instance = MagicMock()
        mock_cluster_client_class.return_value = mock_cluster_instance

        main_method("group id", 'create')

        mock_requests_client_class.assert_called_once()
        mock_cluster_client_class.assert_called_once_with("url", ["node1", "node2"], mock_requests_instance)
        mock_cluster_instance.create_group.assert_called_once_with("group id")

    @patch('client_module.src.main.RequestsClient')
    @patch('client_module.src.main.ClusterClient')
    def test_main_delete(self, mock_cluster_client_class: Mock, mock_requests_client_class: Mock) -> None:
        # Setting return value of RequestsClient
        mock_requests_instance = MagicMock()
        mock_requests_client_class.return_value = mock_requests_instance

        # Setting return value of ClusterClient
        mock_cluster_instance = MagicMock()
        mock_cluster_client_class.return_value = mock_cluster_instance

        main_method("group id", 'delete')

        mock_requests_client_class.assert_called_once()
        mock_cluster_client_class.assert_called_once_with("url", ["node1", "node2"], mock_requests_instance)
        mock_cluster_instance.delete_group.assert_called_once_with("group id")

    @patch('client_module.src.main.RequestsClient')
    @patch('client_module.src.main.ClusterClient')
    def test_wrong_mode(self, mock_cluster_client: Mock, mock_requests_client: Mock) -> None:
        with pytest.raises(ValueError):
            main_method("group id", 'mode')

        mock_requests_client.assert_not_called()
        mock_cluster_client.assert_not_called()

    @patch('client_module.src.main.RequestsClient')
    @patch('client_module.src.main.ClusterClient')
    @patch('client_module.src.main.os.getenv')
    def test_invalid_nodes(self, mock_getenv: Mock, mock_cluster_client: Mock, mock_requests_client: Mock) -> None:
        mock_getenv.side_effect = ["url", ""]
        with pytest.raises(Exception):
            main_method("group id", 'create')

        mock_requests_client.assert_not_called()
        mock_cluster_client.assert_not_called()
