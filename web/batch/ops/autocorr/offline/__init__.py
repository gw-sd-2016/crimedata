import pysal
import numpy
import sys
import pickle


def autocorrelate(weights_path, csv_file, csv_col):
    # print("WPath = %s" % weights_path)
    weights_matrix_data = pickle.load(open(weights_path, "rb"))
    weights_matrix = pysal.W(weights_matrix_data)

    raw_data = pysal.open(csv_file)
    y_data = numpy.array(raw_data.by_col[csv_col])
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


autocorrelate(sys.argv[1], sys.argv[2], sys.argv[3])