#!/bin/bash

set -euo pipefail

cd /nanomath
python -m pytest python -m pytest nanomath/
