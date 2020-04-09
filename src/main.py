from fastapi import FastAPI

from .models.health_check import HealthCheckResponse
from .models.route import FoundRouteResponse, FindRouteRequest

app = FastAPI()


@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    return {"status": "OK"}


@app.post("/find_route", response_model=FoundRouteResponse)
async def find_route(request: FindRouteRequest):
    return {}
