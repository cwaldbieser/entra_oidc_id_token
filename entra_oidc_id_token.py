#! /usr/bin/env python

import argparse
import json
import sys

import jwt
import requests


def main(args):
    """
    The main program.
    """
    username = args.username
    password = args.password_file.read().strip()
    client_info = json.load(args.client_info)
    client_id = client_info["client_id"]
    metadata_url = client_info["metadata_url"]
    response = requests.get(metadata_url)
    metadata = response.json()
    token_endpoint = metadata["token_endpoint"]
    # print(f"Token endpoint: {token_endpoint}")
    # print("")
    # print(json.dumps(auth_methods, indent=4))
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "username": username,
        "password": password,
        "scope": "openid profile email",
    }
    response = requests.post(token_endpoint, headers=headers, data=data)
    response_json = response.json()
    # print("")
    # print(json.dumps(response_json, indent=4))
    if "error_codes" in response_json:
        if 7000218 in response_json["error_codes"]:
            print(
                "Must allow public clients in application to use this tool.  "
                "[App Registrations] -> [your app] -> [Authentication] -> "
                "[Settings] -> [Allow Public Client Flows]"
            )
            sys.exit(1)
    id_token = response_json.get("id_token")
    if id_token is None:
        print(json.dumps(response_json, indent=4))
        sys.exit(1)
    decoded = jwt.decode(id_token, options={"verify_signature": False})
    print("")
    print(json.dumps(decoded, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Retrieve the OIDC ID token for an Entra ID application."
    )
    parser.add_argument(
        "client_info",
        action="store",
        type=argparse.FileType("r"),
        help="Path to JSON file containing client information.",
    )
    parser.add_argument(
        "username", action="store", help="Username of the principal to authenticate as."
    )
    parser.add_argument(
        "password_file",
        action="store",
        type=argparse.FileType("r"),
        help="File containing the password of the principal to authenticate as.",
    )
    args = parser.parse_args()
    main(args)
