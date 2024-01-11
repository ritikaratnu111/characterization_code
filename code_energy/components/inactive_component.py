from component_profiler import ComponentProfiler
from isa import ISA
import logging

class InactiveComponent():

    def __init__(self, name, signals, window):
        self.name = name
        self.signals = signals
        self.window = window if window is not None else {}
        self.profiler = ComponentProfiler()
        self.init_profiler(window)

    def init_profiler(self,total_window):
        self.profiler.init(0,0,total_window)

    def set_per_cycle_measurement(self,reader):
        print("Setting per cycle power")
        self.profiler.set_per_cycle_measurement(reader,self.signals)

    def set_measurement(self,reader,iter):
        print("Setting inactive power")
        logging.info("Iter: %s", iter)
        self.profiler.set_inactive_measurement(reader,self.name,self.signals,iter)

    def print(self):
        print(f"Component: {self.name}, {self.active_window}, {self.inactive_window}")

