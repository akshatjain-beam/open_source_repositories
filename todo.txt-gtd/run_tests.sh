#!/bin/bash

set -euo pipefail
cd /todo_txt_gtd
python -m pytest test/
