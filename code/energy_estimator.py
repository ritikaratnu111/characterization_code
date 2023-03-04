class EnergyEstimator():
    def __init__(self,tb,active_components,active_window,inactive_window,all_cycles):
        self.active_components = active_components
        self.active_window = active_window
        self.inactive_window = inactive_window
        self.power = {}
        self.energy = {}

    def print_power(self):
        for component in self.power:
            print(component, round(self.power[component],2))

    def set_power(self,tb):
        for component self.active_components:
            signals = self.active_components[component]
            active_power_file = tb + "/" + component + "_active.pwr"
            inactive_power_file = tb + "/" + component + "_inactive.pwr"
            self.power.set_nets(active_power_file)
            self.power[component]['active'] = self.power.get_active_component_power(signals)
            self.power.set_nets(inactive_power_file)
            self.power[component]['inactive'] = self.power.get_active_component_power(signals)
        power_file = tb + "/" + "activity.pwr"
        self.power['inactive_components'] = self.get_inactive_component_power('rest')

    def set_energy(self):
        for component in self.power:
            for state in self.power[component]:
                for power_type in self.power[component][state]:
                    self.energy[component][state][power_type] = int(self.active_windows[component]) * self.power[component][state][power_type]

    def print_energy(self):
        for component in self.energy:
            print(component, self.energy[component])

