import pysal
import numpy
import sys
import pickle


def autocorrelate(weights_path):
    # print("WPath = %s" % weights_path)
    base_path = "/home/ben/sd/app/demo/stl/"

    weights_matrix_data = pickle.load(open(weights_path, "rb"))
    weights_matrix = pysal.W(weights_matrix_data)

    raw_data = pysal.open(base_path + "stl_hom.txt")
    y_data = numpy.array(raw_data.by_col["HR8893"])
    #weights_matrix = pysal.open(base_path + "stl.gal").read()

    local_moran = pysal.Moran_Local(y_data, weights_matrix)

    idx = 0
    sig_vals = []

    for p_val in local_moran.p_sim:
        if p_val < 0.05:
            sig_vals.append(idx)
        idx += 1

    #print(local_moran.p_sim)
    print(",".join(str(p) for p in sig_vals))


autocorrelate(sys.argv[1])