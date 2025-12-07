from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import POI


class POISerializer(GeoFeatureModelSerializer):
    class Meta:
        model = POI
        fields = "__all__"
        geo_field = "location"