#!/usr/bin/env bash
# Smoke: bearer-token guard.
# Hits paths directly with curl (bypassing _lib.sh's auto-injected header) so
# we can assert the negative cases — no header, wrong token, cross-user path.
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

# Helper: run curl with explicit header overrides.
auth_req() {
    local method="$1" path="$2"
    shift 2
    local response
    response=$(curl -sS -w "\n%{http_code}" -X "$method" "$@" "$BASE_URL$path")
    STATUS=$(printf '%s' "$response" | tail -n1)
    BODY=$(printf '%s' "$response" | sed '$d')
}

section "GET /users/$USER_ID without Authorization → 401 UNAUTHENTICATED"
auth_req GET "/users/$USER_ID"
[ "$STATUS" = "401" ] || fail "expected 401, got $STATUS — $BODY"
[ "$(echo "$BODY" | jq -r .error.code)" = "UNAUTHENTICATED" ] \
    || fail "expected error.code=UNAUTHENTICATED, got: $BODY"

section "GET /users/$USER_ID with wrong token → 401 UNAUTHENTICATED"
auth_req GET "/users/$USER_ID" -H "Authorization: Bearer not-the-real-token"
[ "$STATUS" = "401" ] || fail "expected 401, got $STATUS — $BODY"
[ "$(echo "$BODY" | jq -r .error.code)" = "UNAUTHENTICATED" ] \
    || fail "expected error.code=UNAUTHENTICATED, got: $BODY"

section "GET /users/somebody-else with valid token → 403 FORBIDDEN"
auth_req GET "/users/somebody-else" -H "Authorization: Bearer $MACROW_TOKEN"
[ "$STATUS" = "403" ] || fail "expected 403, got $STATUS — $BODY"
[ "$(echo "$BODY" | jq -r .error.code)" = "FORBIDDEN" ] \
    || fail "expected error.code=FORBIDDEN, got: $BODY"

section "GET /foods/3017624010701 without Authorization → 401 (foods is auth-gated too)"
auth_req GET "/foods/3017624010701"
[ "$STATUS" = "401" ] || fail "expected 401 on /foods, got $STATUS — $BODY"

section "GET /health without Authorization → 200 (probe exemption)"
auth_req GET "/health"
[ "$STATUS" = "200" ] || fail "expected 200 on /health, got $STATUS — $BODY"

pass "auth-guard smoke OK"
