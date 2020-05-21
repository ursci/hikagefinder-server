import json
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

import schemas
from models.route import Point
from models.route import FoundRouteResponse


RAW_QUERY = '''
SELECT SUM(distance), ST_AsGeoJSON(ST_LineMerge(ST_Union(geom))) 
FROM shade_fromAtoB(:x1, :y1, :x2, :y2);
'''.strip()

def search_path(db: Session, source: Point, destination: Point):
    sql_statement = text(RAW_QUERY)
    args = {'x1': source.lon, 'y1': source.lat, 'x2': destination.lon, 'y2': destination.lat}
    nearest_destination_path = db.execute(sql_statement, args).first()
    print(nearest_destination_path)
    shortest_distance = nearest_destination_path[0]
    shortest_geojson = json.loads(nearest_destination_path[1])
    shortest = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': shortest_geojson['type'],
                    'coordinates': shortest_geojson['coordinates'],
                },
                'properties': {
                    'shade_rate': 0.0,
                    'total_distance': shortest_distance,
                    'total_minutes': shortest_distance,
                }
            }
        ],
    }
    response = {'shortest': shortest, 'recommended': shortest}
    return response
