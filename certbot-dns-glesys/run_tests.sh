#!/bin/bash

set -euo pipefail

cd /certbot-dns-glesys
python -m pytest
