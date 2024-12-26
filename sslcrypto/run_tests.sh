#!/bin/bash

set -euo pipefail

cd /sslcrypto
python -m pytest test/
