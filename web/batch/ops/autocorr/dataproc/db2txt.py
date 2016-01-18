# Helper functions for converting database data into temporary text files to run analysis
from spatial.models import CrimeType, Incident, Subdivision
from batch.ops.autocorr import get_crimes_in_square
from collections import OrderedDict
import csv
import uuid
from web import settings

def generate_txt(crime_type, start_time, end_time):
    """
    :type crime_type: CrimeType
    :param crime_type:
    :param start_time:
    :param end_time:
    :return:
    """

    subdiv_counts = {}

    for sd in Subdivision.objects.all(): # type: Subdivision
        sd_incs = Incident.objects.filter(point__contained=sd.polygon)
        subdiv_counts[sd.src_file_index] = {"idx": sd.src_file_index,
                                            "pk": sd.pk,
                                            "disp": sd.display_name,
                                            "count": sd_incs.count()}

    sorted_subdiv_counts = OrderedDict(sorted(subdiv_counts.items(), key=lambda rec: rec[0]))

    file_path = "%sautocorr_db2txt_%s.csv" % (settings.TMP_BASE, uuid.uuid4())
    with open(file_path, "w", newline="") as csv_file:
        csvout = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        header = ["IDX", "PK", "COUNT", "OVERTIME"]
        csvout.writerow([len(sorted_subdiv_counts), len(header)])
        csvout.writerow(header)
        for key, val in list(sorted_subdiv_counts.items()):
            csvout.writerow(
                [
                    int(key),
                    int(val['pk']),
                    int(val['count']),
                    -1
                ]
            )
            if settings.DEBUG:
                print("%s -> %s - %d" % (key, val['disp'], val['count']))

    print("File written to %s" % file_path)