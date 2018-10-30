# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 12:53:21 2018

@author: Louis
"""

import ev_speed_range as esr
import matplotlib.pyplot as plt
import chargespeeds as csp


czero = esr.electricVehicle()
czero.power_cont = 300
czero.weight = 1200
czero.coeff_roll = 0.008
czero.coeff_drag = 0.33
czero.frontal_area = 2.13
czero.eff_discharge = 0.91
czero.speed = 0
czero.capacity = 13.5
czero.speed_min = 50/3.6
czero.speed_max = 130/3.6
czero.soc_min = 10
czero.soc_start = 100
czero.chargespeeds = csp.power2time(csp.czero_batt)

kona_175 = esr.electricVehicle()
kona_175.power_cont = 300
kona_175.weight = 1840
kona_175.coeff_roll = 0.009
kona_175.coeff_drag = 0.29
kona_175.frontal_area = 2.4
kona_175.eff_discharge = 0.95
kona_175.capacity = 64
kona_175.speed = 0
kona_175.speed_min = 50/3.6
kona_175.speed_max = 167/3.6
kona_175.soc_min = 10
kona_175.soc_start = 100
kona_175.chargespeeds = csp.power2time(csp.kona_batt_175)

kona_50 = kona_175
kona_50.chargespeeds = csp.power2time(csp.kona_batt_50)

ioniq_175 = esr.electricVehicle()
ioniq_175.power_cont = 300
ioniq_175.weight = 1520
ioniq_175.coeff_roll = 0.009
ioniq_175.coeff_drag = 0.24
ioniq_175.frontal_area = 2.22
ioniq_175.eff_discharge = 0.95
ioniq_175.capacity = 28
ioniq_175.speed = 0
ioniq_175.speed_min = 50/3.6
ioniq_175.speed_max = 165/3.6
ioniq_175.soc_min = 10
ioniq_175.soc_start = 100
ioniq_175.chargespeeds = csp.power2time(csp.ioniq_batt_175)

ioniq_50 = esr.electricVehicle()
ioniq_50.__dict__.update(ioniq_175.__dict__)
ioniq_50.chargespeeds = csp.power2time(csp.ioniq_batt_50)

model3 = esr.electricVehicle()
model3.power_cont = 550
model3.weight = 1730
model3.coeff_roll = 0.01
model3.coeff_drag = 0.21
model3.frontal_area = 2.28
model3.eff_discharge = 0.95
model3.capacity = 75
model3.speed = 0
model3.speed_min = 50/3.6
model3.speed_max = 200/3.6
model3.soc_min = 15
model3.soc_start = 100
model3.chargespeeds = csp.power2time(csp.model_3_batt)

kms = [i for i in range(50, 1000)]


ioniq_result_50 = [esr.bestSpeed(ioniq_50, i) for i in kms]
ioniq_result_175 = [esr.bestSpeed(ioniq_175, i) for i in kms]
# czero_result = [esr.bestSpeed(czero, i) for i in kms]
# model3_result = [esr.bestSpeed(model3, i) for i in kms]
# kona_result = [esr.bestSpeed(kona, i) for i in kms]


def plotStrat(result, col, name):
    fig2, ax2 = plt.subplots()
    fig2.set_dpi(100)
    fig2.set_size_inches(16, 10)
    ax2.plot(kms, [i[0]*3.6 for i in result], color=col,
             label='Durchschnittsgeschwindigkeit')
    ax2.plot(kms, [i[1]*3.6 for i in result], color=col,
             linestyle='dashed', label='Fahrgeschwindigkeit')
    ax2.grid()
    ax2.set(xlabel='Distanz in km', ylabel='Geschwindigkeit in km/h',
            title='Ladestrategie '+name)
    ax3 = ax2.twinx()
    ax3.plot(kms, [i[2] for i in result], color='0.5', label='Anzahl Ladungen')
    ax3.set(ylabel='Anzahl Ladungen')
    lines, labels = ax2.get_legend_handles_labels()
    lines2, labels2 = ax3.get_legend_handles_labels()
    ax3.legend(lines + lines2, labels + labels2, loc='upper center')

    plt.show
    return


# arg format [result,name,color,linestyle]
# Example: plotComparison('Vergleich',[ioniq_result,'Ioniq 175kW','b','-'],
#                         [kona_result,'Kona 175kW','r','-'])

def plotComparison(headline, *args):
    fig, ax = plt.subplots()
    fig.set_dpi(100)
    fig.set_size_inches(16, 10)
    for arg in args:
        ax.plot(kms, [k[0] for k in arg[0]], color=arg[2],
                label=arg[1], linestyle=arg[3])
    ax.set(xlabel='Distanz in km', ylabel='Geschwindigkeit in km/h',
           title=headline)
    ax.grid()
    ax.legend()
    plt.show
