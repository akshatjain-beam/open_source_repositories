#!/bin/bash

set -euo pipefail

cd /app
# Todo: Add the test command to run the tests. Copy the run test command from Dockerfile
go test -v ./schema