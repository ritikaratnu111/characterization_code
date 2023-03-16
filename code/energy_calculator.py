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

        self.active_component_energy = {}
        self.inactive_component_energy = {} 
        self.estimated_energy = {} 
        self.total_energy = {}
        self.energy = {}
        self.energy_error = {}

        self.net_count = {}
        self.active_net_count = 0
        self.inactive_net_count = 0
        self.total_net_count = 0
        
        self.set_power()
        self.set_energy()
        self.print_energy()

    def set_active_window_power(self,component):
        signals = self.active_components[component]
        print('Active power for: ',component ,' ', signals)
        for window in self.active_windows[component]:
            active_component_active_power_file = self.tb + "/vcd/" + component + "_active_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
            self.NetPower.set_nets(active_component_active_power_file)
            self.NetPower.set_active_nets(signals)
            duration = str(window['start']) + "_" + str(window['end']) 
            self.active_component_power[component]['active'][duration], self.net_count[component] = self.NetPower.get_active_component_power(signals)

    def set_inactive_window_power(self,component):
        signals = self.active_components[component]
        print('Inactive power for: ',component ,' ', signals)
        for window in self.inactive_windows[component]:
            active_component_inactive_power_file = self.tb + "/vcd/" + component + "_inactive_" + str(window['start']) + "_" + str(window['end']) + ".vcd.pwr"
    #       print(component,signals,window)
            self.NetPower.set_nets(active_component_inactive_power_file)
            self.NetPower.set_active_nets(signals)
            duration = str(window['start']) + "_" + str(window['end']) 
            self.active_component_power[component]['inactive'][duration], self.net_count[component] = self.NetPower.get_active_component_power(signals)

    def set_active_component_power(self):
        print("Computing active component power... ")
        for component in self.active_components:
            self.net_count[component] = 0
            self.active_component_power[component] = {'active': {}, 'inactive': {}}
            self.set_active_window_power(component)
            self.set_inactive_window_power(component)
            self.active_net_count += self.net_count[component]

    def set_inactive_component_power(self):
        print("Computing inactive component power... ")
        inactive_component_power_file = self.tb + "/vcd/" + "total" + "_active_" + str(self.total_window['start']) + "_" + str(self.total_window['end']) + ".vcd.pwr"
        self.NetPower.set_nets(inactive_component_power_file)
        duration = str(self.total_window['start']) + "_" + str(self.total_window['end']) 
        for component in self.active_components:
            signals = self.active_components[component]
            self.NetPower.set_active_nets(signals)
        self.inactive_component_power, self.inactive_net_count = self.NetPower.get_inactive_component_power()

    def set_total_power(self):
        print("Computing total component power... ")
        active_power = {'internal': 0, 'switching': 0, 'leakage': 0}
        self.total_power = {'internal': 0, 'switching': 0, 'leakage': 0}
        power_file = self.tb + "/vcd/" + "total" + "_active_" + str(self.total_window['start']) + "_" + str(self.total_window['end']) + ".vcd.pwr"
        for component in self.active_components:
            signals = self.active_components[component]
            print('Actual power for: ',component ,' ', signals)
            self.NetPower.set_nets(power_file)
            self.NetPower.set_active_nets(signals)
            component_power, self.net_count[component] = self.NetPower.get_active_component_power(signals)
            for power_type in component_power:
                active_power[power_type] += component_power[power_type]

        for power_type in self.total_power:
            self.total_power[power_type] = self.inactive_component_power[power_type] + active_power[power_type]              #The inactive power is independent of windows

    def set_power(self):
        self.set_active_component_power()
        self.set_inactive_component_power()
        self.set_total_power()
        self.total_net_count = self.active_net_count + self.inactive_net_count
        print('Net count... :')
        print('Active components: ', self.active_net_count,' Inactive components: ', self.inactive_net_count,' Total: ', self.total_net_count)

    def set_active_component_energy(self):
        print("Computing active component energy... ")
        self.active_component_energy = {'internal': 0, 'switching': 0, 'leakage' : 0}
        print('Active component, state, duration:')
        for component in self.active_components:
            self.energy[component] = {'active': {}, 'inactive': {}}
            for state in self.active_component_power[component]:
                for duration in self.active_component_power[component][state]:
                    self.energy[component][state][duration] = {'internal': 0, 'switching': 0, 'leakage' : 0} 
                    start = int(duration.split('_')[0])
                    end = int(duration.split('_')[1])
                    time = end - start
                    for power_type in self.active_component_power[component][state][duration]:
                        self.energy[component][state][duration][power_type] = time * self.active_component_power[component][state][duration][power_type]
                        self.active_component_energy[power_type] += self.energy[component][state][duration][power_type]
#                    print(component, state, duration,self.energy[component][state][duration])

    def set_inactive_component_energy(self):
        print("Computing inactive component energy... ")
        self.inactive_component_energy = {'internal': 0, 'switching': 0, 'leakage' : 0}
        start = self.total_window['start']
        end = self.total_window['end']
        time = end - start
        for power_type in self.total_power:
            self.inactive_component_energy[power_type] = time * self.inactive_component_power[power_type]

    def set_total_energy(self):
        print("Computing total component energy... ")
        self.total_energy = {'internal': 0, 'switching': 0, 'leakage' : 0}
        start = self.total_window['start']
        end = self.total_window['end']
        time = end - start
        for power_type in self.total_power:
            self.total_energy[power_type] = time * self.total_power[power_type]

    def set_energy_error(self):
        self.energy_error = {'internal': 0, 'switching': 0, 'leakage' : 0}
        for power_type in self.total_power:
            estimate = self.active_component_energy[power_type] + self.inactive_component_energy[power_type]
            actual = self.total_energy[power_type]
            self.estimated_energy[power_type] = estimate
            self.energy_error[power_type] = (actual - estimate) * 100 /max(actual,estimate)

    def set_energy(self):
        self.set_active_component_energy()
        self.set_inactive_component_energy()
        self.set_total_energy()
        self.set_energy_error()

    def print_energy(self):
        print("Actual: ", 'internal : ', self.total_energy['internal'], ' switching : ',self.total_energy['switching'],  ' leakage : ',self.total_energy['leakage'])
        print("Estimate: ", 'internal : ', self.estimated_energy['internal'], ' switching : ',self.estimated_energy['switching'],  ' leakage : ',self.estimated_energy['leakage'])
        print("Error: ", 'internal : ', self.energy_error['internal'], ' switching : ',self.energy_error['switching'],  ' leakage : ',self.energy_error['leakage'])
