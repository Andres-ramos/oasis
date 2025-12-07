from django.contrib import admin

from .models import Route
from .models import POI

# Register your models here.
models = [
    POI,
    Route
]
admin.site.register(models)