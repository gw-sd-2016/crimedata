from spatial.models import Incident, CrimeType, LocationAlias, LocationAliasSecondaryName
import csv
# from spatial.utils import *
from web import settings
from batch.geocode import addr2coord
from django.contrib.gis.geos import GEOSGeometry
import re
from datetime import datetime

def import_gwupd_csv(filepath=settings.GWUPD_DATA_CSV_PATH):
    addr_re = '(?P<addr>.*)(?:,\s?N(?:\s?|\.?)W(?:\.?|\s?))(?:.*)'
    addr_regex = re.compile(addr_re)

    with open(filepath) as updcsv:
        reader = csv.DictReader(updcsv)

        idx = 0
        csvrows = [row for row in reader]
        all_locations = [x for x in LocationAlias.objects.all()]
        unknown_locations = []

        while idx < (len(csvrows) - 1):
            crime_header = csvrows[idx]
            crime_detail = csvrows[idx + 1]['CType']
            inc_location = None

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
                loc_name_rex = None
                try:
                    loc_name_rex = addr_regex.match(loc_name).group("addr")
                    loc_name_rex = "%s, N.W." % loc_name_rex
                except:
                    loc_name_rex = loc_name

                if loc_name_rex is None or str(loc_name_rex).strip() == "":
                    loc_name_rex = loc_name

                if loc_name not in unknown_locations:
                    try:
                        db_location = next(loc for loc in all_locations if loc_name_rex in loc.all_names)

                        if loc_name not in db_location.all_names:
                            LocationAliasSecondaryName.objects.create(
                                location_alias = db_location,
                                display_name = loc_name,
                            )

                        inc_location = db_location
                    except StopIteration: # No record found
                        # unknown_locations.append(loc_name)
                        addr_fmt = "%s, Washington DC, 20052"
                        geocode_input = addr_fmt % loc_name_rex

                        try:
                            geocode_raw = addr2coord(geocode_input)
                            geocode_result = geocode_raw['results'][0]['geometry']['location']
                            geocode_lat = geocode_result['lat']
                            geocode_lng = geocode_result['lng']
                        except:
                            unknown_locations.append(loc_name)

                            idx += 2
                            continue

                        geos_coord_str = "POINT(%s %s)" % (geocode_lng, geocode_lat)
                        geos_coord = GEOSGeometry(geos_coord_str)
                        print(geocode_raw)
                        print(geocode_input, geocode_result, geocode_lat, geocode_lng)

                        new_loc = LocationAlias.objects.create(
                            point=geos_coord,
                            primary_display_name=loc_name_rex
                        )
                        all_locations.append(new_loc)
                        inc_location = new_loc

                    # https://regex101.com/r/xH4aZ0/5


                parsed_date = None
                try:
                    parsed_date = datetime.strptime(crime_header['Date'], "%m/%d/%Y")
                except:
                    pass

                if inc_location is not None and parsed_date is not None:
                    Incident.objects.create(
                        import_source="ARM",
                        date_time=parsed_date.isoformat(" "),
                        incident_type=db_ctype,
                        narrative=crime_detail,
                        point = inc_location.point,
                    )
                else:
                    print("Skip! %d" % idx)

                # print("%s => %s" % (crime_header['CType'], crime_detail))

                idx += 2

        print("%d Rows imported" % idx)
        print("The following locations were not found:")
        for x in unknown_locations:
            print(x)