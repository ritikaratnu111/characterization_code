from power import Power
class EnergyCalculator():
    def __init__(self,tb,active_components,active_windows,inactive_windows,total_window):
        self.tb = tb
        self.active_components = active_components
        self.active_windows = active_windows
        self.inactive_windows = inactive_windows
        self.total_window = total_window
        self.NetPower = Power()
        self.active_component_power = {}
        self.inactive_component_power = {}
        self.total_power = {}
        self.energy = {}
        self.energy_error = {'internal': 0, 'switching': 0, 'leakage' : 0}
        self.set_active_component_power()
        self.set_inactive_component_power()
        self.set_total_power()
        self.set_energy()
        self.print_energy()

    def print_power(self):
        for component in self.power:
            for state in self.power[component]:
                for duration in self.power[component][state]:
                    for power_type in self.power[component][state][duration]:
                        print(component,state,duration,power_type,round(self.power[component][state][duration][power_type],2))

    def set_active_component_power(self):
        print("Computing active component power... ")
        for component in self.active_components:
            self.active_component_power[component] = {'active': {}, 'inactive': {}}
            signals = self.active_components[component]
            for window in self.active_windows[component]:
    #            print(component,signals,window)
                active_component_active_power_file = self.tb + "/vcd/" + component + "_active_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
                self.NetPower.set_nets(active_component_active_power_file)
                self.NetPower.set_active_nets(signals)
                duration = str(window['start']) + "_" + str(window['end']) 
                self.active_component_power[component]['active'][duration] = self.NetPower.get_active_component_power()
    #            print(component,'active', duration,self.active_component_power[component]['active'][duration])
            for window in self.inactive_windows[component]:
                active_component_inactive_power_file = self.tb + "/vcd/" + component + "_inactive_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
    #            print(component,signals,window)
                self.NetPower.set_nets(active_component_inactive_power_file)
                self.NetPower.set_active_nets(signals)
                duration = str(window['start']) + "_" + str(window['end']) 
                self.active_component_power[component]['inactive'][duration] = self.NetPower.get_active_component_power()
    #            print(component,'inactive', duration,self.active_component_power[component]['inactive'][duration])

    def set_inactive_component_power(self):
        print("Computing inactive component power... ")
        inactive_component_power_file = self.tb + "/vcd/" + "total" + "_active_" + str(self.total_window['start']) + "_" + str(self.total_window['end']) + ".vcd.pwr"
        self.NetPower.set_nets(inactive_component_power_file)
        duration = str(self.total_window['start']) + "_" + str(self.total_window['end']) 
        for component in self.active_components:
            signals = self.active_components[component]
            self.NetPower.set_active_nets(signals)
        self.NetPower.set_inactive_nets()
        self.inactive_component_power = self.NetPower.get_inactive_component_power()

    def set_total_power(self):
        print("Computing total component power.. ")
        power_file = self.tb + "/vcd/" + "total" + "_active_" + str(self.total_window['start']) + "_" + str(self.total_window['end']) + ".vcd.pwr"
        duration = str(self.total_window['start']) + "_" + str(self.total_window['end']) 
        self.NetPower.set_nets(power_file)
        self.total_power = self.NetPower.get_total_power()

    def set_energy(self):
        active_component_energy = {'internal': 0, 'switching': 0, 'leakage' : 0}
        internal = 0
        switching = 0
        leakage = 0
        for component in self.active_component_power:
            self.energy[component] = {'active': {}, 'inactive': {}}
            for state in self.active_component_power[component]:
                for duration in self.active_component_power[component][state]:
                    self.energy[component][state][duration] = {'internal': 0, 'switching': 0, 'leakage' : 0} 
                    start = int(duration.split('_')[0])
                    end = int(duration.split('_')[1])
                    time = end - start
                    for power_type in self.active_component_power[component][state][duration]:
                        self.energy[component][state][duration][power_type] = time * self.active_component_power[component][state][duration][power_type]
                        active_component_energy[power_type] += self.energy[component][state][duration][power_type]

#        self.energy['total'] = {}
#        self.energy['inactive_components'] = {}
#        self.energy['active_components'] = {}
#        self.total_power = {'internal': 0, 'switching': 0, 'leakage' : 0}
#        self.active_component_power = {'internal': 0, 'switching': 0, 'leakage' : 0}
#        self.inactive_component_power = {'internal': 0, 'switching': 0, 'leakage' : 0}
        self.energy['total'] = {'internal': 0, 'switching': 0, 'leakage' : 0}
        self.energy['inactive_components'] = {'internal': 0, 'switching': 0, 'leakage' : 0}
        self.energy['active_components'] = {'internal': 0, 'switching': 0, 'leakage' : 0}

        start = self.total_window['start']
        end = self.total_window['end']
        time = end - start

        for power_type in self.total_power:
            self.energy['total'][power_type] = time * self.total_power[power_type]
            self.energy['inactive_components'][power_type] = time * self.inactive_component_power[power_type]
            self.energy['active_components'][power_type] = active_component_energy[power_type]
            estimate = self.energy['inactive_components'][power_type] + self.energy['active_components'][power_type]
            actual = self.energy['total'][power_type]
            self.energy_error[power_type] = (actual - estimate) * 100 /max(actual,estimate)

    def print_energy(self):
        print("total: ", 'internal : ', self.energy['total']['internal'], ' switching : ',self.energy['total']['switching'],  ' leakage : ',self.energy['total']['leakage'])
        print("active_components: ", 'internal : ', self.energy['active_components']['internal'], ' switching : ',self.energy['active_components']['switching'],  ' leakage : ',self.energy['active_components']['leakage'])
        print("inactive_components: ", 'internal : ', self.energy['inactive_components']['internal'], ' switching : ',self.energy['inactive_components']['switching'],  ' leakage : ',self.energy['inactive_components']['leakage'])
        print("Error: ", 'internal : ', self.energy_error['internal'], ' switching : ',self.energy_error['switching'],  ' leakage : ',self.energy_error['leakage'])
