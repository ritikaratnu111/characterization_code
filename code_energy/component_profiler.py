import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class ComponentProfiler():
    def __init__(self):
        self.active_window = []
        self.inactive_window = []
        self.per_cycle_window = []
        self.per_cycle_active_window = []
        self.active_measurement = []
        self.inactive_measurement = []
        self.per_cycle_measurement = []
        self.active_measurement_from_per_cycle = []
        self.inactive_measurement_from_per_cycle = []
        self.total_measurement_from_per_cycle = Measurement()
        self.total_measurement_from_iter_file = Measurement()

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
            self.per_cycle_measurement.append(measurement)
        active_window = []
        inactive_window = []
        current_window = []
        
        for i, measurement in enumerate(self.per_cycle_measurement):
            if measurement.power.switching > 0:
                if not current_window:
                    current_window.append(measurement.window['start'])
            else:
                if current_window:
                    current_window.append(measurement.window['start'])
                    active_window.append(current_window)
                    current_window = []
                if i < len(self.per_cycle_measurement) - 1:  
                    inactive_window.append([measurement.window['start'], self.per_cycle_measurement[i + 1].window['start'] ])

        self.per_cycle_active_window = active_window
    def set_active_measurement_from_per_cycle(self):
        iter = 0
        for window in self.active_window:
            measurement = Measurement()
            measurement.set_window(window)
            for i,per_cycle_window in enumerate(self.per_cycle_window):
                if(window['start'] <= per_cycle_window['start'] and window['end'] >= per_cycle_window['end']):
                    #print(per_cycle_window['start'])
                    measurement.add_power(self.per_cycle_measurement[i])
                    measurement.add_energy(self.per_cycle_measurement[i])
                    measurement.nets = self.per_cycle_measurement[i].nets
            measurement.adjust_power()
            self.active_measurement_from_per_cycle.append(measurement)                    

    def set_inactive_measurement_from_per_cycle(self):
        iter = 0
        print(self.inactive_window)
        for window in self.inactive_window:
            measurement = Measurement()
            measurement.set_window(window)
            for i,per_cycle_window in enumerate(self.per_cycle_window):
                if(window['start'] <= per_cycle_window['start'] and window['end'] >= per_cycle_window['end']):
                    measurement.add_power(self.per_cycle_measurement[i])
                    measurement.add_energy(self.per_cycle_measurement[i])
                    measurement.nets = self.per_cycle_measurement[i].nets
            measurement.adjust_power()
            self.inactive_measurement_from_per_cycle.append(measurement)                    

    def set_total_measurement_from_per_cycle(self,window):
        iter = 0
        print(window)
        self.total_measurement_from_per_cycle.set_window(window)
        for active_measurement in self.active_measurement_from_per_cycle:
            self.total_measurement_from_per_cycle.nets = active_measurement.nets
            self.total_measurement_from_per_cycle.add_power(active_measurement)
            self.total_measurement_from_per_cycle.add_energy(active_measurement)

        for inactive_measurement in self.inactive_measurement_from_per_cycle:
            self.total_measurement_from_per_cycle.nets = inactive_measurement.nets
            self.total_measurement_from_per_cycle.add_power(inactive_measurement)
            self.total_measurement_from_per_cycle.add_energy(inactive_measurement)
        self.total_measurement_from_per_cycle.adjust_power()
        print(self.total_measurement_from_per_cycle.window,self.total_measurement_from_per_cycle.power.internal,self.total_measurement_from_per_cycle.power.switching,self.total_measurement_from_per_cycle.power.leakage)

    def set_total_measurement_from_iter_file(self,reader,signals,iter,window):
            file = f"./vcd/iter/iter_{iter}.vcd.pwr"
            print(f"File: {file}")
            self.total_measurement_from_iter_file.set_window(window)
            self.total_measurement_from_iter_file.read_power(reader,file,signals)
            self.total_measurement_from_iter_file.get_energy()

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
