import constants
from innovus_reader import InnovusPowerParser
import logging

class Power():
    def __init__(self,window=None):
        self.window = window if window is not None else {}
        self.internal = 0
        self.switching = 0
        self.leakage = 0
        self.total = 0

class Energy():
    def __init__(self):
        self.window = 0
        self.internal =  0
        self.switching = 0
        self.leakage = 0
        self.total = 0

class Net():
    def __init__(self):
        self.active = 0
        self.inactive = 0
        self.total = 0

class ComponentProfiler():
    def __init__(self):
        self.active_window = []
        self.inactive_window = []
        self.total_window = {}
        self.active_power = []
        self.inactive_power = []
        self.per_cycle_power = []

    def init(self, active_window, inactive_window,total_window):
        self.active_window = active_window
        self.inactive_window = inactive_window
        self.total_window = total_window
        self.init_active_power()
        self.init_inactive_power()
        self.init_per_cycle_power()

    def init_active_power(self): 
        self.active_power = [Power(window=window) for window in self.active_window]

    def init_inactive_power(self):
        self.inactive_power = [Power(window=window) for window in self.inactive_window]

    def init_per_cycle_power(self):
        windows = []
        current_start = self.total_window['start']
        while current_start < self.total_window['end']:
            windows.append({'start': current_start, 'end': current_start + constants.CLOCK_PERIOD})
            current_start += constants.CLOCK_PERIOD        
        self.per_cycle_power = [Power(window=window) for window in windows]

    def set_per_cycle_power(self,signals):
        for power in self.per_cycle_power:
            file = f"./vcd/{power.window['start']}.vcd.pwr"
            print(f"File: {file}")
            reader = InnovusPowerParser(file)
            reader.set_nets()
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage
            #Log in the power and the component name
            logging.info('%s %s %s %s',
             '{}'.format(power.window['start']).ljust(20),
             '{:.3f}'.format(power.internal).ljust(20),
             '{:.3f}'.format(power.switching).ljust(20),
             '{:.3f}'.format(power.leakage).ljust(20))
            print(f"Power: internal: {power.internal} switching: {power.switching} leakage: {power.leakage} total: {power.total}")

    def set_active_power(self,name,signals,iter):
        """
        Set the power of the component in the active window
        """
        for power in self.active_power:
            file = f"./vcd/iter/iter_{iter}_{name}_active_{power.window['start']}.vcd.pwr"
            reader = InnovusPowerParser(file)
            reader.set_nets()
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage
            print(f"Power: internal: {power.internal} switching: {power.switching} leakage: {power.leakage} total: {power.total}")
            logging.info('%s %s %s %s',
             '{}'.format(power.window['start']).ljust(20),
             '{:.3f}'.format(power.internal).ljust(20),
             '{:.3f}'.format(power.switching).ljust(20),
             '{:.3f}'.format(power.leakage).ljust(20))

    def set_inactive_power(self,name,signals,iter):
        """
        Set the power of the component in the inactive window
        """
        for power in self.inactive_power:
            file = f"./vcd/iter/iter_{iter}_{name}_inactive_{power.window['start']}.vcd.pwr"
            reader = InnovusPowerParser(file)
            reader.set_nets()
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage
            print(f"Power: internal: {power.internal} switching: {power.switching} leakage: {power.leakage} total: {power.total}")
            logging.info('%s %s %s %s',
             '{}'.format(power.window['start']).ljust(20),
             '{:.3f}'.format(power.internal).ljust(20),
             '{:.3f}'.format(power.switching).ljust(20),
             '{:.3f}'.format(power.leakage).ljust(20))


class CellProfiler():
    def __init__(self):
        self.power = Power()
        self.per_cycle_power = []
        self.energy = Energy()
        self.net = {}

    def add_power(self, new_power):
        self.power.append(new_power)

    def add_energy(self, new_energy):
        self.energy.append(new_energy)
