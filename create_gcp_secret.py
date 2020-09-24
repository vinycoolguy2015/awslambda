#!/usr/bin/env python
# pip3 install google-cloud-secret-manager

import argparse


def create_secret(project_id, secret_id):

    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()

    parent = f"projects/woven-honor-229707"

    # Create the secret.
    response = client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    # Print the new secret name.
    print("Created secret: {}".format(response.name))
    # [END secretmanager_create_secret]

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret to create")
    args = parser.parse_args()

    create_secret(args.project_id, args.secret_id)
