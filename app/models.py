from django.contrib.gis.db import models

class Route(models.Model):
    time = models.FloatField()
    distance = models.FloatField()
    ascend = models.FloatField()
    descend = models.FloatField()
    instructions = models.JSONField()
    request_time = models.DateTimeField()
    route = models.LineStringField()
    departure = models.PointField()
    destination = models.PointField()
    ndvi_count = models.FloatField()

class NDVILayer(models.Model):
    date = models.DateField()
    satellite = models.CharField(max_length=32)
    image = models.RasterField()

class POI(models.Model):
    name = models.CharField(max_length=128)
    municipality = models.CharField(max_length=24)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    category=models.CharField(max_length=24)
    location = models.PointField()


class Shadow(models.Model):
    polygon = models.PolygonField()
    time = models.TimeField()
    season = models.CharField(max_length=12)