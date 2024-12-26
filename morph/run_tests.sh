#!/bin/bash

set -euo pipefail

cd /morph
python -m pytest morph/
