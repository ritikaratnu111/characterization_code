from component_profiler import ComponentProfiler
from isa import ISA
import logging

class ActiveComponent():
    def __init__(self, name, signals, active_window, inactive_window, c_internal, c_leakage):
        self.name = name
        self.signals = signals
        self.active_window = active_window if active_window is not None else []
        self.inactive_window = inactive_window if inactive_window is not None else []
        self.c_internal = c_internal
        self.c_leakage = c_leakage
        self.profiler = ComponentProfiler()
        self.mode = None

    def __eq__(self, other):
        if isinstance(other, ActiveComponent):
            return (
                self.name == other.name and
                self.signals == other.signals 
            )
        return False

    def init_profiler(self,total_window):
#        logging.info(f"{self.name}, {self.active_window}")
        self.profiler.init(self.active_window, self.inactive_window,total_window, self.signals, self.c_internal, self.c_leakage)

    def print(self):
        print(f"Component: {self.name}, {self.active_window}, {self.inactive_window}")

class InactiveComponent():

    def __init__(self, name, signals, window):
        self.name = name
        self.signals = signals
        self.window = window if window is not None else {}
        self.profiler = ComponentProfiler()

    def init_profiler(self,total_window):
        inactive_window = []
        inactive_window.append(total_window)
        self.profiler.init(0,inactive_window,total_window,self.signals)

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
