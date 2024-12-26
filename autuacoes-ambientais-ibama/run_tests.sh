#!/bin/bash

set -euo pipefail

cd /autuacoes-ambientais-ibama
python -m pytest tests/
