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

class Measurement():
    def __init__(self,window=None):
        self.window = window if window is not None else {}
        self.power = Power()
        self.energy = Energy()
        self.nets = 0

    def set_window(self,window):
        self.window = window

    def read_power(self,reader,file,signals):
        reader.update_nets(file)
        reader.set_active_nets(signals)
        reader_power, self.nets = reader.get_power(signals)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def read_remaining_power(self,reader,file,tiles):
        reader.update_nets(file)
        reader_power, self.nets = reader.get_remaining_power(tiles)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def read_total_power(self,reader,file,tiles):
        reader.update_nets(file)
        reader_power, self.nets = reader.get_total_power(tiles)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def get_energy(self):
        self.energy.internal = self.power.internal * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.switching = self.power.switching * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.leakage = self.power.leakage * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.total = self.power.total * self.window['clock_cycles'] * constants.CLOCK_PERIOD

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

    def adjust_power(self):
        self.power.internal  = self.power.internal/self.window['clock_cycles'] 
        self.power.switching = self.power.switching/self.window['clock_cycles']
        self.power.leakage   = self.power.leakage/self.window['clock_cycles']
        self.power.total     = self.power.total/self.window['clock_cycles']


    def log_power(self):
        logging.info('[%s %s] %s    %s %s %s %s',
         '{}'.format(self.window['start']).ljust(1),
         '{}'.format(self.window['end']).ljust(1),
         '{}'.format(self.nets).ljust(2),
         '{:.3f}'.format(self.power.internal).ljust(20),
         '{:.6f}'.format(self.power.switching).ljust(20),
         '{:.3f}'.format(self.power.leakage).ljust(20),
         '{:.3f}'.format(self.power.total).ljust(20))
    
    def log_energy(self):
        logging.info('[%s %s] %s     %s %s %s %s',
         '{}'.format(self.window['start']).ljust(1),
         '{}'.format(self.window['end']).ljust(1),
         '{}'.format(self.nets).ljust(2),
         '{:.3f}'.format(self.energy.internal).ljust(20),
         '{:.6f}'.format(self.energy.switching).ljust(20),
         '{:.3f}'.format(self.energy.leakage).ljust(20),
         '{:.3f}'.format(self.energy.total).ljust(20))
