#!/bin/bash

set -euo pipefail
cd /binary
go test -v ./internal/validation -run ^Test