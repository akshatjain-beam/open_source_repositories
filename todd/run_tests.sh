#!/bin/bash

set -euo pipefail

cd /todd
python -m pytest tests/
