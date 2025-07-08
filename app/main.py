from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import auth, orders, catalog

app = FastAPI(
    title="BBC",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="/app/static"), name="static")
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(catalog.router)

@app.get("/")
def ping():
    return {"message": "/docs to access docs"}