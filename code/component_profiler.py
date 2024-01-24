import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class AverageMeasurement():
    def __init__(self):
        self.active = Measurement()
        self.inactive = Measurement()
        self.diff_active = Measurement()
        self.diff_inactive = Measurement()
        self.count = 0

class ComponentProfiler():
    def __init__(self):
        self.active_window = []
        self.inactive_window = []
        self.per_cycle_window = []
        self.per_cycle_active_window = []
        self.active_measurement = Measurement
        self.inactive_measurement = Measurement
        self.total_measurement = Measurement
        self.error_measurement = Measurement()
        self.per_cycle_measurement = []
        self.active_measurement_from_per_cycle = []
        self.inactive_measurement_from_per_cycle = []
        self.total_measurement_from_per_cycle = Measurement()
        self.nets = 0
        self.signals = [] 
        self.active_factor = 0
        self.inactive_factor = 0
        self.average_measurement = [] 

    def init(self, active_window, inactive_window,total_window, signals):
        if(active_window):
            self.active_window= {
                'windows': [{'start': window['start'], 'end': window['end']} for window in active_window],
                'clock_cycles': sum(window['clock_cycles'] for window in active_window)
            }
        if(inactive_window):
            self.inactive_window= {
                'windows': [{'start': window['start'], 'end': window['end']} for window in inactive_window],
                'clock_cycles': sum(window['clock_cycles'] for window in inactive_window)
            }

        self.total_window = total_window
        if(self.active_window):
            self.active_factor = self.active_window['clock_cycles'] / self.total_window['clock_cycles']
        if(self.inactive_window):
            self.inactive_factor = self.inactive_window['clock_cycles'] / self.total_window['clock_cycles']
        self.signals = signals
        current_start = total_window['start']
        while current_start < total_window['end']:
            self.per_cycle_window.append({'start': current_start, 'end': current_start + constants.CLOCK_PERIOD, 'clock_cycles' : 1})
            current_start += constants.CLOCK_PERIOD        

    def set_avg_measurement_size(self,iter):
        self.average_measurement = [AverageMeasurement() for i in range(iter)]

    def add_avg_measurement(self,active_measurement,inactive_measurement,iter):
        if(iter > 0):
            self.average_measurement[iter].active.average_power(self.average_measurement[iter-1].active,active_measurement,iter)
            self.average_measurement[iter].inactive.average_power(self.average_measurement[iter-1].inactive,inactive_measurement,iter)
            self.average_measurement[iter].diff_active.diff_power(self.average_measurement[iter].active,self.average_measurement[iter-1].active)
            self.average_measurement[iter].diff_inactive.diff_power(self.average_measurement[iter].inactive,self.average_measurement[iter-1].inactive)
        else:
            self.average_measurement[iter].active.average_power(self.average_measurement[iter].active,active_measurement,iter)
            self.average_measurement[iter].inactive.average_power(self.average_measurement[iter].inactive,inactive_measurement,iter)
            self.average_measurement[iter].diff_active.diff_power(self.average_measurement[iter].active,self.average_measurement[iter].active)
            self.average_measurement[iter].diff_inactive.diff_power(self.average_measurement[iter].inactive,self.average_measurement[iter].inactive)

        self.average_measurement[iter].count = iter

    def set_per_cycle_measurement(self,reader,signals):
        for window in self.per_cycle_window:
            file = f"./vcd/{window['start']}.vcd.pwr"
            print(f"File: {file}")
            measurement = Measurement()
            measurement.set_window(window)
            measurement.read_power(reader,file,signals)
            measurement.get_energy()
            measurement.log_power()
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

    def set_total_measurement(self,reader,iter):
        file = f"./vcd/iter_{iter}.vcd.pwr"
        print(f"File: {file}")
        print("Total measurement: ", self.total_window["clock_cycles"])
        measurement = Measurement()
        measurement.set_window(self.total_window)
        measurement.read_power(reader,file,self.signals)
        measurement.get_energy()
        measurement.log_power()
        measurement.log_energy("Total")
        self.nets = measurement.nets
        self.total_measurement = measurement

    def set_inactive_measurement(self,reader,iter):
        """
        Set the power of the component in the inactive window
        """
        if(self.inactive_window):
            file = f"./vcd/iter_{iter}.vcd.pwr"
            print(f"File: {file}")
            print("Inactive measurement: ", self.inactive_window["clock_cycles"])
            measurement = Measurement()
            measurement.set_window(self.inactive_window)
            measurement.read_inactive_power(reader,file,self.signals)
            measurement.get_energy()
            measurement.log_power()
            measurement.log_energy("Inactive")
            self.nets = measurement.nets
            self.inactive_measurement = measurement
        else:
            self.inactive_measurement = Measurement()
            self.inactive_measurement.set_window(self.inactive_window)
            self.inactive_measurement.energy.internal = 0
            self.inactive_measurement.energy.switching = 0
            self.inactive_measurement.energy.leakage = 0
            self.inactive_measurement.energy.total = 0
            self.inactive_measurement.power.internal = 0
            self.inactive_measurement.power.switching = 0
            self.inactive_measurement.power.leakage = 0
            self.inactive_measurement.power.total = 0
            self.inactive_measurement.nets = 0
            self.inactive_measurement.log_energy("Inactive")

    def set_active_measurement(self,reader,iter):
        """
        Set the power of the component in the active window
        """
        if(self.active_window):
            file = f"./vcd/iter_{iter}.vcd.pwr"
            print("Active measurement: ", self.active_window["clock_cycles"])
            measurement = Measurement()
            measurement.set_window(self.active_window)
            measurement.set_factor(self.active_factor)
            measurement.read_power(reader,file,self.signals)
            measurement.get_energy()
            measurement.log_power()
            measurement.log_energy("Active")
            self.nets = measurement.nets
            self.active_measurement = measurement
        else:
            self.active_measurement = Measurement()
            self.active_measurement.set_window(self.active_window)
            self.active_measurement.energy.internal = 0
            self.active_measurement.energy.switching = 0
            self.active_measurement.energy.leakage = 0
            self.active_measurement.energy.total = 0
            self.active_measurement.power.internal = 0
            self.active_measurement.power.switching = 0
            self.active_measurement.power.leakage = 0
            self.active_measurement.power.total = 0
            self.active_measurement.nets = 0
            self.active_measurement.log_energy("Active")

    def set_error_measurement(self):
        """
        Set the error between total and active + inactive energy of the cell
        """
        print("Error measurement: ")
        measurement = Measurement()
        measurement.set_window(self.total_window)
        measurement.add_energy(self.active_measurement)
        measurement.add_energy(self.inactive_measurement)
        self.error_measurement.set_window(self.total_window)
        self.error_measurement.diff_energy(self.total_measurement,measurement)
        self.error_measurement.log_energy("Error")


    def print_avg_results(self,iter):
        print(f"Average Results for iteration {iter}")
        print(f"Active: ")
        self.average_measurement[iter].active.log_power()
        print(f"Inactive: ")
        self.average_measurement[iter].inactive.log_power()
        print(f"Diff Active: ")
        self.average_measurement[iter].diff_active.log_power()
        print(f"Diff Inactive: ")
        self.average_measurement[iter].diff_inactive.log_power()