#!/bin/bash

set -euo pipefail
cd /chinesestrokesorting
python -m pytest chinese_stroke_sorting/
