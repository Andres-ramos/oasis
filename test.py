import requests
import json
from requests.exceptions import RequestException
from app.routing import get_route
# def get_route(lng_a, lat_a, lng_b, lat_b):


#     BASE_URI = "https://graphhopper.com/api/1/route"
#     params = {
#         "key": "676fc600-5875-4ea5-abd5-0a85e515dc98" #Get from os env
#     }
#     header = {
#         "Content-Type": "application/json"
#     }
#     body = {
#     "points": [
#         [
#         lng_a,
#         lat_a
#         ],
#         [
#         lng_b,
#         lat_b
#         ]
#     ],
#     "profile": "foot",
#     "locale": "en",
#     "instructions": True,
#     "calc_points": True,
#     "points_encoded": False,
#     "algorithm":"alternative_route"
#     }
#     json_body = json.dumps(body, separators=(',', ':'))
#     try :
#         data = requests.post(BASE_URI, params=params, data=json_body, headers=header)
#     except RequestException:
#         pass 
#     try:
#         data = data.json()
#     except json.JSONDecodeError:
#         pass 

#     return data


lng_a, lat_a = -66.0558729145757, 18.40645451907811
lng_b, lat_b = -66.04523944929657, 18.397270128021844
 
print(get_route(lng_a, lat_a, lng_b, lat_b))