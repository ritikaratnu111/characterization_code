from energy import ComponentProfiler
from isa import ISA

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

    def init_profiler(self):
        self.profiler.init(self.active_window, self.inactive_window)

    def set_per_cycle_power(self):
        print("Setting per cycle power")
  #      self.profiler.set_per_cycle_power(self.signals)

    def set_active_power(self):
        self.profiler.set_active_power(self.signals)
    
    def set_inactive_power(self):
        self.profiler.set_inactive_power(self.signals)

    def print(self):
        print(f"Component: {self.name}, {self.active_window}, {self.inactive_window}")

class ComponentSet():
    def __init__(self, active_components=None):
        self.active = []
        self.inactive = []

    def add_active_component(self,component):
        if (component not in self.active):
            self.active.append(component)

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