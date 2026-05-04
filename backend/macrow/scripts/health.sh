#!/usr/bin/env bash
# Smoke: GET /health is alive and returns the canonical envelope.
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

section "GET /health"
req GET /health
expect_status 200
echo "$BODY" | jq .

pass "health smoke OK"
