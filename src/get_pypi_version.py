"""Extract the python version."""

from __future__ import annotations

import argparse
import json
import ssl
import urllib.request

import packaging.version


def parse_arguments() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pkg_name",
        help="Package to search.",
    )
    parser.add_argument(
        "--github_action_output_name",
        default=None,
        help="Github action output name.",
    )
    return parser.parse_args()


def get_versions(pkg_name: str) -> list[str]:
    """Returns all package versions."""
    # Use PyPI API: https://warehouse.pypa.io/api-reference/json.html
    url = f"https://pypi.python.org/pypi/{pkg_name}/json"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = json.loads(resp.read())

    # Here, we could eventually filter pre-releases,... if required
    versions = list(data["releases"])
    return sorted(versions, key=packaging.version.Version)


def main():
    args = parse_arguments()

    versions = get_versions(args.pkg_name)
    last_version = versions[-1]

    if args.github_action_output_name:
        # Print to propagate the output to the action.
        print(f"::set-output name={args.github_action_output_name}::{last_version}")
    else:
        print(last_version)


if __name__ == "__main__":
    main()
