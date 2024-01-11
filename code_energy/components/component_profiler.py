import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class ComponentProfiler():
    def __init__(self):
        self.active_window = []
        self.inactive_window = []
        self.per_cycle_window = []
        self.active_measurement = []
        self.inactive_measurement = []
        self.per_cycle_measurement = []

    def init(self, active_window, inactive_window,total_window):
        self.active_window = active_window
        self.inactive_window = inactive_window
        current_start = total_window['start']
        while current_start < total_window['end']:
            self.per_cycle_window.append({'start': current_start, 'end': current_start + constants.CLOCK_PERIOD, 'clock_cycles' : 1})
            current_start += constants.CLOCK_PERIOD        

    def set_per_cycle_measurement(self,reader,signals):
        for window in self.per_cycle_window:
            file = f"./vcd/{window['start']}.vcd.pwr"
            print(f"File: {file}")
            measurement = Measurement()
            measurement.set_window(window)
            measurement.read_power(reader,file,signals)
            measurement.get_energy()
            measurement.log()
            self.per_cycle_measurement.append(measurement)

    def set_active_measurement(self,reader,name,signals,iter):
        """
        Set the power of the component in the active window
        """
        for window in self.active_window:
            file = f"./vcd/iter/iter_{iter}_{name}_active_{window['start']}.vcd.pwr"
            print(f"File: {file}")
            measurement = Measurement()
            measurement.set_window(window)
            measurement.read_power(reader,file,signals)
            measurement.get_energy()
            measurement.log()
            self.active_measurement.append(measurement)

    def set_inactive_measurement(self,reader,name,signals,iter):
        """
        Set the power of the component in the inactive window
        """
        for window in self.inactive_window:
            file = f"./vcd/iter/iter_{iter}_{name}_inactive_{window['start']}.vcd.pwr"
            print(f"File: {file}")
            measurement = Measurement()
            measurement.set_window(window)
            measurement.read_power(reader,file,signals)
            measurement.get_energy()
            measurement.log()
            self.inactive_measurement.append(measurement)
