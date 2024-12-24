#!/bin/bash

set -euo pipefail
cd /randomprofilegenerator
python -m pytest tests/
