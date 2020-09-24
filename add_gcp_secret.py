#!/usr/bin/env python

import argparse


def add_secret_version(project_id, secret_id, payload):

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = client.secret_path(project_id, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode("UTF-8")

    # Add the secret version.
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": payload}}
    )

    # Print the new secret version name.
    print("Added secret version: {}".format(response.name))
    # [END secretmanager_add_secret_version]

    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", help="id of the GCP project")
    parser.add_argument("secret_id", help="id of the secret in which to add")
    parser.add_argument("payload", help="secret material payload")
    args = parser.parse_args()

    add_secret_version(args.project_id, args.secret_id, args.payload)
