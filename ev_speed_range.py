# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 19:17:33 2018

@author: Louis
"""
import chargespeeds as csp


class electricVehicle:
    def powerCont(self):
        return self.power_cont

    def powerRoll(self):
        p_r = self.weight * 9.81 * self.coeff_roll * self.speed
        return p_r

    def powerAero(self):
        p_a = 0.5 * 1.2 * self.coeff_drag * self.frontal_area * self.speed**3
        return p_a

    def powerTotal(self):
        p = self.powerRoll() + self.powerCont() + self.powerAero()
        if hasattr(self, 'eff_discharge'):
            p = p/self.eff_discharge
        return p


time_start_stop = 150


def bestSpeed(car, km):
    n_charges = 0
    t_old = 0
    t_new = 0
    v_drive = 0
    quitnext = 0
    while 1:
        if (t_new <= t_old or t_old == 0):
            t_old = t_new
            n_best = n_charges-1
            v_best = v_drive
        [t_new, v_drive] = bestTimenCH(car, km, n_charges)
        n_charges += 1
        if t_old <= t_new and t_old != 0:
            quitnext += 1
        else:
            quitnext = 0
        if quitnext > 1:
            break
    v_opt = km*1000/t_old
    return [v_opt, v_best, n_best]


def bestTimenCH(car, km, n_charges):
    test_speed = car.speed_min
    t_old = 0
    t_new = 0
    t_chg = 0
    soc_end = 0
    while (t_old >= t_new or t_old == 0) and test_speed <= car.speed_max:
        if t_old == 0 or t_new <= t_old:
            t_old = t_new
            v_d = test_speed - 0.1
        E_cons = Power(car, test_speed)*km*1000/test_speed
        if E_cons > (((car.soc_start-car.soc_min)/100)
                     + n_charges*((100-car.soc_min)/100))*3600000*car.capacity:
            t_new = 0
        else:
            if E_cons > ((car.soc_start-car.soc_min)/100)*car.capacity*3600000:
                E_to_charge = E_cons-((car.soc_start-car.soc_min)/100)*car.capacity*3600000
                if n_charges != 0:
                    E_per_charge = E_to_charge/n_charges
                    soc_end = car.soc_min + 100*(E_per_charge/3600000/car.capacity)
                    t_end = csp.linInterpolate(car.chargespeeds, soc_end)
                    t_start = csp.linInterpolate(car.chargespeeds, car.soc_min)
                    t_chg = n_charges*(t_end-t_start)*car.capacity/100
                else:
                    t_chg = 0
                if t_chg < 0:
                    t_chg = 0
            t_new = (n_charges+1)*time_start_stop + t_chg + 1000*km/test_speed
        test_speed = test_speed + 0.1
    return [t_old, v_d]


def Power(car, speed):
    speed_old = car.speed
    car.speed = speed
    p = car.powerTotal()
    car.speed = speed_old
    return p
