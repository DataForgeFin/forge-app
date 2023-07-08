from fastapi import FastAPI

from apps.routers import patients, users

app = FastAPI(
    title="Template API Python",
    version="0.0.1",
)

app.include_router(users.router)
app.include_router(patients.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/health/liveness/")
async def liveness():
    return "alive"


@app.get("/health/readiness/")
async def readiness():
    return "ready"
