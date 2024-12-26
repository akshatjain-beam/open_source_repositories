#!/bin/bash

set -euo pipefail
cd /grimoirelab-toolkit
python -m pytest tests/
