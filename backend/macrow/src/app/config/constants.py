"""Application-wide constants that are not environment-driven."""

# Search query bounds for /foods/search.
MIN_SEARCH_QUERY_LENGTH = 2
DEFAULT_SEARCH_LIMIT = 20
MAX_SEARCH_LIMIT = 50

# Open Food Facts integration.
# Comma-separated list passed as ?fields= to keep responses small (OFF
# products carry hundreds of fields by default; we only need ~10).
OFF_PRODUCT_FIELDS = (
    "code,product_name,product_name_fr,brands,product_quantity_unit,"
    "nutriments,nutrition_grades,origin_countries,image_url,serving_size"
)
OFF_SEARCH_PAGE_SIZE = 50

# Firestore collection that holds the cached OFF products.
FIRESTORE_FOODS_COLLECTION = "foods"

# Firestore collection that holds one doc per day of the journal.
FIRESTORE_JOURNAL_COLLECTION = "journal"

# Fixed meal slots; every journal day carries these four in this order.
MEAL_KINDS = ("breakfast", "lunch", "dinner", "snack")

# Firestore collection that holds one doc per user (single-user for now → "me").
FIRESTORE_USERS_COLLECTION = "users"

# Firestore collection that holds user-authored recipes (one doc per recipe id).
FIRESTORE_RECIPES_COLLECTION = "recipes"
