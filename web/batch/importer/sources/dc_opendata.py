from spatial.models import Subdivision
import urllib3
import json
import time
from shapely.geometry import shape, Polygon as s_poly, MultiPolygon as s_mpoly


def import_squares():
    # http://opendata.dc.gov/datasets/84ab8b676a384c339062b53dca3bdfa2_41.geojson
    # http://opendata.dc.gov/datasets/84ab8b676a384c339062b53dca3bdfa2_41

    DC_OPENDATA_SRC = "http://opendata.dc.gov/datasets/84ab8b676a384c339062b53dca3bdfa2_41.geojson"

    http = urllib3.PoolManager()
    data = None

    while True:
        r = http.request("GET", DC_OPENDATA_SRC)
        if r.status == 200:
            req_data = json.loads(r.data.decode("utf-8"))
            if req_data['features'] is not None:
                # print(r.data)
                data = req_data
                break
            else:
                # print(r.data)
                time.sleep(15)

    for feature in data['features']:
        shapely_input = feature['geometry']
        F = shape(shapely_input)

        if type(F) is s_poly:
            F = s_mpoly([F,])

        Subdivision.objects.create(
            polygon = F.wkt,
            display_name = "DC-%s" % feature['properties']['OBJECTID'],
            src_file_index = feature['properties']['OBJECTID']
        )