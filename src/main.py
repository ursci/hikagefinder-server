from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
from models.health_check import HealthCheckResponse
from models.route import FoundRouteResponse, FindRouteRequest
from usecases.search_path import search_path

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    return {"status": "OK"}


@app.post("/find_route", response_model=FoundRouteResponse)
async def find_route(request: FindRouteRequest, db: Session = Depends(get_db)):
    result = search_path(db, request.departure_point, request.destination_point, request.departure_time)
    return result
