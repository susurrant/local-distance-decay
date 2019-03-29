# -*- coding: utf-8 -*-：

import numpy as np
import csv


# 出租车数据处理
def taxi_data(data_file, out_file):
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

    with open(out_file, 'w', newline='') as rf:
        sheet = csv.writer(rf, delimiter='\t')
        sheet.writerow(['ogid', 'dgid', 'm'])
        for g, m in flows.items():
            sheet.writerow([g[0], g[1], m])

def grid_dis(i, j, colnum):
    x0 = int(i) % colnum
    y0 = int(i) // colnum
    x1 = int(j) % colnum
    y1 = int(j) // colnum
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def gravity_model(flows, attraction, colnum):
    Y = []
    X = []
    for k in flows:
        if k[2]:
            #print(k)
            Y.append(np.log(attraction[k[0]]*attraction[k[1]]/k[2]))
            X.append(np.log(grid_dis(k[0], k[1], colnum)))

    p = np.polyfit(X, Y, 1)
    beta = p[0]
    K = np.e**(-p[1])
    '''
    p1 = plt.scatter(X, Y, marker='.', color='green', s=10)
    plt.show()
    '''
    return beta, K


if __name__ == '__main__':
    pass