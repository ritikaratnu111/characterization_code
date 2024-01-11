from component_profiler import ComponentProfiler
from isa import ISA
import logging

class ActiveComponent():
    def __init__(self, name, signals, active_window, inactive_window):
        self.name = name
        self.signals = signals
        self.active_window = active_window if active_window is not None else {}
        self.inactive_window = inactive_window if inactive_window is not None else {}
        self.profiler = ComponentProfiler()

    def __eq__(self, other):
        if isinstance(other, ActiveComponent):
            return (
                self.name == other.name and
                self.signals == other.signals 
            )
        return False

    def init_profiler(self,total_window):
        self.profiler.init(self.active_window, self.inactive_window,total_window)

    def set_per_cycle_measurement(self,reader):
        print("Setting per cycle power")
        self.profiler.set_per_cycle_measurement(reader,self.signals)

    def set_active_measurement(self,reader,iter):
        print("Setting active power")
        logging.info("Iter: %s", iter)
        self.profiler.set_active_measurement(reader,self.name,self.signals,iter)
    
    def set_inactive_measurement(self,reader,iter):
        print("Setting inactive power")
        logging.info("Iter: %s", iter)
        self.profiler.set_inactive_measurement(reader,self.name,self.signals,iter)

    def print(self):
        print(f"Component: {self.name}, {self.active_window}, {self.inactive_window}")
