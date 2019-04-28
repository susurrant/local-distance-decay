# -*- coding: utf-8 -*-：

import csv
import numpy as np
import collections
import matplotlib.pyplot as plt

def taxi_data(data_file, flow_file, feature_file, col_num, threshold=0):
    features = {}  # [row, col, attract, pull]

    flows = {}
    with open(data_file, 'r') as f:
        f.readline()
        line = f.readline().strip()
        while line:
            d1 = line.split(',')
            d2 = f.readline().strip().split(',')
            if d1[1] == '1' and d2[1] == '1':
                k = (d1[-1], d2[-1])
                if k not in flows:
                    flows[k] = 0
                flows[k] += 1
            line = f.readline().strip()

    with open(flow_file, 'w', newline='') as rf:
        sheet = csv.writer(rf, delimiter='\t')
        sheet.writerow(['ogid', 'dgid', 'm'])
        for g, m in flows.items():
            if m >= threshold:
                sheet.writerow([g[0], g[1], m])
                if g[0] not in features:
                    features[g[0]] = [g[0], int(g[0]) // col_num, int(g[0]) % col_num, 0, 0]
                if g[1] not in features:
                    features[g[1]] = [g[1], int(g[1]) // col_num, int(g[1]) % col_num, 0, 0]
                features[g[0]][4] += m  # pick-up:  pull
                features[g[1]][3] += m  # drop-off: attract

    with open(feature_file, 'w', newline='') as rf:
        sheet = csv.writer(rf, delimiter='\t')
        sheet.writerow(['gid', 'row', 'col', 'attract', 'pull'])
        for v in features.values():
            sheet.writerow(v)


if __name__ == '__main__':
    col_num = 40#30#15#59
    taxi_data('data/sj_051317_750m.txt', 'data/flow_051317_750m.txt', 'data/feature_051317_750m.txt', col_num, threshold=25)
    '''
    data = np.loadtxt('data/flow_051317_500m.txt', skiprows=1, delimiter='\t', dtype=np.uint16)
    r = collections.Counter(data[:, 2])
    X = []
    Y = []
    for x, y in r.items():
        X.append(x)
        Y.append(y)

    plt.figure()
    plt.bar(X, Y)
    plt.show()
    '''