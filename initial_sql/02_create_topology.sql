ALTER TABLE shade ADD source INTEGER;
ALTER TABLE shade ADD target INTEGER;
SELECT pgr_createTopology('shade', 0.0000001, 'geom', 'gid');
