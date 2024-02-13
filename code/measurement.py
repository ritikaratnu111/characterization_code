import constants
from innovus_reader import InnovusPowerParser
import logging

class Power():
    def __init__(self):
        self.internal = 0
        self.switching = 0
        self.leakage = 0
        self.total = 0

    def update(self, p_avg, T, Tactive, Tinactive, c_internal, c_leakage):
        self.internal = (p_avg['internal'] * T - c_internal * Tinactive) / Tactive
        self.switching = p_avg['switching'] * T / Tactive
        self.leakage = (p_avg['leakage'] * T - c_leakage * Tinactive)/ Tactive
        self.total = self.internal + self.switching + self.leakage

    def add(self,T, t1, t2, p1, p2):
        print(T, t1, t2)
        self.internal = (p1.internal * t1 + p2.internal * t2 ) / T
        self.switching = (p1.switching * t1 + p2.switching * t2 ) / T
        self.leakage = (p1.leakage * t1 + p2.leakage * t2) / T
        self.total = (p1.total * t1 + p2.total * t2) / T

    def diff(self, power1, power2):
        if(power1.internal == 0):
            self.internal = 0
        else:
            self.internal = (power1.internal - power2.internal) * 100/max(power1.internal,power2.internal)
        if(power1.switching == 0):
            self.switching = 0
        else:
            self.switching = (power1.switching - power2.switching) * 100/max(power1.switching,power2.switching)
        if(power1.leakage == 0):
            self.leakage = 0
        else:
            self.leakage = (power1.leakage - power2.leakage) * 100/max(power1.leakage,power2.leakage)
        if(power1.total == 0):
            self.total = 0
        else:
            self.total = (power1.total - power2.total) * 100/max(power1.total,power2.total)

    def set_zero(self):
        self.internal = 0
        self.switching = 0
        self.leakage = 0
        self.total = 0
    
class Energy():
    def __init__(self):
        self.internal =  0
        self.switching = 0
        self.leakage = 0
        self.total = 0

    def update(self, power, T):
        self.internal = power.internal * T
        self.switching = power.switching * T
        self.leakage = power.leakage * T
        self.total = self.internal + self.switching + self.leakage

    def add(self, energy1, energy2):
        self.internal = energy1.internal + energy2.internal
        self.switching = energy1.switching + energy2.switching
        self.leakage = energy1.leakage + energy2.leakage
        self.total = energy1.total + energy2.total

    def diff(self, energy1, energy2):
        if(energy1.internal == 0):
            self.internal = 0
        else:
            self.internal = (energy1.internal - energy2.internal) * 100/max(energy1.internal,energy2.internal)
        if(energy1.switching == 0):
            self.switching = 0
        else:
            self.switching = (energy1.switching - energy2.switching) * 100/max(energy1.switching,energy2.switching)
        if(energy1.leakage == 0):
            self.leakage = 0
        else:
            self.leakage = (energy1.leakage - energy2.leakage) * 100/max(energy1.leakage,energy2.leakage)
        if(energy1.total == 0):
            self.total = 0
        else:
            self.total = (energy1.total - energy2.total) * 100/max(energy1.total,energy2.total)

    def set_zero(self):
        self.internal = 0
        self.switching = 0
        self.leakage = 0
        self.total = 0

class Net():
    def __init__(self):
        self.active = 0
        self.inactive = 0
        self.total = 0
        self.tile_nets = {}

