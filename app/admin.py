from django.contrib import admin

from .models import Route
from .models import POI
from .models import NDVILayer
from .models import Shadow

# Register your models here.
models = [
    NDVILayer,
    POI,
    Route,
    Shadow
]
admin.site.register(models)