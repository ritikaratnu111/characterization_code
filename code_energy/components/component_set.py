from component_profiler import ComponentProfiler
from isa import ISA
import logging

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
