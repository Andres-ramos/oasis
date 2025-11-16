import requests
import json
from requests.exceptions import RequestException

# from app.models import Route
from dotenv import load_dotenv
import os

load_dotenv()

def get_routes_from_graphopper(lng_a, lat_a, lng_b, lat_b):
    BASE_URI = "https://graphhopper.com/api/1/route"
    ALGORITHM = "alternative_route"
    params = {
        "key": os.getenv("GRAPHHOPPER-API-KEY") #Get from os env
    }
    header = {
        "Content-Type": "application/json"
    }
    body = {
        "points": [
            [
                lng_a,
                lat_a
            ],
            [
                lng_b,
                lat_b
            ]
        ],
        "profile": "foot",
        "locale": "en",
        "instructions": True,
        "calc_points": True,
        "points_encoded": False,
        "algorithm": ALGORITHM
    }
    json_body = json.dumps(body, separators=(',', ':'))
    try :
        data = requests.post(BASE_URI, params=params, data=json_body, headers=header)
    except RequestException:
        pass 
    try:
        data = data.json()
    except json.JSONDecodeError:
        pass 
    return data


def compute_shadow_layer(bounding_box):
    # TODO: Get angle of the sun using the datetime and location
    # TODO: Do computations and stuff to get the shade layer
    # TODO: Should probably return a multipolygon
    return 

def compute_ndvi_layer(bounding_box):
    # TODO: Compute the ndvi from a given satelite image
    # TODO: Static image or do we compute ndvi on the fly with the most recent image?
    # TODO: Should probably return a multipolygon
    return 

def get_route(lng_a, lat_a, lng_b, lat_b):
    payload = get_routes_from_graphopper(lng_a, lat_a, lng_b, lat_b)
    # TODO: Insert route into database
    
    return payload['paths'][0]

    # TODO: Implement algorithm for computing overlaps with shadow and ndvi layers and return best route
    # TODO: Get bounding box from the payload
    bbox = ""
    shadow_layer = compute_shadow_layer(bbox)
    ndvi_layer = compute_ndvi_layer(bbox)

    best_route = ""
    for route in payload["route"]:
        # TODO: Measure overlap with shadow layer and ndvi layer
        pass 

    return best_route