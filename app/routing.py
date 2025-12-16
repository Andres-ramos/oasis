import requests
import json
from requests.exceptions import RequestException

from dotenv import load_dotenv
import os
import logging
import geopandas as gpd
import shapely
import rioxarray as rxr
from geojson import Feature, LineString
import numpy as np
from app.models import Shadow
from django.contrib.gis.geos import GEOSGeometry


logger = logging.getLogger(__name__)

load_dotenv()

def get_routes_from_graphopper(lng_a, lat_a, lng_b, lat_b):
    BASE_URI = "https://graphhopper.com/api/1/route"
    ALGORITHM = "alternative_route"
    params = {
        "key": os.getenv("GRAPHHOPPER-API-KEY") #Get from os env
    }
    header = {
        "Content-Type": "application/json"
    }
    body = {
        "points": [
            [
                lng_a,
                lat_a
            ],
            [
                lng_b,
                lat_b
            ]
        ],
        "profile": "foot",
        "locale": "en",
        "instructions": True,
        "calc_points": True,
        "points_encoded": False,
        "algorithm": ALGORITHM,
        "alternative_route.max_paths": 5,
        "alternative_route.max_share_factor": 1
    }
    json_body = json.dumps(body, separators=(',', ':'))
    try :
        logger.info("Requesting data from graphhopper API")
        data = requests.post(BASE_URI, params=params, data=json_body, headers=header)
    except RequestException:
        logger.error("Routing service error: request exception")

    try:
        data = data.json()
    except json.JSONDecodeError:
        logger.error("Routing service error: json decode error")

    return data


def compute_shadow_layer(route_geojson):
    BUFFER_SIZE=10
    db_geom = GEOSGeometry(json.dumps(route_geojson))
    db_geom.transform(6566)
    db_geom = db_geom.buffer(BUFFER_SIZE)
    # TODO: Add filtering by hour and season
    s = Shadow.objects.filter(polygon__intersects=db_geom)
    
    a = 0
    for shadow_poly in s:
        shadow_poly.polygon.transform(6566)
        intersection = shadow_poly.polygon.intersection(db_geom)
        a += intersection.area

    return a/db_geom.area

def fragment_linestring(linestring):
    """Break a LineString into individual line segments"""
    segments = []
    coords = list(linestring.coords)
    
    for i in range(len(coords) - 1):
        segment = LineString([coords[i], coords[i + 1]])
        segments.append(segment)
    
    return segments


def compute_route_fragment_ndvi(route_geojson):
    BUFFER_SIZE=15

    gdf = gpd.GeoDataFrame.from_features(route_geojson)
    gdf = gdf.set_crs(4326)


    # Fragment all LineStrings
    all_segments = []
    for idx, row in gdf.iterrows():
        if row.geometry.geom_type == 'LineString':
            segments = fragment_linestring(row.geometry)
            for seg_id, seg in enumerate(segments):
                seg_props = row.to_dict()
                seg_props['geometry'] = seg
                seg_props['segment_id'] = seg_id
                all_segments.append(seg_props)

    gdf_fragmented = gpd.GeoDataFrame(all_segments, crs=gdf.crs)
    transformed_gdf = gdf_fragmented.to_crs(6566)
    transformed_gdf["geometry"] = transformed_gdf.buffer(15)
    buff_gdf = transformed_gdf.to_crs(4326)

    instance = "./RP_NDVI.tif"
    ndvi_raster = rxr.open_rasterio(instance)
    ndvis = []
    for geom in buff_gdf["geometry"]:
        clipped_raster = ndvi_raster.rio.clip([geom], buff_gdf.crs)
        bin_raster = clipped_raster.where(clipped_raster >= 0.1, 0.0)
        bin_raster = np.ceil(bin_raster).mean().values
        ndvis.append(bin_raster)

    gdf_fragmented["ndvi"] = ndvis
    return list(gdf_fragmented["ndvi"].values)

def compute_total_route_ndvi(route_geojson):
    BUFFER_SIZE=15
    
    gdf = gpd.GeoDataFrame.from_features(route_geojson)
    gdf = gdf.set_crs(4326)
    transformed_gdf = gdf.to_crs(6566)
    transformed_gdf["geometry"] = transformed_gdf.buffer(BUFFER_SIZE)
    buff_gdf = transformed_gdf.to_crs(4326)
    # TODO: Load raster from db
    instance = "./RP_NDVI.tif"
    ndvi_raster = rxr.open_rasterio(instance)
    clipped_raster = ndvi_raster.rio.clip(buff_gdf.geometry.values, buff_gdf.crs)
    bin_raster = clipped_raster.where(clipped_raster >= 0.1, 0.0)
    bin_raster = np.ceil(bin_raster).mean().values

    return bin_raster

def get_route(lng_a, lat_a, lng_b, lat_b):
    payload = get_routes_from_graphopper(lng_a, lat_a, lng_b, lat_b)
    ndvi_counts = []
    shade_coverages = []

    for path in payload["paths"]:
        route_geojson = Feature(geometry=path["points"])
        ndvi_count = compute_total_route_ndvi([route_geojson])
        shade_coverage = compute_shadow_layer(path["points"])
        ndvi_counts.append(ndvi_count)
        shade_coverages.append(shade_coverage)

    max_ndvi = max(ndvi_counts)
    max_shade = max(shade_coverages)
    max_ndvi_route_index = ndvi_counts.index(max_ndvi)
    max_shade_route_index = shade_coverages.index(max_shade)

    combined = [a + b for a, b in zip(ndvi_counts, shade_coverages)]
    max_index = combined.index(max(combined))

    path_object = payload["paths"][max_index]
    path["ndvi"] = ndvi_counts[max_index]
    path["shade"] = shade_coverages[max_index]

    path["ndvi_segment_list"] = compute_route_fragment_ndvi([route_geojson])
    
    return path