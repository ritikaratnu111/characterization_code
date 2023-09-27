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

    def set_window(self,window):
        self.window = window

    def read_power(self,file,signals):
        reader = InnovusPowerParser(file)
        reader.set_nets()
        reader.set_active_nets(signals)
        reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def read_remaining_power(self,file,tile,active_components):
        reader = InnovusPowerParser(file)
        reader.set_nets()
        for component in active_components:
            signals = component.signals
            reader.set_active_nets(signals)
        reader_power, active_nets = reader.get_remaining_power(tile)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def read_total_power(self,file,tile):
        reader = InnovusPowerParser(file)
        reader.set_nets()
        reader_power, active_nets = reader.get_total_power(tile)
        self.power.internal = reader_power['internal']
        self.power.switching = reader_power['switching']
        self.power.leakage = reader_power['leakage']
        self.power.total = self.power.internal + self.power.switching + self.power.leakage

    def get_energy(self):
        self.energy.internal = self.power.internal * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.switching = self.power.switching * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.leakage = self.power.leakage * self.window['clock_cycles'] * constants.CLOCK_PERIOD
        self.energy.total = self.power.total * self.window['clock_cycles'] * constants.CLOCK_PERIOD

    def add_measurement(self,measurement):
        """
        Add the give energy, we don't add power because power of all components is not addtitive energy is additive
        """
        self.energy.internal += measurement.energy.internal
        self.energy.switching += measurement.energy.switching
        self.energy.leakage += measurement.energy.leakage
        self.energy.total += measurement.energy.total

    def log(self):
        logging.info('%s %s %s %s %s',
         '{}'.format(self.window['start']).ljust(20),
         '{:.3f}'.format(self.power.internal).ljust(20),
         '{:.3f}'.format(self.power.switching).ljust(20),
         '{:.3f}'.format(self.power.leakage).ljust(20),
         '{:.3f}'.format(self.power.total).ljust(20))
        logging.info('%s %s %s %s %s',
         '{}'.format(self.window['start']).ljust(20),
         '{:.3f}'.format(self.energy.internal).ljust(20),
         '{:.3f}'.format(self.energy.switching).ljust(20),
         '{:.3f}'.format(self.energy.leakage).ljust(20),
         '{:.3f}'.format(self.energy.total).ljust(20))
        print(f"Power: internal: {self.power.internal} switching: {self.power.switching} leakage: {self.power.leakage} total: {self.power.total}")
        print(f"Energy: internal: {self.energy.internal} switching: {self.energy.switching} leakage: {self.energy.leakage} total: {self.energy.total}")
