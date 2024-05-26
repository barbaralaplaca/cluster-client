# Cluster Client

## Overview
This client module interacts with a cluster of nodes to create and delete objects reliably, handling API instability with rollback mechanisms.

## Challenges
- Cluster consists of nodes with identical RESTful APIs.
- Network issues or server errors can occur, necessitating retries and rollbacks.
- Consistency is critical; changes must be fully propagated or fully reverted.

## Approach
- It was decided on a synchronous approach due to the size of this project. 
- It was assumed that the NODES are usually the same. For this reason they are placed as an environment variable, which is more static but still flexible.
- The `group_id` and `action` are considered to be very dynamic. For this reason they are accepted as arguments in docker build.

## Installation
1. Clone the repository
2. Run `cp .env.dist .env` and set the variables.

## Development
1. Create a virtual environment `python3 -m venv .venv` and activate it `. .venv/bin/activate`.
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest`
4. Run pylint: `pylint client_module`
5. To run the container locally: `docker build -t cluster-client . && docker run cluster-client <action> <group-id>`. `<action>` should be replaced with `create` or `delete`.

## Usage
1. In `manifests/deployment.yaml`, first update the container image value, following by updating the container arguments and environment variables with the right values.
2. Run `kubectl apply -f manifests/deployment.yaml`
