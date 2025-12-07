from django.urls import path

from .views import RouteCreateView
from .views import POIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register("routing", RouteCreateView)
router.register("poi", POIView)

urlpatterns = router.urls
