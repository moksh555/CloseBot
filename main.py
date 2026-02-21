from src.app.api.v1.router import mainApiRouter
from fastapi import FastAPI #type: ignore
from src.app.schemas.healthCheckSchemas import healthCheckResponse

APP_VERSION = "1.0.0:v1"

app = FastAPI(
    title="agentMicroservice",
    version = APP_VERSION
)

app.include_router(mainApiRouter, prefix="/agents")

@app.get("/")
def root() -> healthCheckResponse:
    return healthCheckResponse(status = "Live", message="Your app is Live and running")
