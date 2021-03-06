import math
# Autocorrelation and associated helper functions
# Formula used in new_lat/new_lon from here: http://gis.stackexchange.com/a/2980
from spatial.models import Incident
import subprocess
from batch.ops.autocorr.dataproc.gengal import generate_weights
from batch.ops.autocorr.dataproc.db2txt import generate_txt

R = 6378137 # Radius of the Earth

def new_lat(old_lat, diff):
    lat_diff = diff / R
    return old_lat + (lat_diff * (180/math.pi))


def new_lon(old_lon, old_lat, diff):
    lon_diff = diff / (R * math.cos(math.pi * (old_lat / 180)))
    return old_lon + (lon_diff * (180/math.pi))

def get_squares(size, nw_lat, nw_lon, se_lat, se_lon):
    # size in **meters**
    curr_lat = nw_lat
    curr_lon = nw_lon
    squares = []

    while curr_lon < se_lon:
        while curr_lat < se_lat:
            lat = new_lat(curr_lat, size)
            lon = new_lon(curr_lon, size)

            squares.append({
                "lat": lat,
                'lon': lon,
            })

            curr_lat = lat
            curr_lon = lon

            print("Lat: %s Lon: %s" % (str(lat), str(lon)))

    return squares

def get_crimes_in_square(nw_lat, nw_lon, se_lat, se_lon):
    # Get crime records bounded by the current bounding box (NW and SE points)
    return Incident.objects.filter(
            # incident_type__pk=crime_type_id,
            lat__gte=float(se_lat),
            lat__lte=float(nw_lat),
            lon__gte=float(nw_lon),
            lon__lte=float(se_lon),
    )


def stl_process(sdiv_set, start_date, end_date, ctid, demo=False):
    weights_path = generate_weights(sdiv_set)
    print("stl_process: csv params: %s %s %s" % (start_date, end_date, ctid))
    csv_file = generate_txt(sdiv_set, ctid, start_date, end_date)

    py_file = "/home/ben/sd/web/batch/ops/autocorr/offline/__init__.py"
    csv_col = "OVERTIME"

    if demo:
        csv_file = "/home/ben/sd/app/demo/stl/stl_hom.txt"
        csv_col = "HR8893"

    py_cmd = "python2 %s \"%s\" \"%s\" \"%s\"" % (py_file, weights_path, csv_file, csv_col)

    print("stl_process will call %s" % py_cmd)

    autocorr_output = subprocess.getoutput(py_cmd)
    autocorr_obj_indexes = autocorr_output.split(",")
    autocorr_obj_indexes = [int(i) for i in autocorr_obj_indexes]

    return autocorr_obj_indexes