import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement, Power, Energy, Net, MeasurementSet

class AverageMeasurement():
    def __init__(self):
        self.active = Measurement()
        self.inactive = Measurement()
        self.total = Measurement()
        self.diff = Measurement()
        self.count = 0

class ComponentProfiler():
    def __init__(self):
        self.active_window = []
        self.inactive_window = []
        self.per_cycle_window = []
        self.per_cycle_active_window = []
        self.measurement = MeasurementSet()
        self.per_cycle_measurement = []
        self.active_measurement_from_per_cycle = []
        self.inactive_measurement_from_per_cycle = []
        self.total_measurement_from_per_cycle = Measurement()
        self.nets = 0
        self.signals = [] 
        self.average_measurement = [] 
        self.c_internal = 0
        self.c_leakage = 0

    def init(self, active_window, inactive_window,total_window, signals, c_internal, c_leakage):
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
        self.signals = signals
        current_start = total_window['start']
        while current_start < total_window['end']:
            self.per_cycle_window.append({'start': current_start, 'end': current_start + constants.CLOCK_PERIOD, 'clock_cycles' : 1})
            current_start += constants.CLOCK_PERIOD        

        self.c_internal = float(c_internal) if c_internal != "uncharacterized" else 0
        self.c_leakage = float(c_leakage)

    def set_avg_measurement_size(self,iter):
        self.average_measurement = [AverageMeasurement() for i in range(iter)]

    def add_avg_measurement(self,active_measurement,inactive_measurement,iter):
        if(iter > 0):
            self.average_measurement[iter].active.average(self.average_measurement[iter-1].active,active_measurement,iter)
            self.average_measurement[iter].inactive.average(self.average_measurement[iter-1].inactive,inactive_measurement,iter)
            self.average_measurement[iter].total.add_energy(self.average_measurement[iter].active)
            self.average_measurement[iter].total.add_energy(self.average_measurement[iter].inactive)
            self.average_measurement[iter].diff.diff(self.average_measurement[iter].total,self.average_measurement[iter-1].total)
        else:
            self.average_measurement[iter].active.average(self.average_measurement[iter].active,active_measurement,iter)
            self.average_measurement[iter].inactive.average(self.average_measurement[iter].inactive,inactive_measurement,iter)
            self.average_measurement[iter].total.add_energy(self.average_measurement[iter].active)
            self.average_measurement[iter].total.add_energy(self.average_measurement[iter].inactive)
            self.average_measurement[iter].diff.diff(self.average_measurement[iter].total,self.average_measurement[iter].total)

        self.average_measurement[iter].count = iter

    def set_per_cycle_measurement(self,reader,signals):
        measurement = Measurement()
        measurement.set_measurement(reader, signals, constants.CLOCK_PERIOD, constants.CLOCK_PERIOD, 0, self.c_internal, self.c_leakage)
        measurement.log()
        self.per_cycle_measurement.append(measurement)
        active_window = []
        inactive_window = []
        current_window = []
        
        #for i, measurement in enumerate(self.per_cycle_measurement):
        #    if measurement.power.switching > 0:
        #        if not current_window:
        #            current_window.append(measurement.window['start'])
        #    else:
        #        if current_window:
        #            current_window.append(measurement.window['start'])
        #            active_window.append(current_window)
        #            current_window = []
        #        if i < len(self.per_cycle_measurement) - 1:  
        #            inactive_window.append([measurement.window['start'], self.per_cycle_measurement[i + 1].window['start'] ])

        #self.per_cycle_active_window = active_window
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


    def set_measurement(self, reader):
        print(f"Active Window: {self.active_window}, Inactive Window {self.inactive_window}, Total Window: {self.total_window}")
        print(f"c_internal, c_leakage: {self.c_internal}, {self.c_leakage}")
        self.measurement.set_T(
            self.total_window, self.active_window, self.inactive_window
            )
        if(self.inactive_window):
            self.measurement.set_inactive(
                self.c_internal, self.c_leakage
        )
        else:
            self.measurement.inactive.set_zero()
        
        if(self.active_window):
            self.measurement.set_active(
                reader, self.signals
            )
        else:
            self.measurement.active.set_zero()

        self.measurement.set_predicted()
        reader.remove_labels(self.signals)
        self.measurement.set_actual(reader, self.signals)
        self.measurement.set_error()
        self.measurement.log()

    def print_avg_results(self,iter):
        print(f"Average Results for iteration {iter}")
        print(f"Active:")
        self.average_measurement[iter].active.log_energy("Active")
        print(f"Inactive:")
        self.average_measurement[iter].inactive.log_energy("Inactive")
        print(f"Total:")
        self.average_measurement[iter].total.log_energy("Total")
        print(f"Diff:")
        self.average_measurement[iter].diff.log_energy("Diff")
