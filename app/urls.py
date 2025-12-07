from django.urls import path

from .views import RouteCreateView
from .views import POIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("poi", POIView)

urlpatterns = router.urls
urlpatterns += [
    path('routing', RouteCreateView.as_view()),
]