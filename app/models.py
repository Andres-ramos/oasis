from django.contrib.gis.db import models

# Create your models here.

class Route(models.Model):
    time = models.FloatField()
    distance = models.FloatField()
    ascend = models.FloatField()
    descend = models.FloatField()
    instructions = models.JSONField()
    request_time = models.DateField()
    route = models.LineStringField()
    departure = models.PointField()
    destination = models.PointField()

class NDVILayer(models.Model):
    date = models.DateField()
    satellite = models.CharField(max_length=32)
    image = models.RasterField()