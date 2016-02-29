import pickle
import uuid

from spatial.models import Subdivision
from web import settings
from django.contrib.gis.measure import D


def generate_weights(sdiv_set=None):
    PICKLE_VERSION = 2

    if sdiv_set is None:
        sdiv_set = Subdivision.objects.filter(src_file_index__gt=100)
        #sdiv_set = Subdivision.objects.filter()

    print("Got %d SDivs" % len(sdiv_set))

    neighbor_set = dict()
    i = 0
    for subdiv in sdiv_set: # type: Subdivision
        i += 1
        #subdiv_neighbors = Subdivision.objects.filter(polygon__touches=subdiv.polygon) # type: list[Subdivision]
        subdiv_neighbors = Subdivision.objects.filter(
            pk__in=sdiv_set,
            poly_centroid__distance_lte=(subdiv.poly_centroid, D(mi=1))
        ).distance(subdiv.poly_centroid).order_by('distance')[:4]

        if len(subdiv_neighbors) < 4:
            print("Warn: %d / %d => Neighbor set size %d, should be 4" % (i, len(sdiv_set), len(subdiv_neighbors)))
        neighbor_set[subdiv.src_file_index] = [x.src_file_index for x in subdiv_neighbors]

    # print(neighbor_set)
    file_path = "%sgengal_weights_%s.bin" % (settings.TMP_BASE, uuid.uuid4())
    with open(file_path, "wb") as outfile:
        pickle.dump(neighbor_set, outfile, PICKLE_VERSION)

    print("File written to %s" % file_path)
    return file_path