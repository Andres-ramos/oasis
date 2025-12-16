import math
from pathlib import Path
import geopandas as gpd
from shapely.affinity import translate
from shapely.geometry import mapping
from pyproj import Transformer
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone, time, timedelta
from zoneinfo import ZoneInfo

from app.models import Shadow
from django.contrib.gis.geos import GEOSGeometry
import shapely
from shapely import Polygon




GEOJSON_IN = Path("./sjPR_buildings.geojson")
OUT = Path("shadows_san_juanPRCurrent.geojson")
HEIGHT_FIELD = "height"
DEFAULT_HEIGHT = 6.0

RP_AOI = {
    "type": "FeatureCollection",
    "features": [
        {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "coordinates": [
            [
                [
                -66.05803857394139,
                18.41709353114257
                ],
                [
                -66.05803857394139,
                18.384132746780622
                ],
                [
                -66.02875622742928,
                18.384132746780622
                ],
                [
                -66.02875622742928,
                18.41709353114257
                ],
                [
                -66.05803857394139,
                18.41709353114257
                ]
            ]
            ],
            "type": "Polygon"
        }
        }
    ]
}

print("Loading geojson file into memory")
sj_gdf = gpd.read_file(GEOJSON_IN)
# sj_gdf = sj_gdf.set_crs(epsg=4326)

def sun_angles(lat, lon, when):
    elev = get_altitude(lat, lon, when)
    az = get_azimuth(lat, lon, when)
    return elev, az

def project_shadow(poly, height, elev_deg, az_deg):
       #shadow_length = height / tan(elevation)
    if elev_deg <= 0 or height <= 0:
        return None
    elev_rad = math.radians(elev_deg)
    az_rad = math.radians(az_deg)
    # sun azimuth from pysolar is clockwise from north; convert to vector x(east), y(north)
    # x = sin(az)*len, y = cos(az)*len (north positive)
    shadow_len = height / math.tan(elev_rad)
    dx = math.sin(az_rad) * shadow_len
    dy = math.cos(az_rad) * shadow_len
    # translate polygon by (dx east, dy north)
    # print("poly orig", poly)
    return translate(poly, xoff=dx, yoff=dy)

def filter_gdf(gdf):
    aoi_coords = RP_AOI["features"][0]["geometry"]["coordinates"][0]
    polygon = Polygon(aoi_coords)
    aoi_gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon])
    return gpd.sjoin(gdf, aoi_gdf)


def insert_shadow_batch(season, time):
    print(f"Inserting batch {season}-{time}")
    gdf = filter_gdf(sj_gdf)
    # metr = gdf.to_crs(epsg=6566)
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    # metr = gdf.to_crs(epsg=3857)
    metr = gdf.to_crs(epsg=3857)

    # gdf = gdf[~gdf["geometry"].isna()]
    # time = datetime.now(timezone.utc)
    shadow_features = []
    c = 0
    for _, row in metr.iterrows():
        geom = row.geometry

        try:
            h = float(h)
        except Exception:
            h = DEFAULT_HEIGHT

        centroid = geom.centroid
        # lon, lat = centroid.x, centroid.y
        lon, lat = Transformer.from_crs(metr.crs, "EPSG:4326", always_xy=True).transform(centroid.x, centroid.y)
        # print(lon, lat)
        elev, az = sun_angles(lat, lon, time)
        # print(elev, az)
        if elev <= 0:
            continue
        # print(elev, az)
        shadow_poly = project_shadow(geom, h, elev, az)
        # print(shadow_poly)
        if shadow_poly is None or shadow_poly.is_empty:
            continue
        # print(shadow_poly)
        db_geometry = GEOSGeometry(shapely.to_wkt(shadow_poly), srid=3857)
        shadow_db = Shadow.objects.create(
            polygon=db_geometry,
            time=time,
            season=season
        )
        data = shadow_db.save()
        c += 1
        # break 
    
    print(f"Inserted {len(metr)} polygons \n")

def main():


    SEASON_LIST = ["winter", "summer", "fall", "spring"]

    for season in SEASON_LIST:
        start_time = time(10, 0)
        end_time = time(19, 0)

        # TODO: Change to summer solstice date
        start = datetime.combine(datetime.today(), start_time)
        start = start.replace(tzinfo=ZoneInfo('US/Eastern'))
        end = datetime.combine(datetime.today(), end_time)
        end= end.replace(tzinfo=ZoneInfo('US/Eastern'))
        current = start
        while current <= end:
            insert_shadow_batch(season, current)
            current += timedelta(minutes=15)
            break 
        break 
    
def run() -> None:
    main()

