from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


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
    arrival_time: Optional[datetime]
    departure_point: Point
    destination_point: Point


class FoundRouteResponse(BaseModel):
    shortest: GeoJson
    recommended: GeoJson
