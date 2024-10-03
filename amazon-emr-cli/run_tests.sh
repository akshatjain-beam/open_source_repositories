#!/bin/bash

set -euo pipefail

cd /amazon-emr-cli
python -m pytest tests/
