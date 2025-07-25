from fastapi import FastAPI
from .routers import items  # Use a relative import to include the router

app = FastAPI()

# Include the router, all routes from `items.py` will be added
app.include_router(items.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}
