#!/bin/bash

set -euo pipefail

cd /abnf
python -m pytest tests/
