#!/usr/bin/env bash
# Smoke: foods barcode lookup + cache prefix search + OFF miss envelope.
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"
require_jq

BARCODE="3017624010701"  # Nutella — well-known, stable test fixture on OFF.

section "GET /foods/$BARCODE (cache hit, or fetch+upsert from OFF)"
req GET "/foods/$BARCODE"
expect_status 200
echo "$BODY" | jq '{barcode,name,brand,baseUnit,calories,protein,carbs,fat}'
[ "$(echo "$BODY" | jq -r .barcode)" = "$BARCODE" ] || fail "wrong barcode echoed"

section "GET /foods/search?q=nut&source=cache (Firestore prefix range)"
req GET "/foods/search?q=nut&source=cache&limit=5"
expect_status 200
echo "$BODY" | jq '{total, sourceBreakdown, sample: ([.items[] | {barcode,name}] | .[0])}'
[ "$(echo "$BODY" | jq '.items | length')" -ge 1 ] || fail "prefix search returned no rows"

section "GET /foods/0000000000001 (genuine OFF miss → 404 BARCODE_NOT_FOUND)"
req GET "/foods/0000000000001"
expect_status 404
echo "$BODY" | jq .
[ "$(echo "$BODY" | jq -r .error.code)" = "BARCODE_NOT_FOUND" ] || fail "wrong error code"

pass "foods smoke OK"
