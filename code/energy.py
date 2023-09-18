import constants
from innovus_reader import InnovusPowerParser

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

    def init(self, active_window, inactive_window):
        self.active_window = active_window
        self.inactive_window = inactive_window
        self.init_total_window()
        self.init_active_power()
        self.init_inactive_power()
        self.init_per_cycle_power()

    def init_total_window(self):
        print(self.active_window)
        print(self.inactive_window)
        min_start = min(window['start'] for window in self.active_window + self.inactive_window)
        max_end = max(window['end'] for window in self.active_window + self.inactive_window)
        self.total_window = [{'start': min_start, 'end': max_end}]

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
            file = f"{constants.VCD_DIR}/iter_{iter}_{name}_active_{power.window['start']}.vcd.pwr"
            reader = InnovusPowerParser()
            reader.set_nets(file)
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage

    def set_active_power(self,signals,iter,name):
        """
        Set the power of the component in the active window
        """
        for power in self.active_power:
            file = f"{constants.VCD_DIR}/iter_{iter}_{name}_active_{power.window['start']}.vcd.pwr"
            reader = InnovusPowerParser()
            reader.set_nets(file)
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage

    def set_inactive_power(self,signals,iter,name):
        """
        Set the power of the component in the inactive window
        """
        for power in self.inactive_power:
            file = f"{constants.VCD_DIR}/iter_{iter}_{name}_inactive_{power.window['start']}.vcd.pwr"
            reader = InnovusPowerParser()
            reader.set_nets(file)
            reader.set_active_nets(signals)
            reader_power, active_nets = reader.get_active_component_dynamic_power(signals)
            power.internal = reader_power['internal']
            power.switching = reader_power['switching']
            power.leakage = reader_power['leakage']
            power.total = power.internal + power.switching + power.leakage

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
