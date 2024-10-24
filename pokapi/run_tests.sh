#!/bin/bash

set -euo pipefail

cd /pokapi
python -m pytest tests/
