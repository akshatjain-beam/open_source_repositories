#!/bin/bash

set -euo pipefail

cd /py-package-template
python -m pytest tests/
