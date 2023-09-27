import constants
import logging
from innovus_reader import InnovusPowerParser
from energy import Power, Energy, Measurement

class CellProfiler():
    def __init__(self):
        self.window = {}
        self.AEC_measurement = Measurement()
        self.remaining_measurement = Measurement()
        self.total_measurement = Measurement()

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


    def set_remaining_measurement(self,tile,active_components,iter):
        """
        Set the power of the remaining components in the cell apart from active components
        """
        file = f"./vcd/iter/iter_{iter}.vcd.pwr"
        measurement = Measurement()
        measurement.set_window(self.window)
        measurement.read_remaining_power(file,tile,active_components)
        measurement.get_energy()
        measurement.log()
        self.remaining_measurement = measurement

    def set_total_measurement(self,tile,iter):
        """
        Set total power of the cell 
        """
        file = f"./vcd/iter/iter_{iter}.vcd.pwr"
        measurement = Measurement()
        measurement.set_window(self.window)
        measurement.read_total_power(file,tile)
        measurement.get_energy()
        measurement.log()
        self.total_measurement = measurement