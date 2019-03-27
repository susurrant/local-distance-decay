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


if __name__ == '__main__':
    pass