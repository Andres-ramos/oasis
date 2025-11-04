from django.shortcuts import render
from django.http import HttpResponse
import json 
from django.http import JsonResponse
from .routing import get_route
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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
    
    route = get_route(
        origin['lng'], origin['lat'],
        destination['lng'], destination['lat']
    )

    return JsonResponse({'route': route})