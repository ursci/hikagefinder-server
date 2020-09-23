from datetime import datetime
from typing import List, Optional

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
            raise ValueError("Given time is out of service.")


class FoundRouteResponse(BaseModel):
    shortest: GeoJson
    recommended: GeoJson
