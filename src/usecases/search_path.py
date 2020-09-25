from datetime import datetime
import json
from fastapi.exceptions import HTTPException
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

import schemas
from models.route import Point


RAW_SHORTEST_QUERY = """
SELECT
    SUM(distance),
    ST_AsGeoJSON(ST_LineMerge(ST_Union(geom))),
    SUM(distance * ABS(rate)) / SUM(distance)
FROM shortest_fromAtoB(:x1, :y1, :x2, :y2, :depart_at);
""".strip()

RAW_RECOMMENDED_QUERY = """
SELECT
    SUM(distance),
    ST_AsGeoJSON(ST_LineMerge(ST_Union(geom))),
    SUM(distance * ABS(rate)) / SUM(distance)
FROM shade_fromAtoB(:x1, :y1, :x2, :y2, :depart_at);
""".strip()

# Find number of roads within about 500m
RAW_NEAREST_ROAD_QUERY = """
SELECT count(*)
FROM shibuya_roads
WHERE
    ST_DWithin(geom, ST_SetSRID(ST_Point(:x1, :y1),4612), 0.005)
""".strip()

WALK_SPEED = 80


def search_path(
    db: Session, source: Point, destination: Point, departure_time: datetime
):
    # Validation for departure point
    sql_statement = text(RAW_NEAREST_ROAD_QUERY)
    args = {
        "x1": source.lon,
        "y1": source.lat,
    }
    num_of_near_roads_from_start_point = db.execute(sql_statement, args).fetchone()
    if num_of_near_roads_from_start_point[0] == 0:
        raise HTTPException(
            status_code=422,
            detail="Out of service area",
        )

    # Validation for destination point
    args = {
        "x1": destination.lon,
        "y1": destination.lat,
    }
    num_of_near_roads_from_dest_point = db.execute(sql_statement, args).fetchone()
    if num_of_near_roads_from_dest_point[0] == 0:
        raise HTTPException(
            status_code=422,
            detail="Out of service area",
        )

    # Find shortest path
    sql_statement = text(RAW_SHORTEST_QUERY)
    args = {
        "x1": source.lon,
        "y1": source.lat,
        "x2": destination.lon,
        "y2": destination.lat,
        "depart_at": departure_time.time().strftime("%H:%M:%S"),
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
                    "sunlight_rate": nearest_destination_path[2],
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
        "depart_at": departure_time.time().strftime("%H:%M:%S"),
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
                    "sunlight_rate": recommended_destination_path[2],
                    "total_distance": recommended_distance,
                    "total_minutes": recommended_distance / WALK_SPEED,
                },
            }
        ],
    }
    response = {"shortest": shortest, "recommended": recommended}
    return response
