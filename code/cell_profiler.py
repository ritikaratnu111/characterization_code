import constants
import logging
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class CellProfiler():
    def __init__(self):
        self.window = {}
        self.AEC_measurement = Measurement()
        self.remaining_measurement = Measurement()
        self.total_measurement = Measurement()
        self.diff_measurement = Measurement()

    def init(self, total_window):
        self.window = total_window

    def set_AEC_measurement(self,active_components,iter):
        """
        Sum up the energies of the active components in the cell
        """
        for component in active_components:
            self.AEC_measurement.set_window(self.window)
            for measurement in component.profiler.active_measurement:
                self.AEC_measurement.add_measurement(measurement)
            for measurement in component.profiler.inactive_measurement:
                self.AEC_measurement.add_measurement(measurement)
        self.AEC_measurement.log()


    def set_remaining_measurement(self,reader,tiles,iter):
        """
        Set the power of the remaining components in the cell apart from active components
        """
        file = f"./vcd/iter/iter_{iter}.vcd.pwr"
        measurement = Measurement()
        measurement.set_window(self.window)
        measurement.read_remaining_power(reader,file,tiles)
        measurement.get_energy()
        measurement.log()
        self.remaining_measurement = measurement

    def set_total_measurement(self,reader,tiles,iter):
        """
        Set total power of the cell 
        """
        file = f"./vcd/iter/iter_{iter}.vcd.pwr"
        measurement = Measurement()
        measurement.set_window(self.window)
        measurement.read_total_power(reader,file,tiles)
        measurement.get_energy()
        measurement.log()
        self.total_measurement = measurement

    def set_diff_measurement(self):
        """
        Set the difference between total and remaining power of the cell
        """
        measurement = Measurement()
        measurement.set_window(self.window)
        measurement.energy.internal = self.total_measurement.energy.internal - self.remaining_measurement.energy.internal - self.AEC_measurement.energy.internal
        measurement.energy.switching = self.total_measurement.energy.switching - self.remaining_measurement.energy.switching - self.AEC_measurement.energy.switching
        measurement.energy.leakage = self.total_measurement.energy.leakage - self.remaining_measurement.energy.leakage - self.AEC_measurement.energy.leakage
        measurement.energy.total = self.total_measurement.energy.total - self.remaining_measurement.energy.total - self.AEC_measurement.energy.total
        measurement.log()
        self.diff_measurement = measurement
