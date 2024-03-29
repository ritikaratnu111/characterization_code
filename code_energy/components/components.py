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


class ComponentSet():
    def __init__(self, active_components=None):
        self.active = []
        self.inactive = []

    def add_active_component(self,component):
        if (component not in self.active):
            self.active.append(component)

    def add_inactive_component(self,name,info,window):
        new_component = InactiveComponent(name,info["signals"],window) 
        if (new_component not in self.inactive):
            self.inactive.append(new_component)

    def reorder_components(self):
        my_isa = ISA()
        component_hierarchy = my_isa.component_hierarchy
        component_hierarchy_dict = {component: index for index, component in enumerate(component_hierarchy)}
        sorted_components = sorted(self.active, key=lambda component: component_hierarchy_dict.get(component.name, float('inf')))
        self.active = sorted_components

    def add_active_window(self):
        for component in self.active:
            active_window = []
            start = self.total_window['start']
            for window in component.active_window:
                end = window['start']
                if (start != end):
                    active_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                active_window.append({'start': start, 'end': end})
            component.active_window = active_window
    
    def add_inactive_window(self):
        for component in self.active:
            inactive_window = []
            start = self.total_window['start']
            for window in component.active_window:
                end = window['start']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                inactive_window.append({'start': start, 'end': end})
            component.inactive_window = inactive_window

    def print(self):
        for component in self.active:
            component.print()
