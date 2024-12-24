#!/bin/bash

set -euo pipefail
cd /chineseflashcards
python -m pytest tests/
