CREATE OR REPLACE FUNCTION shade_fromAtoB(
  IN x1 numeric,
  IN y1 numeric,
  IN x2 numeric,
  IN y2 numeric,
  IN depart_at time DEFAULT now(),
  OUT seq INTEGER,
  OUT gid BIGINT,
  OUT cost double precision,
  OUT distance double precision,
  OUT geom geometry,
  OUT rate double precision
)
RETURNS SETOF record AS
$BODY$
DECLARE
    final_query TEXT;
BEGIN
    final_query :=
        FORMAT( $$
            WITH
            vertices AS (
                SELECT * FROM public.roads_vertices_pgr
                WHERE id IN (
                    SELECT source FROM public.roads
                    UNION
                    SELECT target FROM public.roads)
            ),
            slots AS (
                SELECT * FROM shades
                WHERE time between time '%5$s' and time '%5$s' + interval '4 minutes 59 seconds'
            ),
            dijkstra AS (
                SELECT *
                FROM pgr_dijkstra(
                    -- cost = length * (1 + sunlight rate)
                    'SELECT roads.id AS id, source, target, ST_Length(ST_Transform(geom, 3857)) * (1 + ABS(rate)) AS cost 
                     FROM roads 
                     INNER JOIN (
                       SELECT * FROM shades
                       WHERE time between time ''%5$s'' and time ''%5$s'' + interval ''4 minutes 59 seconds''
                     ) AS shades 
                     ON roads.id = shades.id ORDER BY cost',
                    -- source
                    (SELECT id FROM vertices
                        ORDER BY the_geom <-> ST_SetSRID(ST_Point(%1$s, %2$s), 4612) LIMIT 1),
                    -- target
                    (SELECT id FROM vertices
                        ORDER BY the_geom <-> ST_SetSRID(ST_Point(%3$s, %4$s), 4612) LIMIT 1),
                    false
                )
                INNER JOIN slots ON edge = slots.id
            )
            SELECT
                seq,
                dijkstra.edge AS gid,
                dijkstra.cost,
                st_length(st_transform(roads.geom, 3857)),
                roads.geom,
                dijkstra.rate
            FROM dijkstra, public.roads WHERE dijkstra.edge = roads.id;$$,
        x1,y1,x2,y2,depart_at); -- %1 to %4 of the FORMAT function
    --RAISE notice '%', final_query;
    RETURN QUERY EXECUTE final_query;
END;
$BODY$
LANGUAGE 'plpgsql';
