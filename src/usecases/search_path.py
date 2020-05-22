from datetime import datetime
import json
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

import schemas
from models.route import Point
from models.route import FoundRouteResponse


RAW_SHORTEST_QUERY = """
SELECT SUM(distance), ST_AsGeoJSON(ST_LineMerge(ST_Union(geom))) 
FROM shortest_fromAtoB(:x1, :y1, :x2, :y2);
""".strip()

RAW_RECOMMENDED_QUERY = """
SELECT SUM(distance), ST_AsGeoJSON(ST_LineMerge(ST_Union(geom)))
FROM shade_fromAtoB(:x1, :y1, :x2, :y2, :depart_at);
""".strip()

WALK_SPEED = 80


def search_path(db: Session, source: Point, destination: Point, departure_time: datetime):
    # Find shortest path
    sql_statement = text(RAW_SHORTEST_QUERY)
    args = {
        "x1": source.lon,
        "y1": source.lat,
        "x2": destination.lon,
        "y2": destination.lat,
    }
    nearest_destination_path = db.execute(sql_statement, args).first()
    # when the result is empty, return empty geojson
    if nearest_destination_path[0] is None:
        dummy = {
            "type": "FeatureCollection",
            "features": [],
        }
        return {"shortest": dummy, "recommended": dummy}
    shortest_distance = nearest_destination_path[0]
    shortest_geojson = json.loads(nearest_destination_path[1])
    shortest = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": shortest_geojson["type"],
                    "coordinates": shortest_geojson["coordinates"],
                },
                "properties": {
                    "shade_rate": 0.0,
                    "total_distance": shortest_distance,
                    "total_minutes": shortest_distance / WALK_SPEED,
                },
            }
        ],
    }
    # Find recommended path
    sql_statement = text(RAW_RECOMMENDED_QUERY)
    args = {
        "x1": source.lon,
        "y1": source.lat,
        "x2": destination.lon,
        "y2": destination.lat,
        "depart_at": departure_time.time().strftime('%H:%M:%S'),
    }
    recommended_destination_path = db.execute(sql_statement, args).first()
    # when the result is empty, return empty geojson
    if recommended_destination_path[0] is None:
        dummy = {
            "type": "FeatureCollection",
            "features": [],
        }
        return {"shortest": dummy, "recommended": dummy}
    recommended_distance = recommended_destination_path[0]
    recommended_geojson = json.loads(recommended_destination_path[1])
    recommended = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": recommended_geojson["type"],
                    "coordinates": recommended_geojson["coordinates"],
                },
                "properties": {
                    "shade_rate": 0.0,
                    "total_distance": recommended_distance,
                    "total_minutes": recommended_distance / WALK_SPEED,
                },
            }
        ],
    }
    response = {"shortest": shortest, "recommended": recommended}
    return response
