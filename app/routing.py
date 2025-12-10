import requests
import json
from requests.exceptions import RequestException

from dotenv import load_dotenv
import os
import logging
import geopandas as gpd
import shapely
import rioxarray as rxr
from geojson import Feature 


logger = logging.getLogger(__name__)

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
        "algorithm": ALGORITHM,
        "alternative_route.max_paths": 5,
        "alternative_route.max_share_factor": 1
    }
    json_body = json.dumps(body, separators=(',', ':'))
    try :
        logger.info("Requesting data from graphhopper API")
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

def compute_route_ndvi(route_geojson):
    BUFFER_SIZE=15
    gdf = gpd.GeoDataFrame.from_features(route_geojson)
    gdf = gdf.set_crs(4326)
    transformed_gdf = gdf.to_crs(6566)
    transformed_gdf["geometry"] = transformed_gdf.buffer(15)
    buff_gdf = transformed_gdf.to_crs(4326)
    # TODO: Load raster from db in the future :)
    instance = "./RP_NDVI.tif"
    ndvi_raster = rxr.open_rasterio(instance)
    clipped_raster = ndvi_raster.rio.clip(buff_gdf.geometry.values, buff_gdf.crs)
    return clipped_raster.sum().values

def get_route(lng_a, lat_a, lng_b, lat_b):
    payload = get_routes_from_graphopper(lng_a, lat_a, lng_b, lat_b)
    # payload = {'hints': {'visited_nodes.sum': 722, 'visited_nodes.average': 722.0}, 'info': {'copyrights': ['GraphHopper', 'OpenStreetMap contributors'], 'took': 4, 'road_data_timestamp': '2025-12-09T02:00:00Z'}, 'paths': [{'distance': 1223.594, 'weight': 1087.276992, 'time': 894846, 'transfers': 0, 'legs': [], 'points_encoded': False, 'bbox': [-66.055072, 18.398452, -66.048283, 18.404925], 'points': {'type': 'LineString', 'coordinates': [[-66.055072, 18.404906], [-66.05507, 18.404843], [-66.055048, 18.404834], [-66.054587, 18.404925], [-66.054569, 18.404839], [-66.054408, 18.404459], [-66.054254, 18.404045], [-66.054007, 18.403627], [-66.053932, 18.403566], [-66.053847, 18.40347], [-66.05356, 18.403042], [-66.053453, 18.402895], [-66.053522, 18.402862], [-66.053009, 18.402157], [-66.052842, 18.401938], [-66.052571, 18.401676], [-66.05256, 18.401647], [-66.052588, 18.401628], [-66.052602, 18.401627], [-66.0526, 18.401605], [-66.052361, 18.401597], [-66.05217, 18.401483], [-66.051877, 18.401328], [-66.051762, 18.400912], [-66.051671, 18.400685], [-66.051511, 18.400415], [-66.051078, 18.399878], [-66.049685, 18.399749], [-66.048677, 18.399855], [-66.048669, 18.399726], [-66.048665, 18.399107], [-66.04868, 18.398458], [-66.048283, 18.398452]]}, 'instructions': [{'distance': 59.198, 'heading': 178.17, 'sign': 0, 'interval': [0, 3], 'text': 'Continue', 'time': 42623, 'street_name': ''}, {'distance': 181.767, 'sign': 2, 'interval': [3, 9], 'text': 'Turn right onto Calle Añasco', 'time': 130871, 'street_name': 'Calle Añasco'}, {'distance': 56.408, 'sign': 0, 'interval': [9, 10], 'text': 'Continue onto Calle Cabrera', 'time': 40614, 'street_name': 'Calle Cabrera'}, {'distance': 19.859, 'sign': 0, 'interval': [10, 11], 'text': 'Continue onto Avenida Dr. José Narciso Gándara Cartagena', 'time': 14298, 'street_name': 'Avenida Dr. José Narciso Gándara Cartagena'}, {'distance': 8.085, 'sign': 2, 'interval': [11, 12], 'text': 'Turn right', 'time': 5821, 'street_name': ''}, {'distance': 177.156, 'sign': -2, 'interval': [12, 19], 'text': 'Turn left', 'time': 133886, 'street_name': ''}, {'distance': 25.339, 'sign': -2, 'interval': [19, 20], 'text': 'Turn left onto Calle Amalia Marín', 'time': 18244, 'street_name': 'Calle Amalia Marín'}, {'distance': 59.234, 'sign': 1, 'interval': [20, 22], 'text': 'Turn slight right onto Avenida Dr. José Narciso Gándara Cartagena', 'time': 50174, 'street_name': 'Avenida Dr. José Narciso Gándara Cartagena'}, {'distance': 184.441, 'sign': 2, 'interval': [22, 26], 'text': 'Turn right onto Calle Rosales', 'time': 132798, 'street_name': 'Calle Rosales'}, {'distance': 254.734, 'sign': -2, 'interval': [26, 28], 'text': 'Turn left onto Calle Robles', 'time': 183409, 'street_name': 'Calle Robles'}, {'distance': 155.408, 'sign': 2, 'interval': [28, 31], 'text': 'Turn right', 'time': 111893, 'street_name': ''}, {'street_ref': 'PR-47', 'distance': 41.964, 'sign': -2, 'interval': [31, 32], 'text': 'Turn left onto Avenida José de Diego', 'time': 30215, 'street_name': 'Avenida José de Diego'}, {'distance': 0.0, 'sign': 4, 'last_heading': 91.530007772149, 'interval': [32, 32], 'text': 'Arrive at destination', 'time': 0, 'street_name': ''}], 'details': {}, 'ascend': 19.3289794921875, 'descend': 3.752960205078125, 'snapped_waypoints': {'type': 'LineString', 'coordinates': [[-66.055072, 18.404906], [-66.048283, 18.398452]]}}, {'distance': 1329.922, 'weight': 1160.647717, 'time': 963287, 'transfers': 0, 'legs': [], 'points_encoded': False, 'bbox': [-66.055072, 18.398452, -66.048283, 18.404925], 'points': {'type': 'LineString', 'coordinates': [[-66.055072, 18.404906], [-66.05507, 18.404843], [-66.055048, 18.404834], [-66.054587, 18.404925], [-66.054569, 18.404839], [-66.054408, 18.404459], [-66.054254, 18.404045], [-66.054007, 18.403627], [-66.053932, 18.403566], [-66.053847, 18.40347], [-66.05356, 18.403042], [-66.053453, 18.402895], [-66.053522, 18.402862], [-66.053009, 18.402157], [-66.052842, 18.401938], [-66.052571, 18.401676], [-66.05256, 18.401647], [-66.052588, 18.401628], [-66.052602, 18.401627], [-66.0526, 18.401605], [-66.05287, 18.401622], [-66.052971, 18.399642], [-66.052289, 18.399646], [-66.052319, 18.399412], [-66.052394, 18.399088], [-66.051387, 18.398812], [-66.050728, 18.398618], [-66.0502, 18.398486], [-66.049991, 18.39848], [-66.049912, 18.398471], [-66.048283, 18.398452]]}, 'instructions': [{'distance': 59.198, 'heading': 178.17, 'sign': 0, 'interval': [0, 3], 'text': 'Continue', 'time': 42623, 'street_name': ''}, {'distance': 181.767, 'sign': 2, 'interval': [3, 9], 'text': 'Turn right onto Calle Añasco', 'time': 130871, 'street_name': 'Calle Añasco'}, {'distance': 56.408, 'sign': 0, 'interval': [9, 10], 'text': 'Continue onto Calle Cabrera', 'time': 40614, 'street_name': 'Calle Cabrera'}, {'distance': 19.859, 'sign': 0, 'interval': [10, 11], 'text': 'Continue onto Avenida Dr. José Narciso Gándara Cartagena', 'time': 14298, 'street_name': 'Avenida Dr. José Narciso Gándara Cartagena'}, {'distance': 8.085, 'sign': 2, 'interval': [11, 12], 'text': 'Turn right', 'time': 5821, 'street_name': ''}, {'distance': 177.156, 'sign': -2, 'interval': [12, 19], 'text': 'Turn left', 'time': 133886, 'street_name': ''}, {'distance': 28.542, 'sign': 2, 'interval': [19, 20], 'text': 'Turn right onto Calle Amalia Marín', 'time': 19960, 'street_name': 'Calle Amalia Marín'}, {'distance': 220.424, 'sign': -2, 'interval': [20, 21], 'text': 'Turn left onto Calle González', 'time': 158705, 'street_name': 'Calle González'}, {'distance': 71.945, 'sign': -2, 'interval': [21, 22], 'text': 'Turn left onto Callejón Borinquena', 'time': 51800, 'street_name': 'Callejón Borinquena'}, {'street_ref': 'PR-25', 'distance': 63.047, 'sign': 2, 'interval': [22, 24], 'text': 'Turn right onto Avenida Juan Ponce de León', 'time': 45394, 'street_name': 'Avenida Juan Ponce de León'}, {'street_ref': 'PR-47', 'distance': 443.49, 'sign': -2, 'interval': [24, 30], 'text': 'Turn left onto Paseo José de Diego', 'time': 319315, 'street_name': 'Paseo José de Diego'}, {'distance': 0.0, 'sign': 4, 'last_heading': 91.530007772149, 'interval': [30, 30], 'text': 'Arrive at destination', 'time': 0, 'street_name': ''}], 'details': {}, 'ascend': 18.98699951171875, 'descend': 3.410980224609375, 'snapped_waypoints': {'type': 'LineString', 'coordinates': [[-66.055072, 18.404906], [-66.048283, 18.398452]]}}]}
    print("num routes", len(payload["paths"]))
    ndvi_counts = []
    for path in payload["paths"]:
        route_geojson = Feature(geometry=path["points"])
        ndvi_count = compute_route_ndvi([route_geojson])
        ndvi_counts.append(ndvi_count)

    max_ndvi = max(ndvi_counts)
    max_ndvi_route_index = ndvi_counts.index(max_ndvi)

    # # TODO: Implement algorithm for computing overlaps with shadow and ndvi layers and return best route
    # # TODO: Get bounding box from the payload
    # bbox = ""
    # shadow_layer = compute_shadow_layer(bbox)
    # ndvi_layer = compute_ndvi_layer(bbox)

    # best_route = ""
    # for route in payload["route"]:
    #     # TODO: Measure overlap with shadow layer and ndvi layer
    #     pass 
    path_object = payload["paths"][max_ndvi_route_index]
    path["ndvi"] = max_ndvi
    return path