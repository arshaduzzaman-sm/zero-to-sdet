#!/usr/bin/env bash
# Runs once when a GitHub Codespace is created (see devcontainer.json).
# Installs every Python package the project uses; pip checks each one against
# its SHA-256 hash, so nothing unexpected can be installed.
set -euo pipefail

python -m venv .venv
.venv/bin/pip install --quiet --disable-pip-version-check --require-hashes \
  -r requirements-docs.txt -r requirements.txt -r practice-app/requirements.txt

echo "Setup done. The Practice App starts by itself: open the Ports tab, then port 8080."
