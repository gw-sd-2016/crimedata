import csv
import re
import datetime
import warnings
from batch.importer import ImporterBase
from spatial.models import Incident

SOURCE_FILE = "/home/ben/sd/web/static/chicago/chicago_2015.csv"


class ChicagoImporter(ImporterBase):
    def __init__(self):
        self.set_source_code("CHI")

    def load_data(self, *args, **kwargs):
        # 11/07/2015 11:52:00 PM
        chicago_datetime_re = '(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+) (?P<hour>\d+)\:(?P<min>\d+)\:(?P<sec>\d+) (?P<tz>.+)'
        dt_parse = re.compile(chicago_datetime_re)

        with open(SOURCE_FILE, newline='') as CSV:
            crimereader = csv.reader(CSV, delimiter=",", quotechar='"')
            next(crimereader)  # Throw away headers

            max_rows = int(kwargs["max_rows"]) if kwargs["max_rows"] is not None else -1
            i = max_rows
            import_count = 0

            for row in crimereader:
                if i == 0:
                    break

                raw_date_time = row[2]
                parsed_time = dt_parse.match(raw_date_time)
                # print("Got -> %s " % (parsed_time.group("sec")))
                date_time = datetime.datetime(
                    int(parsed_time.group("year")),
                    int(parsed_time.group("month")),
                    int(parsed_time.group("day")),
                    int(parsed_time.group("hour")),
                    int(parsed_time.group("min")),
                    int(parsed_time.group("sec")),
                )

                lat = float(row[19]) if row[19] != "" else 0
                lon = float(row[20]) if row[19] != "" else 0
                type = 1 if row[8] == "true" else 2
                narrative = str("%s %s" % (row[5], row[6])).title()

                # print("Lat: %s \n Lon: %s" % (lat, lon))

                if lat != 0 and lon != 0:
                    self.insert_record(type, date_time, lat, lon, narrative)
                    i -= 1
                    import_count += 1

            print(self.__module__ + "." + self.__class__.__name__ +
                  ": imported " + str(import_count) + " records")


class TestChicago(object):
    def __init__(self, max_rows=None):
        for i in Incident.objects.filter(import_source="CHI"):
            i.delete()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            C = ChicagoImporter()
            C.load_data(max_rows=max_rows)
