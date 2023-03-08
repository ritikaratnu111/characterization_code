from power import Power
class EnergyCalculator():
    def __init__(self,tb,active_components,active_windows,inactive_windows,total_window):
        self.tb = tb
        self.active_components = active_components
        self.active_windows = active_windows
        self.inactive_windows = inactive_windows
        self.total_window = total_window
        self.NetPower = Power()
        self.power = {}
        self.energy = {}
        self.set_active_component_power()
        self.set_inactive_component_power()
        self.set_energy()

#        self.print_power()

    def print_power(self):
        for component in self.power:
            for state in self.power[component]:
                for duration in self.power[component][state]:
                    for power_type in self.power[component][state][duration]:
                        print(component,state,duration,power_type,round(self.power[component][state][duration][power_type],2))

    def set_active_component_power(self):
        for component in self.active_components:
            self.power[component] = {'active': {}, 'inactive': {}}
            signals = self.active_components[component]
            for window in self.active_windows[component]:
                print(component,signals,window)
                active_component_active_power_file = self.tb + "/vcd/" + component + "_active_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
                self.NetPower.set_nets(active_component_active_power_file)
                self.NetPower.set_active_nets(signals)
                duration = str(window['start']) + "_" + str(window['end']) 
                self.power[component]['active'][duration] = self.NetPower.get_active_component_power()
                print(component,'active', duration,self.power[component]['active'][duration])
            for window in self.inactive_windows[component]:
                active_component_inactive_power_file = self.tb + "/vcd/" + component + "_inactive_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
                print(component,signals,window)
                self.NetPower.set_nets(active_component_inactive_power_file)
                self.NetPower.set_active_nets(signals)
                duration = str(window['start']) + "_" + str(window['end']) 
                self.power[component]['inactive'][duration] = self.NetPower.get_active_component_power()
                print(component,'inactive', duration,self.power[component]['inactive'][duration])

    def set_inactive_component_power(self):
        inactive_component_power_file = tb + "/vcd/" + "total" + "_active_" + str(total_window['start']) + "_" + str(total_window['end']) + ".vcd.pwr"
        self.NetPower.set_nets(inactive_component_power_file)
        for component in self.active_components:
            signals = self.active_components[component]
            self.NetPower.set_active_nets(signals)
        self.NetPower.set_inactive_nets()
        self.power['inactive_components'] = self.get_inactive_component_power()

    def set_energy(self):
        for component in self.power:
            for state in self.power[component]:
                for duration in self.power[component][state]:
                    start = int(duration.split('_')[0])
                    end = int(duration.split('_')[1])
                    time = end - start
                    for power_type in self.power[component][state]:
                        self.energy[component][state][duration][power_type] = time * self.power[component][state][duration][power_type]
                        print(self.energy[component][state][duration][power_type])

    def print_energy(self):
        for component in self.energy:
            print(component, self.energy[component])
