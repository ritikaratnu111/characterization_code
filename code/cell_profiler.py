import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement
import matplotlib.pyplot as plt
import json

class AverageMeasurement():
    def __init__(self):
        self.current = Measurement()
        self.diff = Measurement()
        self.count = 0

class CellProfiler():
    def __init__(self):
        self.window = {}
        self.active_AEC_measurement = Measurement()
        self.inactive_AEC_measurement = Measurement()
        self.total_measurement = Measurement()
        self.error_measurement = Measurement()
        self.nets = 0
        self.average_measurement = []
        self.cell_id = ""

    def init(self, total_window, id):
        self.window = total_window
        self.cell_id = id

    def set_avg_measurement_size(self,iter):
        self.average_measurement = [AverageMeasurement() for i in range(iter)]

    def add_avg_measurement(self,measurement,iter):
        if(iter > 0):
            self.average_measurement[iter].current.average(self.average_measurement[iter-1].current,measurement,iter)
            self.average_measurement[iter].diff.diff(self.average_measurement[iter].current,self.average_measurement[iter-1].current)
        else:
            self.average_measurement[iter].current.average(measurement,measurement,iter)
            self.average_measurement[iter].diff.diff(self.average_measurement[iter].current,self.average_measurement[iter].current)

        self.average_measurement[iter].count = iter

    def set_active_AEC_measurement(self,active_components,iter):
        """
        Sum up the energies of the active components in the cell
        """
        for component in active_components:
            print(component.name, component.active_window)
            #self.active_AEC_measurement.set_window(self.window)
            #self.active_AEC_measurement.nets += component.profiler.total_measurement_from_per_cycle.nets
            #self.active_AEC_measurement.add_power(component.profiler.total_measurement_from_per_cycle)
            #self.active_AEC_measurement.add_energy(component.profiler.total_measurement_from_per_cycle)

    def set_inactive_AEC_measurement(self,inactive_components,iter):
        """
        Sum up the energies of the inactive components in the cell
        """
        for component in inactive_components:
            self.inactive_AEC_measurement.set_window(self.window)
            self.inactive_AEC_measurement.nets += component.profiler.total_measurement_from_per_cycle.nets
            self.inactive_AEC_measurement.add_power(component.profiler.total_measurement_from_per_cycle)
            self.inactive_AEC_measurement.add_energy(component.profiler.total_measurement_from_per_cycle)

    def set_total_measurement(self,reader,tiles,iter):
        """
        Set total power of the cell 
        """
        file = f"./vcd/iter_{iter}.vcd.pwr"
        self.total_measurement.set_window(self.window)
        self.total_measurement.read_cell_power(reader,file,tiles)
        self.total_measurement.get_energy()
        self.total_measurement.log_power()
        self.total_measurement.log_energy("Cell Total")
        self.nets = self.total_measurement.nets

    def set_error_measurement(self):
        """
        Set the errorerence between total and remaining power of the cell
        """
        self.error_measurement.set_window(self.window)
        self.error_measurement.nets = 100 *  (self.total_measurement.nets - self.active_AEC_measurement.nets - self.inactive_AEC_measurement.nets) / max(self.total_measurement.nets,self.active_AEC_measurement.nets+self.inactive_AEC_measurement.nets)
        self.error_measurement.energy.internal = 100 * (self.total_measurement.energy.internal - self.active_AEC_measurement.energy.internal - self.inactive_AEC_measurement.energy.internal)/ max(self.total_measurement.energy.internal,self.active_AEC_measurement.energy.internal+self.inactive_AEC_measurement.energy.internal)
        self.error_measurement.energy.switching = 100 * (self.total_measurement.energy.switching - self.active_AEC_measurement.energy.switching - self.inactive_AEC_measurement.energy.switching) / max(self.total_measurement.energy.internal,self.active_AEC_measurement.energy.internal+self.inactive_AEC_measurement.energy.internal)
        self.error_measurement.energy.leakage = 100 * (self.total_measurement.energy.leakage - self.active_AEC_measurement.energy.leakage - self.inactive_AEC_measurement.energy.leakage) / max(self.total_measurement.energy.internal,self.active_AEC_measurement.energy.internal+self.inactive_AEC_measurement.energy.internal)
        self.error_measurement.energy.total = 100 * (self.total_measurement.energy.total - self.active_AEC_measurement.energy.total - self.inactive_AEC_measurement.energy.total) / max(self.total_measurement.energy.internal,self.active_AEC_measurement.energy.internal+self.inactive_AEC_measurement.energy.internal)


    def plot(self):
        # Extracting diff energy measurements for plotting
        diff_switching_values = [ avg_measurement.diff.energy.switching
            for avg_measurement in self.average_measurement
        ]

        #Plot the diff switching energy measurements
        plt.plot(diff_switching_values, label='Diff Switching Energy')
        # Adding labels and title
        plt.xlabel('Measurements')
        plt.ylabel('Energy Values')
        plt.title('Diff Energy Measurements')
        plt.savefig('diff_switching_energy_plot.png')
        # Display the plot
        print(diff_switching_values) 
        #plt.show()

    def print_avg_results(self,iter):
        print(f"Cell average Results for iteration {iter}")
        self.average_measurement[iter].current.log_power()
        print(f"Diff:")
        self.average_measurement[iter].diff.log_power()
