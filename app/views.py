from django.shortcuts import render
from django.http import HttpResponse
import json 
from django.http import JsonResponse
from .routing import get_route
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from app.models import Route
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import logging

logger = logging.getLogger(__name__)


class RouteCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        logger.info("Processing routing engpoint")

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=400)
        
        origin = data.get('origin')
        destination = data.get('destination')
        if not origin:
            logger.info("Malformed request")
            return Response({'error': 'origin is required'}, status=400)
        if not destination:
            logger.info("Malformed request")
            return Response({'error': 'destination is required'}, status=400)

        request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info("Processing route")
        try:
            route_data = get_route(
                origin['lng'], origin['lat'],
                destination['lng'], destination['lat']
            )

        except Exception:
            logger.error("Routing service error")
            return Response({"error": "routing service error"}, status=500)


        origin_geojson = {
            "type": "Point",
            "coordinates": [origin["lng"], origin["lat"]]
        }
        destination_geojson = {
            "type": "Point",
            "coordinates": [destination["lng"], destination["lat"]]
        }
        try:
            origin_geom = GEOSGeometry(json.dumps(origin_geojson))        
            destination_geom = GEOSGeometry(json.dumps(destination_geojson))
            route_linestring = GEOSGeometry(json.dumps(route_data["points"]))
        except Exception:
            logger.error("Route service formatting error")

        logger.info("Inserting route into databse")
        try:
            route_obj = Route.objects.create(
                time=route_data["time"],
                distance=route_data["distance"],
                ascend=route_data["ascend"],
                descend=route_data["descend"],
                instructions=json.dumps(route_data["instructions"]),
                request_time=request_time,
                route=route_linestring,
                departure=origin_geom,
                destination=destination_geom
            )
            route_obj.save()
        except Exception:
            logger.error("Route db insertion error")

        logger.info("Returning route to client")
        return Response({'route': route_data}, status=200)