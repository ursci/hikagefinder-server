from datetime import datetime
from typing import List, Optional
from fastapi.exceptions import HTTPException

from pydantic import BaseModel, validator


class GeoJsonGeometry(BaseModel):
    type: str
    coordinates: List[List[float]]


class GeoJsonProperty(BaseModel):
    sunlight_rate: float
    total_distance: int
    total_minutes: int


class GeoJsonFeature(BaseModel):
    type: str
    geometry: GeoJsonGeometry
    properties: GeoJsonProperty


class GeoJson(BaseModel):
    type: str
    features: List[GeoJsonFeature]


class Point(BaseModel):
    lat: float
    lon: float


class FindRouteRequest(BaseModel):
    departure_time: Optional[datetime]
    departure_point: Point
    destination_point: Point

    @validator("departure_time")
    def departure_time_validator(value: datetime):
        if 8 <= value.hour <= 18:
            return value
        else:
            return value.replace(hour=8)
            # Temporary fix to return a default route when there is no shade data
            # Uncomment if routes should only returned during day time
            #
            # raise HTTPException(
            #    status_code=422,
            #    detail="Out of service time",
            # )


class FoundRouteResponse(BaseModel):
    shortest: GeoJson
    recommended: GeoJson
