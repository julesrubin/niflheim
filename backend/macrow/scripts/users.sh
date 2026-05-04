#!/usr/bin/env bash
# Smoke: /users/me lazy-create + PATCH semantics.
# Specifically guards: explicit-null in PATCH must NOT overwrite existing fields
# (regression for the BLOCKER #4 fix).
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

section "GET /users/me (lazy-create on first hit)"
req GET /users/me
expect_status 200
echo "$BODY" | jq .

section "PATCH /users/me with real fields"
req PATCH /users/me '{"name":"Smoke Test","calorieGoal":2400}'
expect_status 200
echo "$BODY" | jq .
NAME_BEFORE=$(echo "$BODY" | jq -r .name)
GOAL_BEFORE=$(echo "$BODY" | jq -r .calorieGoal)
[ "$NAME_BEFORE" = "Smoke Test" ] || fail "name was not set to 'Smoke Test'"
[ "$GOAL_BEFORE" = "2400" ]       || fail "calorieGoal was not set to 2400"

section "PATCH /users/me with explicit nulls (must be a no-op)"
req PATCH /users/me '{"name":null,"regime":null,"calorieGoal":null}'
expect_status 200
NAME_AFTER=$(echo "$BODY" | jq -r .name)
GOAL_AFTER=$(echo "$BODY" | jq -r .calorieGoal)
[ "$NAME_AFTER" = "$NAME_BEFORE" ] || fail "name was overwritten by null"
[ "$GOAL_AFTER" = "$GOAL_BEFORE" ] || fail "calorieGoal was overwritten by null"
pass "explicit-null PATCH preserved both fields"

pass "users smoke OK"
