import math
# Autocorrelation and associated helper functions
# Formula used in new_lat/new_lon from here: http://gis.stackexchange.com/a/2980
from models import Incident

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
