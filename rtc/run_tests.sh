#!/bin/bash

set -euo pipefail
cd /rtc
go test ./schema -v
