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


@require_POST
@csrf_exempt
def route(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    origin = data.get('origin')
    destination = data.get('destination')
    if not origin:
        return JsonResponse({'error': 'origin is required'}, status=400)
    if not destination:
        return JsonResponse({'error': 'destination is required'}, status=400)

    request_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        route_data = get_route(
            origin['lng'], origin['lat'],
            destination['lng'], destination['lat']
        )

    except Exception:
        return JsonResponse({"error": "routing service error"}, status=500)


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
        print("Route service formatting error")

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
        print("Route db insertion error")

    return JsonResponse({'route': route_data}, status=200)