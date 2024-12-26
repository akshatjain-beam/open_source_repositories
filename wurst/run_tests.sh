#!/bin/bash

set -euo pipefail

cd /wurst
python -m pytest tests/
