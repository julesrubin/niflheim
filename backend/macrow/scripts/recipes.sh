#!/usr/bin/env bash
# Smoke: recipe CRUD + server-derived per-serving macros.
# Verifies:
#   - POST returns macros computed from ingredient × Food.macro
#   - PATCH (servings 2 → 4) halves the per-serving macros
#   - DELETE is idempotent (204 even on missing id)
#   - GET after DELETE returns 404 RECIPE_NOT_FOUND
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

BARCODE="3017624010701"

# Ensure the food is in the cache before we lean on it for macro derivation.
req GET "/foods/$BARCODE"
expect_status 200

RECIPE_ID=""
cleanup() {
    [ -n "$RECIPE_ID" ] || return 0
    curl -sS -X DELETE \
        -H "Authorization: Bearer $MACROW_TOKEN" \
        "$BASE_URL/users/$USER_ID/recipes/$RECIPE_ID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

section "POST /users/$USER_ID/recipes (servings=2, 50g of Nutella)"
req POST /users/$USER_ID/recipes \
  "{\"name\":\"Smoke Toast\",\"servings\":2,\"emoji\":\"🍞\",\"ingredients\":[{\"barcode\":\"$BARCODE\",\"quantity\":50}]}"
expect_status 200
echo "$BODY" | jq '{id,name,servings,caloriesPerServing,proteinPerServing,carbsPerServing,fatPerServing,nutritionComplete}'
RECIPE_ID=$(echo "$BODY" | jq -r .id)
CAL_2=$(echo "$BODY" | jq -r .caloriesPerServing)
[ "$CAL_2" -gt 0 ] || fail "caloriesPerServing was not derived"
[ "$(echo "$BODY" | jq -r .nutritionComplete)" = "true" ] || fail "nutritionComplete should be true"

section "GET /users/$USER_ID/recipes (list with macros)"
req GET /users/$USER_ID/recipes
expect_status 200
echo "$BODY" | jq '[.[] | {id, name, caloriesPerServing}] | .[0:3]'

section "GET /users/$USER_ID/recipes/$RECIPE_ID (single fetch)"
req GET "/users/$USER_ID/recipes/$RECIPE_ID"
expect_status 200
[ "$(echo "$BODY" | jq -r .id)" = "$RECIPE_ID" ] || fail "wrong id echoed"

section "PATCH /users/$USER_ID/recipes/$RECIPE_ID (servings 2 → 4, macros must halve)"
req PATCH "/users/$USER_ID/recipes/$RECIPE_ID" '{"servings":4}'
expect_status 200
echo "$BODY" | jq '{servings, caloriesPerServing, proteinPerServing, carbsPerServing, fatPerServing}'
CAL_4=$(echo "$BODY" | jq -r .caloriesPerServing)
EXPECTED=$(( CAL_2 / 2 ))
# Allow ±1 for integer rounding.
if [ "$CAL_4" -gt $((EXPECTED + 1)) ] || [ "$CAL_4" -lt $((EXPECTED - 1)) ]; then
    fail "expected caloriesPerServing ≈ $EXPECTED, got $CAL_4"
fi
pass "macros recomputed correctly after servings change"

section "PATCH /users/$USER_ID/recipes/$RECIPE_ID with explicit nulls (must no-op)"
req PATCH "/users/$USER_ID/recipes/$RECIPE_ID" '{"name":null,"emoji":null}'
expect_status 200
[ "$(echo "$BODY" | jq -r .name)" = "Smoke Toast" ] || fail "name was overwritten by null"

section "DELETE /users/$USER_ID/recipes/$RECIPE_ID (twice — must be idempotent)"
req DELETE "/users/$USER_ID/recipes/$RECIPE_ID"
expect_status 204
req DELETE "/users/$USER_ID/recipes/$RECIPE_ID"
expect_status 204

section "GET /users/$USER_ID/recipes/$RECIPE_ID after delete (must 404)"
req GET "/users/$USER_ID/recipes/$RECIPE_ID"
expect_status 404

RECIPE_ID=""  # cleanup no-op
pass "recipes smoke OK"
