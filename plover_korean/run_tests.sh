#!/bin/bash

set -euo pipefail

cd /plover_korean
python -m pytest test/
