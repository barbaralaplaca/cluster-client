import logging
from http import HTTPStatus

from client_module.src.services.requests_client.requests_client import RequestsClient
from client_module.src.services.requests_client.requests_schema import ResponseSchema


class ClusterClient:
    def __init__(self, base_url: str, nodes: list, client_request: RequestsClient) -> None:
        self._client_request = client_request
        self._base_url = base_url
        self._nodes = nodes

    def create_group(self, group_id: str) -> None:
        logging.info(f"Creating group {group_id} for {self._nodes}")

        successful_requests = []
        for node in self._nodes:
            url = f"{node}{self._base_url}/v1/group/"
            response: ResponseSchema = self._client_request.post(url, data={"groupId": group_id})
            if response.status_code == HTTPStatus.CREATED:
                successful_requests.append(node)

            # Check if group already exists
            elif self._validate_group_id(node, group_id):
                successful_requests.append(node)

            # Rollback
            else:
                logging.warning(
                    f"Failed to create {group_id} for {node}: {response.status_code}: {response.data}. \
                    {group_id} not found in {node}. Rolling back creation of nodes {successful_requests}."
                )
                self._create_group_rollback(successful_requests, group_id)
                break

        logging.info(f"Successfully created group {group_id} for nodes {self._nodes}")

    def delete_group(self, group_id: str) -> None:
        logging.info(f"Deleting group {group_id} for {self._nodes}")

        successful_requests = []
        for node in self._nodes:
            url = f"{node}{self._base_url}/v1/group/"
            response: ResponseSchema = self._client_request.delete(url, data={"groupId": group_id})
            if response.status_code == HTTPStatus.OK:
                successful_requests.append(node)

            # Check if group still exists
            elif self._validate_group_id(node, group_id):
                successful_requests.append(node)

            # Rollback
            else:
                logging.warning(
                    f"Failed to delete {group_id} for {node}: {response.status_code}: {response.data}. \
                    Rolling back deletion of nodes {successful_requests}."
                )
                self._delete_group_rollback(successful_requests, group_id)
                break

        logging.info(f"Successfully deleted group {group_id} for nodes {self._nodes}")

    def get_group(self, node: str, group_id: str) -> dict:
        url = f"{node}{self._base_url}/v1/group/{group_id}/"
        response: ResponseSchema = self._client_request.get(url)

        return response.data

    def _validate_group_id(self, node: str, group_id: str) -> bool:
        response = self.get_group(node, group_id)
        if isinstance(response, dict) and response.get("groupId"):
            return True

        return False

    def _create_group_rollback(self, nodes: list[str], group_id: str) -> None:
        logging.info(f"Rollback: deleting group id {group_id} from nodes: {nodes}")
        for node in nodes:
            url = f"{node}{self._base_url}/v1/group/"
            response: ResponseSchema = self._client_request.delete(url, data={"groupId": group_id})
            if response.status_code == HTTPStatus.OK:
                logging.info(f"{group_id} successfully delete from {node}")
                nodes.remove(node)

            else:
                logging.warning(f"Failed in deleting {group_id} from {node}")

        if len(nodes) == 0:
            logging.info(f"Failed in creating {group_id} for {self._nodes}. Successfully rolled back.")
        else:
            logging.error(f"Failed in creating {group_id} for {self._nodes}. Rollback failed for nodes {nodes}")
            raise RuntimeError

    def _delete_group_rollback(self, nodes: list[str], group_id: str) -> None:
        logging.info(f"Rollback: creating group id {group_id} for nodes: {nodes}")
        for node in nodes:
            url = f"{node}{self._base_url}/v1/group/"
            response: ResponseSchema = self._client_request.post(url, data={"groupId": group_id})
            if response.status_code == HTTPStatus.CREATED:
                logging.info(f"{group_id} successfully created for {node}")
                nodes.remove(node)

            else:
                logging.warning(f"Failed in creating {group_id} for {node}")

        if len(nodes) == 0:
            logging.info(f"Failed in deleting {group_id} for {self._nodes}. Successfully rolled back.")
        else:
            logging.error(f"Failed in deleting {group_id} for {self._nodes}. Rollback failed for nodes {nodes}")
            raise RuntimeError
