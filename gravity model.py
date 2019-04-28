
import numpy as np
from sklearn.linear_model import LinearRegression
import csv
from tqdm import tqdm


def dis(x0, y0, x1, y1):
    return np.sqrt((float(x1) - float(x0)) ** 2 + (float(y1) - float(y0)) ** 2)


def grid_dis(i, j, colnum):
    x0 = int(i) % colnum
    y0 = int(i) // colnum
    x1 = int(j) % colnum
    y1 = int(j) // colnum
    return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def global_gravity_model(flows, features):
    Y = []
    X = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for k in flows:
            if k[0] == k[1]:
                continue
            Y.append(np.log(k[2]))
            X.append([np.log(features[k[0]][2]), np.log(features[k[1]][2]),
                      np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])
    elif feature_size == 4:
        for k in flows:
            if k[0] == k[1]:
                continue
            Y.append(np.log(k[2]))
            X.append([np.log(features[k[0]][3]), np.log(features[k[1]][2]),
                      np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])

    reg = LinearRegression().fit(X, Y)
    beta = reg.coef_
    K = np.e**reg.intercept_

    return beta, K


def log_flow(flows, features):
    Y = []
    X = []
    feature_size = len(list(features.values())[0])
    if feature_size == 3:
        for k in flows:
            if k[0] == k[1]:
                continue
            Y.append(np.log(k[2]))
            X.append([np.log(features[k[0]][2]), np.log(features[k[1]][2]),
                      np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])
    elif feature_size == 4:
        for k in flows:
            if k[0] == k[1]:
                continue
            Y.append(np.log(k[2]))
            X.append([np.log(features[k[0]][3]), np.log(features[k[1]][2]),
                      np.log(dis(features[k[0]][0], features[k[0]][1], features[k[1]][0], features[k[1]][1]))])

    return X, Y


def local_gravity_model(gids, flow_file, feature_file, output_file, colnum, sigma=1):
    flows = np.loadtxt(flow_file, delimiter='\t', skiprows=1, dtype=np.uint32)
    feature_data = np.loadtxt(feature_file, delimiter='\t', skiprows=1, dtype=np.uint32)
    features = dict(zip(feature_data[:, 0], feature_data[:, 1:]))
    X, Y = log_flow(flows, features)

    parameters = []
    for gid in tqdm(gids):
        weights = []
        for k in flows:
            if k[0] == k[1]:
                continue
            d = grid_dis(gid, k[0], colnum)
            weights.append(np.exp(-d**2/(2*sigma**2)))  # Radial basis function kernel
        weights = np.array(weights) / sum(weights)
        reg = LinearRegression().fit(X, Y, weights)
        beta = reg.coef_
        K = np.e ** reg.intercept_
        parameters.append([gid, '%.3f' % beta[0], '%.3f' % beta[1], '%.3f' % beta[2], '%.3f' % K])

    with open(output_file, 'w', newline='') as rf:
        sheet = csv.writer(rf, delimiter=',')
        sheet.writerow('gid,alpha,gamma,beta,K'.split(','))
        for result in parameters:
            sheet.writerow(result)


if __name__ == '__main__':
    flow_file = 'data/flow_051317_750m.txt'
    feature_file = 'data/feature_051317_750m.txt'
    output_file = 'data/lgm_051317_750m.txt'
    colnum = 40#15#59#30
    gids = range(1600)

    local_gravity_model(gids, flow_file, feature_file, output_file, colnum, sigma=1)