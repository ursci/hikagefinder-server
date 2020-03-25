from fastapi import FastAPI
from models.health_check import HealthCheckResponse

app = FastAPI()


@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    return {"status": "OK"}
