import math
# Autocorrelation and associated helper functions
# Formula used in new_lat/new_lon from here: http://gis.stackexchange.com/a/2980
from spatial.models import Incident
import subprocess

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


def stl_process():
    py_file = "/home/ben/sd/web/batch/ops/autocorr/offline/__init__.py"
    py_cmd = "python2 %s" % py_file

    autocorr_output = subprocess.getoutput(py_cmd)
    autocorr_obj_indexes = autocorr_output.split(",")
    autocorr_obj_indexes = [int(i) for i in autocorr_obj_indexes]

    return autocorr_obj_indexes