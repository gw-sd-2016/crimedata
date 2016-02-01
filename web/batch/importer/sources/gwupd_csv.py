from spatial.models import Incident
import csv
from spatial.utils import *

def import_gwupd_csv(filepath):
    with open(filepath) as updcsv:
        reader = csv.DictReader(updcsv)

        idx = 0
        for line in reader:
            type = line["CTYPE"]
            row_id = line["RID"]
            location_friendly_name = line["LOC_FN"]
            inc_date = line["CDATE"]

            loc_lat, loc_lon = loc2latlon(location_friendly_name)

            Incident.objects.create(
                date_time=inc_date,
                incident_Type = type,
                narrative = "%S/%S" % (row_id, idx),
                import_source = "ARM",
            )

            idx += 1