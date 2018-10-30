# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:09:47 2018

@author: Louis
"""
kona_batt_50 = [[0, 43], [10, 44], [12, 45], [20, 46], [40, 47], [60, 47],
                [71, 49], [72, 38], [76, 38], [78, 26],
                [87, 25], [89, 24], [91, 19], [95, 10], [100, 1]]

kona_batt_175 = [[0, 71], [10, 72], [12, 73], [20, 75], [40, 77], [42, 70],
                 [52, 71], [55, 57], [71, 59], [72, 38], [76, 38], [78, 26],
                 [87, 25], [89, 24], [91, 19], [95, 10], [100, 1]]

ioniq_batt_50 = [[0, 42], [10, 43], [30, 45], [40, 46], [60, 47], [79, 49],
                 [83, 35], [84, 22], [92, 22], [95, 10], [100, 1]]

ioniq_batt_175 = [[0, 61], [70, 68], [77, 69], [79, 55], [83, 40], [84, 22],
                  [92, 22], [95, 10], [100, 1]]

model_3_batt = [[0, 29], [18, 108], [35, 107], [46, 100], [55, 86], [63, 70],
                [85, 33], [100, 1]]

czero_batt = [[0, 42], [33, 45], [43, 33], [54, 23], [76, 11],
              [85, 7], [100, 0.5]]


def linInterpolate(batt, value):
    i = 0
    while batt[i+1][0] <= value:
        i += 1
    xw = value-batt[i][0]
    d = (batt[i+1][1]-batt[i][1])/(batt[i+1][0]-batt[i][0])
    tr = d*xw
    ylim = tr + batt[i][1]
    return ylim


# Result has to be multiplied with capacity/100
def power2time(batt):
    a = [i for i in range(0, 101)]
    b = [linInterpolate(batt, i) for i in a[0:100]]  # interpolate kw value per percent SOC
    b = [1/i for i in b]
    c = [sum(b[0:i]) for i in a]  #integrating b
    result = [[i, c[i]*3600]for i in a]  # 3600 from hours to seconds
    return result
