#!/usr/bin/env bash
# Smoke: /users/$USER_ID lazy-create + PATCH semantics.
# Specifically guards: explicit-null in PATCH must NOT overwrite existing fields
# (regression for the BLOCKER #4 fix).
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

section "GET /users/$USER_ID (lazy-create on first hit)"
req GET /users/$USER_ID
expect_status 200
echo "$BODY" | jq .

section "PATCH /users/$USER_ID with real fields"
req PATCH /users/$USER_ID '{"name":"Smoke Test","calorieGoal":2400}'
expect_status 200
echo "$BODY" | jq .
NAME_BEFORE=$(echo "$BODY" | jq -r .name)
GOAL_BEFORE=$(echo "$BODY" | jq -r .calorieGoal)
[ "$NAME_BEFORE" = "Smoke Test" ] || fail "name was not set to 'Smoke Test'"
[ "$GOAL_BEFORE" = "2400" ]       || fail "calorieGoal was not set to 2400"

section "PATCH /users/$USER_ID with explicit nulls (must be a no-op)"
req PATCH /users/$USER_ID '{"name":null,"regime":null,"calorieGoal":null}'
expect_status 200
NAME_AFTER=$(echo "$BODY" | jq -r .name)
GOAL_AFTER=$(echo "$BODY" | jq -r .calorieGoal)
[ "$NAME_AFTER" = "$NAME_BEFORE" ] || fail "name was overwritten by null"
[ "$GOAL_AFTER" = "$GOAL_BEFORE" ] || fail "calorieGoal was overwritten by null"
pass "explicit-null PATCH preserved both fields"

pass "users smoke OK"