class Measurement():
    def __init__(self):
        self.power = Power()
        self.energy = Energy()
        self.nets = 0
        self.signals = []
        self.p_avg = {}

    def set_measurement(self, reader, signals, T, Tactive, Tinactive, c_internal, c_leakage):
        self.signals = signals
        reader.label_nets(self.signals)
        self.p_avg, self.nets = reader.get_power(self.signals)
        self.power.update(self.p_avg, T, Tactive, Tinactive, c_internal, c_leakage)
        self.energy.update(self.power, Tactive)

    def set_zero(self):
        self.power.set_zero()
        self.energy.set_zero()

    def read_remaining_power(self,reader,file,tiles):
        reader_power, self.nets = reader.get_remaining_power(tiles)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.switching + self.power.switching + self.power.leakage

    def add(self, T, Tactive, Tinactive, m1, m2):
        self.power.add(T, Tactive, Tinactive, m1.power, m2.power)
        self.energy.add(m1.energy, m2.energy)

    def average(self,prev_measurement, measurement, count):
        self.power.internal = (prev_measurement.power.internal * count + measurement.power.internal) / (count + 1)
        self.power.switching = (prev_measurement.power.switching * count + measurement.power.switching) / (count + 1)
        self.power.leakage = (prev_measurement.power.leakage * count + measurement.power.leakage) / (count + 1)
        self.power.total = (prev_measurement.power.total * count + measurement.power.total) / (count + 1)
        self.energy.internal = (prev_measurement.energy.internal * count + measurement.energy.internal) / (count + 1)
        self.energy.switching = (prev_measurement.energy.switching * count + measurement.energy.switching) / (count + 1)
        self.energy.leakage = (prev_measurement.energy.leakage * count + measurement.energy.leakage) / (count + 1)
        self.energy.total = (prev_measurement.energy.total * count + measurement.energy.total) / (count + 1)

    def diff(self,m1, m2):
        self.power.diff(m1.power, m2.power)
        self.energy.diff(m1.energy, m2.energy)

    def adjust_power(self):
        self.power.internal  = self.power.internal/self.window['clock_cycles'] 
        self.power.switching = self.power.switching/self.window['clock_cycles']
        self.power.leakage   = self.power.leakage/self.window['clock_cycles']
        self.power.total     = self.power.total/self.window['clock_cycles']


    def log_power(self):
        logging.info('              %s %s %s %s',
         '{:.12f}'.format(self.power.internal).ljust(20),
         '{:.12f}'.format(self.power.switching).ljust(20),
         '{:.12f}'.format(self.power.leakage).ljust(20),
         '{:.12f}'.format(self.power.total).ljust(20))
    
    def log_energy(self, type=""):
        logging.info('              %s %s %s %s',
         '{:.12f}'.format(self.energy.internal).ljust(20),
         '{:.12f}'.format(self.energy.switching).ljust(20),
         '{:.12f}'.format(self.energy.leakage).ljust(20),
         '{:.12f}'.format(self.energy.total).ljust(20))
    
    def log(self):
        self.log_power()
        self.log_energy()


class MeasurementSet():
    def __init__(self):
        self.active = Measurement()
        self.inactive = Measurement()
        self.predicted = Measurement()
        self.actual = Measurement()
        self.error = Measurement()
        self.T = 0
        self.Tactive = 0
        self.Tinactive = 0

    def set_T(self, total_window, active_window, inactive_window):
        self.T = total_window["clock_cycles"] if total_window else 0
        self.Tactive = active_window["clock_cycles"] if active_window else 0
        self.Tinactive = inactive_window["clock_cycles"] if inactive_window else 0

    def set_inactive(self,c_internal,c_leakage):
        print("Setting inactive power: ", c_internal, c_leakage)
        self.inactive.power.internal = c_internal
        self.inactive.power.switching = 0
        self.inactive.power.leakage = c_leakage
        self.inactive.power.total = self.inactive.power.internal + self.inactive.power.switching + self.inactive.power.leakage
        self.inactive.energy.update(self.inactive.power, self.Tinactive)

    def set_active(self, reader, signals):
        self.active.set_measurement(
            reader, signals,
            self.T, self.Tactive, self.Tinactive, 
            self.inactive.power.internal, self.inactive.power.leakage
            )

    def set_predicted(self):
        self.predicted.add(
            self.T, self.Tactive, self.Tinactive, self.active, self.inactive
            )
        self.predicted.energy.update(self.predicted.power, self.T)
    
    def set_actual(self, reader, signals):
        self.actual.set_measurement(
            reader, signals,
            self.T, self.T, 0, 
            self.inactive.power.internal, self.inactive.power.leakage
            )
    
    def set_error(self):
        self.error.diff(self.actual, self.predicted)

    def remvove_lables(self):
        self.a

    def log(self):
        print("Inactive Measurement:")
        self.inactive.log()
        print("Active Measurement:")
        self.active.log()
        print("Predicted Measurement:")
        self.predicted.log()
        print("Actual Measurement:")
        self.actual.log()
        print("Error Measurement:")
        self.error.log()
