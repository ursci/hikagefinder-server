CREATE OR REPLACE FUNCTION shortest_fromAtoB(
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
                SELECT * FROM public.shibuya_roads_vertices_pgr
                WHERE id IN (
                    SELECT source FROM public.shibuya_roads
                    UNION
                    SELECT target FROM public.shibuya_roads)
            ),
            shades AS (
                SELECT * FROM shibuya_shades
                WHERE time between time '%5$s' and time '%5$s' + interval '4 minutes 59 seconds'
            ),
            dijkstra AS (
                SELECT *
                FROM pgr_dijkstra(
                    'SELECT id, source, target, st_length(st_transform(geom, 3857)) as cost FROM shibuya_roads',
                    -- source
                    (SELECT id FROM vertices
                        ORDER BY the_geom <-> ST_SetSRID(ST_Point(%1$s, %2$s), 4612) LIMIT 1),
                    -- target
                    (SELECT id FROM vertices
                        ORDER BY the_geom <-> ST_SetSRID(ST_Point(%3$s, %4$s), 4612) LIMIT 1),
                    false
                )
                INNER JOIN shades ON edge = shades.id
            )
            SELECT
                seq,
                dijkstra.edge AS gid,
                dijkstra.cost,
                st_length(st_transform(shibuya_roads.geom, 3857)),
                shibuya_roads.geom,
                dijkstra.rate
            FROM dijkstra, shibuya_roads WHERE dijkstra.edge = shibuya_roads.id;$$,
        x1,y1,x2,y2,depart_at); -- %1 to %4 of the FORMAT function
    --RAISE notice '%', final_query;
    RETURN QUERY EXECUTE final_query;
END;
$BODY$
LANGUAGE 'plpgsql';
