#!/bin/bash

set -euo pipefail
cd /sthir
python -m pytest sthir/tests/
