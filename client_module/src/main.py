import logging
import os
import sys

from client_module.src.cluster_client import ClusterClient
from client_module.src.services.requests_client.requests_client import RequestsClient


def main(group_id: str, mode: str) -> None:
    base_url = os.getenv("BASE_URL")
    nodes = os.getenv("NODES")
    if nodes:
        nodes = nodes.split(" ")

        requests_client = RequestsClient()
        cluster_client = ClusterClient(base_url, nodes, requests_client)

        if mode == "create":
            breakpoint()
            cluster_client.create_group(group_id)

        elif mode == "delete":
            cluster_client.delete_group(group_id)

        else:
            logging.warning(f"Mode {mode} non existent. Choose between 'create' or 'delete'.")

    else:
        logging.error("Nodes not available")


if __name__ == '__main__':
    action: str = sys.argv[1]  # 'create' or 'delete'
    group_id: str = sys.argv[2]
    main(group_id, action)


# TODO: manifests
# TODO: Check for time out
