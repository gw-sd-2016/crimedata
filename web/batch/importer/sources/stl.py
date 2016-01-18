from spatial.models import Subdivision
import csv
from shapely.geometry import Polygon as s_poly, MultiPolygon as s_mpoly
from shapely import wkt as s_wkt


def import_subdivisions():
    filepath = "/home/ben/sd/app/demo/stl/stl_hom.csv"
    with open(filepath) as stlcsv:
        reader = csv.DictReader(stlcsv)
        idx = 0
        for line in reader:
            city_name = line["NAME"]
            state_name = line["STATE_NAME"]
            poly = line["WKT"]

            F = s_wkt.loads(poly)
            if type(F) is s_poly:
                F = s_mpoly([F,])

            poly = F.wkt

            Subdivision.objects.create(
                polygon=poly,
                display_name="%s County, %s" % (city_name, state_name),
                src_file_index=idx
            )
            print("%d: %s %s" % (idx, city_name, state_name))
            idx += 1


        # csvreader = csv.reader(stlcsv, delimiter=",", quotechar='"')
        # for row in csvreader:
        #     WKT = row[0]
        #     city_name = row[]
        #     print(WKT)