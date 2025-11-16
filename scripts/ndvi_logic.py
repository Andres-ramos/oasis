from django.contrib.gis.gdal import GDALRaster
from app.models import NDVILayer


route_example = {
    "distance": 1886.734, "weight": 1180.416452, "time": 1389371, "transfers": 0, "legs": [], "points_encoded": False, "bbox": [
        -66.056021,
        18.397633,
        -66.045233,
        18.40645
    ], "points": {"type": "LineString", "coordinates": [
            [
                -66.056021,
                18.40645
            ],
            [
                -66.056007,
                18.405983
            ],
            [
                -66.054737,
                18.406035
            ],
            [
                -66.054612,
                18.405264
            ],
            [
                -66.054642,
                18.405221
            ],
            [
                -66.054635,
                18.40515
            ],
            [
                -66.054569,
                18.404839
            ],
            [
                -66.054408,
                18.404459
            ],
            [
                -66.054254,
                18.404045
            ],
            [
                -66.054007,
                18.403627
            ],
            [
                -66.053932,
                18.403566
            ],
            [
                -66.053847,
                18.40347
            ],
            [
                -66.05356,
                18.403042
            ],
            [
                -66.053453,
                18.402895
            ],
            [
                -66.053522,
                18.402862
            ],
            [
                -66.053009,
                18.402157
            ],
            [
                -66.052842,
                18.401938
            ],
            [
                -66.052571,
                18.401676
            ],
            [
                -66.05256,
                18.401647
            ],
            [
                -66.052588,
                18.401628
            ],
            [
                -66.052602,
                18.401627
            ],
            [
                -66.0526,
                18.401605
            ],
            [
                -66.052361,
                18.401597
            ],
            [
                -66.05217,
                18.401483
            ],
            [
                -66.051877,
                18.401328
            ],
            [
                -66.051762,
                18.400912
            ],
            [
                -66.051671,
                18.400685
            ],
            [
                -66.051511,
                18.400415
            ],
            [
                -66.051078,
                18.399878
            ],
            [
                -66.049685,
                18.399749
            ],
            [
                -66.048677,
                18.399855
            ],
            [
                -66.048669,
                18.399726
            ],
            [
                -66.048665,
                18.399107
            ],
            [
                -66.04868,
                18.398458
            ],
            [
                -66.048489,
                18.398458
            ],
            [
                -66.048499,
                18.397674
            ],
            [
                -66.045233,
                18.397633
            ]
        ]
    }, "instructions": [
        {"distance": 52.016, "heading": 178.35, "sign": 0, "interval": [
                0,
                1
            ], "text": "Continue", "time": 37452, "street_name": ""
        },
        {"distance": 134.306, "sign": -2, "interval": [
                1,
                2
            ], "text": "Turn left onto Calle Reverendo Domingo Marrero Navarro", "time": 113765, "street_name": "Calle Reverendo Domingo Marrero Navarro"
        },
        {"distance": 307.798, "sign": 2, "interval": [
                2,
                11
            ], "text": "Turn right onto Calle Añasco", "time": 221613, "street_name": "Calle Añasco"
        },
        {"distance": 56.408, "sign": 0, "interval": [
                11,
                12
            ], "text": "Continue onto Calle Cabrera", "time": 40614, "street_name": "Calle Cabrera"
        },
        {"distance": 19.859, "sign": 0, "interval": [
                12,
                13
            ], "text": "Continue onto Avenida Dr. José Narciso Gándara Cartagena", "time": 14298, "street_name": "Avenida Dr. José Narciso Gándara Cartagena"
        },
        {"distance": 8.085, "sign": 2, "interval": [
                13,
                14
            ], "text": "Turn right", "time": 5821, "street_name": ""
        },
        {"distance": 177.156, "sign": -2, "interval": [
                14,
                21
            ], "text": "Turn left", "time": 133886, "street_name": ""
        },
        {"distance": 25.339, "sign": -2, "interval": [
                21,
                22
            ], "text": "Turn left onto Calle Amalia Marín", "time": 18244, "street_name": "Calle Amalia Marín"
        },
        {"distance": 59.234, "sign": 1, "interval": [
                22,
                24
            ], "text": "Turn slight right onto Avenida Dr. José Narciso Gándara Cartagena", "time": 50174, "street_name": "Avenida Dr. José Narciso Gándara Cartagena"
        },
        {"distance": 184.441, "sign": 2, "interval": [
                24,
                28
            ], "text": "Turn right onto Calle Rosales", "time": 132798, "street_name": "Calle Rosales"
        },
        {"distance": 254.734, "sign": -2, "interval": [
                28,
                30
            ], "text": "Turn left onto Calle Robles", "time": 183409, "street_name": "Calle Robles"
        },
        {"distance": 155.408, "sign": 2, "interval": [
                30,
                33
            ], "text": "Turn right", "time": 111893, "street_name": ""
        },
        {"street_ref": "PR-47", "distance": 20.216, "sign": -2, "interval": [
                33,
                34
            ], "text": "Turn left onto Avenida José de Diego", "time": 14556, "street_name": "Avenida José de Diego"
        },
        {"distance": 87.129, "sign": 2, "interval": [
                34,
                35
            ], "text": "Turn right onto Calle Monseñor Torres", "time": 62733, "street_name": "Calle Monseñor Torres"
        },
        {"distance": 344.605, "sign": -2, "interval": [
                35,
                36
            ], "text": "Turn left onto Calle Arzuaga", "time": 248115, "street_name": "Calle Arzuaga"
        },
        {"distance": 0.0, "sign": 4, "last_heading": 90.91121335340772, "interval": [
                36,
                36
            ], "text": "Arrive at destination", "time": 0, "street_name": ""
        }
    ], "details": {}, "ascend": 27.0914306640625, "descend": 7.2474365234375, "snapped_waypoints": {"type": "LineString", "coordinates": [
            [
                -66.056021,
                18.40645
            ],
            [
                -66.045233,
                18.397633
            ]
        ]
    }
}

def run() -> None:
    # TODO: Get NDVI from database
    ndvi = NDVILayer.objects.get()
    print(ndvi)
    # TODO: Convert route into usable geometry (geojson?, shapely linestring?)
    # TODO: Make buffer for route
    # TODO: Compute overlap with raster
