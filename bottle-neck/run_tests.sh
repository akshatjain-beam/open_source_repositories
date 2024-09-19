#!/bin/bash

set -euo pipefail
cd /bottle-neck
python -m pytest test/
