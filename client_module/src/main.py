import os
import sys

import dotenv
from client_module.src.cluster_client import ClusterClient
from client_module.src.services.requests_client.requests_client import RequestsClient


def main(group_id: str, action: str) -> None:
    if action not in ["create", "delete"]:
        raise ValueError(f"Action '{action}' is invalid. Choose between 'create' or 'delete'.")

    dotenv.load_dotenv()
    base_url = os.getenv("BASE_URL")
    nodes = os.getenv("NODES")

    if not nodes:
        raise ValueError("Nodes not available")

    nodes = nodes.split(",")

    requests_client = RequestsClient()
    cluster_client = ClusterClient(base_url, nodes, requests_client)

    if action == "create":
        cluster_client.create_group(group_id)

    elif action == "delete":
        cluster_client.delete_group(group_id)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError("Both ACTION and GROUP_ID must be provided as arguments.")

    action = sys.argv[1]
    group_id = sys.argv[2]

    main(group_id, action)
