# Shared helpers for Macrow smoke scripts.
# Source this from each per-resource script:
#
#   #!/usr/bin/env bash
#   . "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
#
# Required env:
#   MACROW_TOKEN  — bearer token (matches Cloud Run BEARER_TOKEN secret).
# Optional env:
#   MACROW_BASE_URL — defaults to http://127.0.0.1:8000/macrow.
#   USER_ID         — defaults to "me" (matches CURRENT_USER_ID in settings).

set -euo pipefail

BASE_URL="${MACROW_BASE_URL:-http://127.0.0.1:8000/macrow}"
USER_ID="${USER_ID:-me}"

if [ -z "${MACROW_TOKEN:-}" ]; then
    printf "✗ MACROW_TOKEN is required (export it or write it to backend/macrow/.macrow.env)\n" >&2
    exit 2
fi

if [ -t 1 ]; then
    RED=$'\033[0;31m'
    GREEN=$'\033[0;32m'
    YELLOW=$'\033[0;33m'
    NC=$'\033[0m'
else
    RED=""; GREEN=""; YELLOW=""; NC=""
fi

section() { printf "\n%s=== %s ===%s\n" "$YELLOW" "$1" "$NC"; }
pass()    { printf "%s✓ %s%s\n" "$GREEN" "$1" "$NC"; }
fail()    { printf "%s✗ %s%s\n" "$RED" "$1" "$NC" >&2; exit 1; }

# Run a request and capture body + status into BODY and STATUS globals.
# Usage: req METHOD PATH [JSON_BODY]
# Always injects Authorization: Bearer $MACROW_TOKEN.
req() {
    local method="$1" path="$2" data="${3:-}"
    local response
    if [ -n "$data" ]; then
        response=$(curl -sS -w "\n%{http_code}" -X "$method" \
            -H "Authorization: Bearer $MACROW_TOKEN" \
            -H 'content-type: application/json' \
            -d "$data" \
            "$BASE_URL$path")
    else
        response=$(curl -sS -w "\n%{http_code}" -X "$method" \
            -H "Authorization: Bearer $MACROW_TOKEN" \
            "$BASE_URL$path")
    fi
    STATUS=$(printf '%s' "$response" | tail -n1)
    BODY=$(printf '%s' "$response" | sed '$d')
}

expect_status() {
    local expected="$1"
    if [ "$STATUS" != "$expected" ]; then
        fail "Expected HTTP $expected, got $STATUS. Body: $BODY"
    fi
}

require_jq() {
    command -v jq >/dev/null || fail "jq is required (brew install jq)"
}
