#!/bin/bash

set -euo pipefail

cd /dragonfly-uwg
python -m pytest tests/
