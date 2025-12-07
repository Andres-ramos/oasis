from app.models import POI
from django.contrib.gis.geos import Point
import pandas as pd

def run() -> None:
    # TODO: Poner el path correcto
    csv_path = "./pois.csv"
    df = pd.read_csv(csv_path)
    df_records = df.to_dict(orient='records')
    # print(df_records[0])
    model_instances = [POI(
        name=record['Facility Name'],
        municipality=record['Municipality'],
        location=Point(record["Latitude"], record["Longitude"]),
        address=record["Address"],
        phone_number=record["Phone Number"],
        category=record["Categoria"]
    ) for record in df_records]

    POI.objects.bulk_create(model_instances)