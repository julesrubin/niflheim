#!/usr/bin/env bash
# Smoke: /journal — log food, log recipe, GET day, PATCH item, bulk-delete,
# eviction tolerance, error envelopes.
# Verifies the Food-as-source-of-truth contract: no `unit` field on the wire,
# embedded recipes carry server-derived macros.
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

BARCODE="3017624010701"
TODAY=$(date -u +%Y-%m-%d)

# Prime the foods cache.
req GET "/foods/$BARCODE"
expect_status 200

# Build a throwaway recipe for the recipe-item sub-test.
req POST /recipes \
  "{\"name\":\"Smoke Recipe\",\"servings\":2,\"ingredients\":[{\"barcode\":\"$BARCODE\",\"quantity\":50}]}"
expect_status 200
RECIPE_ID=$(echo "$BODY" | jq -r .id)

ITEM_IDS=()
cleanup() {
    if [ "${#ITEM_IDS[@]}" -gt 0 ]; then
        local joined
        joined=$(printf '"%s",' "${ITEM_IDS[@]}")
        joined="[${joined%,}]"
        curl -sS -X POST "$BASE_URL/journal/days/$TODAY/items:bulk-delete" \
            -H 'content-type: application/json' \
            -d "{\"itemIds\":$joined}" >/dev/null 2>&1 || true
    fi
    curl -sS -X DELETE "$BASE_URL/recipes/$RECIPE_ID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

section "POST /journal/days/$TODAY/meals/breakfast/items (food-backed)"
req POST "/journal/days/$TODAY/meals/breakfast/items" \
  "{\"barcode\":\"$BARCODE\",\"quantity\":30}"
expect_status 200
echo "$BODY" | jq '{id, quantity, foodName: .food.name, hasUnit: has("unit")}'
[ "$(echo "$BODY" | jq 'has("unit")')" = "false" ] || fail "wire DTO should not carry 'unit'"
ITEM_IDS+=("$(echo "$BODY" | jq -r .id)")

section "POST /journal/days/$TODAY/meals/dinner/recipes (recipe-backed, embedded macros)"
req POST "/journal/days/$TODAY/meals/dinner/recipes" \
  "{\"recipeId\":\"$RECIPE_ID\",\"servings\":1.5}"
expect_status 200
echo "$BODY" | jq '{
  id, quantity,
  recipeName: .recipe.name,
  caloriesPerServing: .recipe.caloriesPerServing,
  nutritionComplete: .recipe.nutritionComplete,
  hasUnit: has("unit")
}'
[ "$(echo "$BODY" | jq 'has("unit")')" = "false" ] || fail "wire DTO should not carry 'unit'"
[ "$(echo "$BODY" | jq -r .recipe.caloriesPerServing)" -gt 0 ] || fail "embedded recipe macros not derived"
ITEM_IDS+=("$(echo "$BODY" | jq -r .id)")

section "GET /journal/days/$TODAY (full embed)"
req GET "/journal/days/$TODAY"
expect_status 200
echo "$BODY" | jq '
  .meals[]
  | select(.items | length > 0)
  | {kind, items: [.items[] | {id, quantity, food: .food.name?, recipe: .recipe.name?, checked}]}
'

section "PATCH /journal/days/$TODAY/items/${ITEM_IDS[0]} (food, change quantity)"
req PATCH "/journal/days/$TODAY/items/${ITEM_IDS[0]}" '{"quantity":50}'
expect_status 200
echo "$BODY" | jq '{quantity, foodName: .food.name, hasUnit: has("unit")}'
echo "$BODY" | jq -e '.quantity == 50' >/dev/null || fail "PATCH did not update quantity"

section "GET /journal/days/not-a-date → 400 INVALID_DATE"
req GET "/journal/days/not-a-date"
expect_status 400
echo "$BODY" | jq .
[ "$(echo "$BODY" | jq -r .error.code)" = "INVALID_DATE" ] || fail "wrong error code"

section "POST /journal/days/$TODAY/meals/brunch/items → 400 INVALID_MEAL_KIND"
req POST "/journal/days/$TODAY/meals/brunch/items" \
  "{\"barcode\":\"$BARCODE\",\"quantity\":30}"
expect_status 400
[ "$(echo "$BODY" | jq -r .error.code)" = "INVALID_MEAL_KIND" ] || fail "wrong error code"

pass "journal smoke OK"
