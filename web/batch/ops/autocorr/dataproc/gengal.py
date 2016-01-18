from spatial.models import Subdivision
import uuid
from web import settings
import pickle


def generate_weights(sdiv_set=None):
    PICKLE_VERSION = 2

    if sdiv_set is None:
        sdiv_set = Subdivision.objects.filter(src_file_index__lt=100)

    # print("Got %d SDivs" % len(sdiv_set))

    neighbor_set = dict()
    for subdiv in sdiv_set: # type: Subdivision
        subdiv_neighbors = Subdivision.objects.filter(polygon__touches=subdiv.polygon)
        neighbor_set[subdiv.src_file_index] = [x.src_file_index for x in subdiv_neighbors]

    # print(neighbor_set)
    file_path = "%sgengal_weights_%s.bin" % (settings.TMP_BASE, uuid.uuid4())
    with open(file_path, "wb") as outfile:
        pickle.dump(neighbor_set, outfile, PICKLE_VERSION)

    print("File written to %s" % file_path)
    return file_path