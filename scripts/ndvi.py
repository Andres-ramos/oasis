from django.contrib.gis.gdal import GDALRaster
from app.models import NDVILayer


def run() -> None:
    # TODO: Poner el path correcto
    raster_path = "./RP_NDVI.tif"
    gdal_raster = GDALRaster(raster_path, write=True)
    my_raster_instance = NDVILayer(date="2020-01-01", satellite="Sentinel-2",image=gdal_raster)
    my_raster_instance.save()