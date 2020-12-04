#!/bin/bash
set -e

wget -O /tmp/import.sql https://raw.githubusercontent.com/ursci/hikagefinder-data/main/shibuya/SunExpo_shibuya_9_10_every5min.sql

# TODO: use connection parameters from environment
psql -U ursci -d hikage_prod -f /tmp/import.sql
psql -U ursci -d hikage_prod -c "SELECT public.pgr_createTopology('import', 0.0000001, 'geom', 'gid')";
psql -U ursci -d hikage_prod -c "REFRESH MATERIALIZED VIEW public.shades"
psql -U ursci -d hikage_prod -c "ANALYZE"
