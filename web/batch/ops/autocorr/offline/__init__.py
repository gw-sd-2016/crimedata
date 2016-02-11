import pysal
import numpy
import sys
import pickle
import csv


def autocorrelate(weights_path, csv_file, csv_col):
    # print("WPath = %s" % weights_path)
    weights_matrix_data = pickle.load(open(weights_path, "rb"))
    weights_matrix = pysal.W(weights_matrix_data)

    row2id = dict()
    with open(csv_file) as CSV:
        next(CSV)
        reader = csv.DictReader(CSV)

        idx = 0
        for row in reader:
            row2id[int(idx)] = int(row['IDX'])
            idx += 1

    # for k, v in row2id.iteritems():
    #     print("%d => %d" % (k,v))
    #
    raw_data = pysal.open(csv_file)

    y_data = numpy.array(raw_data.by_col[csv_col])
    #weights_matrix = pysal.open(base_path + "stl.gal").read()

    local_moran = pysal.Moran_Local(y_data, weights_matrix)

    idx = 0
    sig_vals = []

    for p_val in local_moran.p_sim:
        if p_val < 0.05:
            sig_vals.append(row2id[int(idx)])
        idx += 1

    #print(local_moran.p_sim)
    print(",".join(str(p) for p in sig_vals))


autocorrelate(sys.argv[1], sys.argv[2], sys.argv[3])