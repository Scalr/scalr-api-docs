#!/usr/bin/env python
#coding:utf-8
import json
import importlib

import requests
import requests.auth

from api.client import ScalrApiClient


def main(credentials_file, scenario):
    # Setup credentials
    with open(credentials_file) as f:
        creds = json.load(f)
        api_url, api_key_id, api_key_secret, env_id, basic_auth_username, basic_auth_password = \
                [creds.get(k, "") for k in ["api_url", "api_key_id", "api_key_secret", "env_id", "basic_auth_username", "basic_auth_password"]]

    client = ScalrApiClient(api_url.rstrip("/"), api_key_id, api_key_secret)
    client.session.auth = requests.auth.HTTPBasicAuth(basic_auth_username, basic_auth_password)

    # Load scenario
    mod = importlib.import_module(".".join(["scenarii", scenario]))
    mod.execute(client, env_id)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("credentials", help="Path to credentials file")
    parser.add_argument("scenario", help="Name of the scenario to execute")

    ns = parser.parse_args()
    main(ns.credentials, ns.scenario)

