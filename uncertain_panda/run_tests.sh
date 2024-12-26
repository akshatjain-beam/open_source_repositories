#!/bin/bash

set -euo pipefail

cd /uncertain_panda
python -m pytest tests/
