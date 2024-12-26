#!/bin/bash

set -euo pipefail
cd /delaunay
python -m unittest discover -s tests
