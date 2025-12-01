import math
from pathlib import Path
import geopandas as gpd
from shapely.affinity import translate
from shapely.geometry import mapping
from pyproj import Transformer
from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime, timezone

GEOJSON_IN = Path("sjPR_buildings.geojson")
OUT = Path("shadows_san_juanPRCurrent.geojson")
HEIGHT_FIELD = "height"
DEFAULT_HEIGHT = 6.0

DT = datetime.now(timezone.utc)

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
    return translate(poly, xoff=dx, yoff=dy)

def main():
    gdf = gpd.read_file(GEOJSON_IN)
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    metr = gdf.to_crs(epsg=3857)

    shadow_features = []
    for _, row in metr.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue
        h = row.get(HEIGHT_FIELD)
        try:
            h = float(h)
        except Exception:
            h = DEFAULT_HEIGHT

        centroid = geom.centroid
        lon_lat = Transformer.from_crs(metr.crs, "EPSG:4326", always_xy=True).transform(centroid.x, centroid.y)
        lon, lat = lon_lat
        elev, az = sun_angles(lat, lon, DT)
        if elev <= 0:
            continue

        shadow_poly = project_shadow(geom, h, elev, az)
        if shadow_poly is None or shadow_poly.is_empty:
            continue

        shadow_features.append({"geometry": shadow_poly, "properties": {"height": h}})

    if not shadow_features:
        print("No shadows computed (sun below horizon or no heights).")
        return

    from geopandas import GeoDataFrame

    records = []
    for feat in shadow_features:
        rec = feat.get("properties", {}).copy()
        rec["geometry"] = feat["geometry"]
        records.append(rec)

    shadows_gdf = GeoDataFrame(records, geometry="geometry", crs=metr.crs)

    shadows_gdf = shadows_gdf.to_crs(epsg=4326)
    shadows_gdf.to_file(OUT, driver="GeoJSON")
    print("Wrote", OUT, "with", len(shadows_gdf), "shadow features")

if __name__ == "__main__":
    main()

