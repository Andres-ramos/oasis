from django.contrib import admin

from .models import Route

# Register your models here.
models = [
    Route
]
admin.site.register(models)