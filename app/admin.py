from django.contrib import admin

from .models import Route
from .models import POI
from .models import NDVILayer

# Register your models here.
models = [
    NDVILayer,
    POI,
    Route
]
admin.site.register(models)