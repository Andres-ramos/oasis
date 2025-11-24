from django.urls import path

from .views import RouteCreateView

urlpatterns = [
    path("", RouteCreateView.as_view() , name="route"),
]