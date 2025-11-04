from django.contrib.gis.db import models

# Create your models here.

class Route(models.Model):
    duration = models.FloatField()
    request_time = models.DateField()
    route = models.LineStringField()