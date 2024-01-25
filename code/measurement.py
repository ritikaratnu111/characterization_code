import constants
from innovus_reader import InnovusPowerParser
import logging

class Power():
    def __init__(self):
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

class Net():
    def __init__(self):
        self.active = 0
        self.inactive = 0
        self.total = 0
        self.tile_nets = {}

class Measurement():
    def __init__(self,window=None):
        self.window = window if window is not None else {}
        self.power = Power()
        self.energy = Energy()
        self.factor = 1

    def set_window(self,window):
        self.window = window

    def set_factor(self,factor):
        self.factor = factor

    def read_power(self,reader,file,signals):
        reader.update_nets(file)
        reader.set_active_nets(signals)
        reader_power, self.nets = reader.get_power(signals)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.switching + self.power.switching + self.power.leakage

    def read_inactive_power(self,reader,file,signals):
        reader.update_nets(file)
        reader.set_active_nets(signals)
        reader_power, self.nets = reader.get_power(signals)
        self.power.internal = 0
        self.power.switching = 0
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.switching + self.power.switching + self.power.leakage

    def read_remaining_power(self,reader,file,tiles):
        reader.update_nets(file)
        reader_power, self.nets = reader.get_remaining_power(tiles)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.switching + self.power.switching + self.power.leakage

    def read_cell_power(self,reader,file,tiles):
        reader.update_nets(file)
        logging.info("Reading total power for %s", tiles)
        reader_power, self.nets = reader.get_cell_power(tiles)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.switching + self.power.switching + self.power.leakage

    def get_energy(self):
        self.energy.internal = self.power.internal * self.window ["clock_cycles"] / self.factor 
        self.energy.switching = self.power.switching * self.window["clock_cycles"] / self.factor
        self.energy.leakage = self.power.leakage * self.window["clock_cycles"] 
        self.energy.total = self.energy.internal + self.energy.switching + self.energy.leakage

    def add_power(self,measurement):
        self.power.internal  += measurement.power.internal
        self.power.switching += measurement.power.switching
        self.power.leakage   += measurement.power.leakage
        self.power.total     += measurement.power.total

    def add_energy(self,measurement):
        self.energy.internal += measurement.energy.internal
        self.energy.switching += measurement.energy.switching
        self.energy.leakage += measurement.energy.leakage
        self.energy.total += measurement.energy.total

    def average(self,prev_measurement, measurement, count):
        self.power.internal = (prev_measurement.power.internal * count + measurement.power.internal) / (count + 1)
        self.power.switching = (prev_measurement.power.switching * count + measurement.power.switching) / (count + 1)
        self.power.leakage = (prev_measurement.power.leakage * count + measurement.power.leakage) / (count + 1)
        self.power.total = (prev_measurement.power.total * count + measurement.power.total) / (count + 1)
        self.energy.internal = (prev_measurement.energy.internal * count + measurement.energy.internal) / (count + 1)
        self.energy.switching = (prev_measurement.energy.switching * count + measurement.energy.switching) / (count + 1)
        self.energy.leakage = (prev_measurement.energy.leakage * count + measurement.energy.leakage) / (count + 1)
        self.energy.total = (prev_measurement.energy.total * count + measurement.energy.total) / (count + 1)

    def diff(self,measurement1, measurement2):
        if(measurement1.power.internal == 0):
            self.power.internal = 0
            self.energy.internal = 0
        else:
            self.power.internal = (measurement1.power.internal - measurement2.power.internal) * 100/measurement1.power.internal
            self.energy.internal = (measurement1.energy.internal - measurement2.energy.internal) * 100/measurement1.energy.internal
        if(measurement1.power.switching == 0):
            self.power.switching = 0
            self.energy.switching = 0
        else:
            self.power.switching = (measurement1.power.switching - measurement2.power.switching) * 100/measurement1.power.switching
            self.energy.switching = (measurement1.energy.switching - measurement2.energy.switching) * 100/measurement1.energy.switching
        if(measurement1.power.leakage == 0):
            self.power.leakage = 0
            self.energy.leakage = 0
        else:
            self.power.leakage = (measurement1.power.leakage - measurement2.power.leakage) * 100/measurement1.power.leakage
            self.energy.leakage = (measurement1.energy.leakage - measurement2.energy.leakage) * 100/measurement1.energy.leakage
        if(measurement1.power.total == 0):
            self.power.total = 0
            self.energy.total = 0
        else:
            self.power.total = (measurement1.power.total - measurement2.power.total) * 100/measurement1.power.total
            self.energy.total = (measurement1.energy.total - measurement2.energy.total) * 100/measurement1.energy.total

    def diff_energy(self,measurement1, measurement2):
        if(measurement1.energy.internal == 0):
            self.energy.internal = 0
        else:
            self.energy.internal = (measurement1.energy.internal - measurement2.energy.internal) * 100/measurement1.energy.internal
        if(measurement1.energy.switching == 0):
            self.energy.switching = 0
        else:
            self.energy.switching = (measurement1.energy.switching - measurement2.energy.switching) * 100/measurement1.energy.switching
        if(measurement1.energy.leakage == 0):
            self.energy.leakage = 0
        else:
            self.energy.leakage = (measurement1.energy.leakage - measurement2.energy.leakage) * 100/measurement1.energy.leakage
        if(measurement1.energy.total == 0):
            self.energy.total = 0
        else:
            self.energy.total = (measurement1.energy.total - measurement2.energy.total) * 100/measurement1.energy.total

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
