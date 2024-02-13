import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement, MeasurementSet
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
        self.measurement_set = MeasurementSet()
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

    def set_measurement(self, reader, tiles, active_components):
        self.measurement_set.set_T(
            self.window, self.window, 0
        )
        self.measurement_set.active.set_zero()
        self.measurement_set.inactive.set_zero()
        self.measurement_set.set_predicted()
        print(tiles)
        self.measurement_set.set_actual(reader, tiles)
        self.measurement_set.set_error()
        self.measurement_set.log()

    def plot(self):
        # Extracting diff energy measurements for plotting
        diff_switching_values = [ avg_measurement.diff.energy.switching
            for avg_measurement in self.average_measurement
        ]

        diff_total_values = [ avg_measurement.diff.energy.total
            for avg_measurement in self.average_measurement
        ]

        diff_internal_values = [ avg_measurement.diff.energy.internal
            for avg_measurement in self.average_measurement
        ]

        diff_leakage_values = [ avg_measurement.diff.energy.leakage
            for avg_measurement in self.average_measurement
        ]

        #Plot internal, switching, leakage, total diff values
        plt.plot(diff_internal_values, label="Internal")
        plt.plot(diff_switching_values, label="Switching")
        plt.plot(diff_leakage_values, label="Leakage")
        plt.plot(diff_total_values, label="Total")
        plt.legend()
        plt.show()
        plt.xlabel("Samples")
        plt.ylabel("Avg Energy Error (%)")
        plt.title("Avg Energy Error (%) vs Samples")
        plt.savefig(f"avg_energy_error.png")




    def print_avg_results(self,iter):
        print(f"Cell average Results for iteration {iter}")
        self.average_measurement[iter].current.log_power()
        print(f"Diff:")
        self.average_measurement[iter].diff.log_power()
