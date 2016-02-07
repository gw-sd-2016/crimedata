from spatial.models import Incident, CrimeType, LocationAlias
import csv
# from spatial.utils import *
from web import settings

def import_gwupd_csv(filepath=settings.GWUPD_DATA_CSV_PATH):
    with open(filepath) as updcsv:
        reader = csv.DictReader(updcsv)

        idx = 0
        csvrows = [row for row in reader]
        all_locations = LocationAlias.objects.all()
        unknown_locations = []

        while idx < (len(csvrows) - 1):
            crime_header = csvrows[idx]
            crime_detail = csvrows[idx + 1]['CType']

            if str(crime_header['Date2']).strip() in ("Occurred", "", None):
                # Invalid/non-data row
                idx += 2
                continue
            else:
                # Get the crime type record or create if this is a new crime type
                # TODO: Potentially refactor to support multiple crime types
                ctype = crime_header['CType'].strip().replace("/ ", "/").replace(" /", "/")   # .replace(" ","")
                try:
                    db_ctype = CrimeType.objects.get(friendly_name__iexact=ctype)
                except CrimeType.DoesNotExist:
                    print("Ctype '%s' doesn't exist, creating..." % ctype)
                    db_ctype = CrimeType.objects.create(friendly_name=ctype, severity=100)

                # Get the location record for this item or bail if it doesn't exist
                loc_name = crime_header['Building']
                try:
                    db_location = next(loc for loc in all_locations if loc_name in loc.all_names)
                except StopIteration: # No record found
                    if loc_name not in unknown_locations:
                        unknown_locations.append(loc_name)
                    idx += 2
                    continue

                # Incident.objects.create(
                #     import_source="ARM",
                #     date_time=crime_header[''],
                #     incident_type=db_ctype,
                #     narrative=crime_detail,
                #     point = db_location.point,
                # )

                # print("%s => %s" % (crime_header['CType'], crime_detail))

                idx += 2

        print("%d Rows imported" % idx)
        print("The following locations were not found:")
        for x in unknown_locations:
            print(x)