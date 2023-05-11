from power import Power
import json

class EnergyCalculator():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.tb = ""
        self.cells = {}
        self.NetPower = Power()

    def set_assembly_file(self, tb):
        self.tb = tb

    def set_input(self,assembly):
        self.cells = assembly.cells

    def set_model(self):
        for id in self.cells:
            self.cells[id]['power_types'] = {
                'internal',
                'switching',
                'leakage'
            }
            self.cells[id]['nets'] = {
                'active_component_nets' : {},
                'count' : {
                    'active' : 0,
                    'inactive' : 0,
                    'total' : 0}
            }
            self.cells[id]['power'] = {
                'active_components' : {},
                'inactive_components' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'total' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
            }
            self.cells[id]['per_cycle_power'] = {
                'active_components' : {},
                'inactive_components' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'total' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
            }
            self.cells[id]['energy'] = {
                'active_components' : {},
                'inactive_components' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'total' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'estimate' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'error' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 }
                }
            for component in self.cells[id]['active_components']:
                self.cells[id]['nets']['active_component_nets'][component] = 0
                self.cells[id]['power']['active_components'][component] = {
                    'internal' : {
                         'active' : {}, 
                         'inactive' : {}},
                    'switching' : {
                        'active' : {}, 
                        'inactive' : {}},
                    'leakage' : 0
                    }
                self.cells[id]['per_cycle_power']['active_components'][component] = {
                    'internal' : {},
                    'switching' : {},
                    'leakage' : {}
                    }
                self.cells[id]['energy']['active_components'][component] = {
                    'internal' : {
                        'active' : {}, 
                        'inactive' : {}},
                    'switching' : {
                        'active' : {}, 
                        'inactive' : {}},
                    'leakage' : 0
                    }

    def set_active_window_dynamic_power(self,id,component):
        active_signals = self.cells[id]['active_components'][component]

        component_active_windows = self.cells[id]['component_active_cycles'][component]
#        print(active_windows)
        active_windows = []
        total_window = self.cells[id]['total_window']
        start = total_window['start']
        end = total_window['end']
        next = start + self.CLOCK_PERIOD
        while next <= end:
            active_windows.append({'start': start, 'end': next}) 
            start = next
            next = start + self.CLOCK_PERIOD
        print(component, "active window: ", component_active_windows)        

        for window in active_windows:
#            file_path = f"{self.tb}/vcd/{id}_{component}_active_{window['start']}_{window['end']}.vcd.pwr" #choose active window power file
            file_path = f"{self.tb}/vcd/{id}_all__{window['start']}_{window['end']}.vcd.pwr" #choose active window power file
            duration = f"{window['start']}_{window['end']}"
    
            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(active_signals)

            power, active_nets = self.NetPower.get_active_component_dynamic_power(active_signals)
#            power_types = self.cells[id]['power_types']
#            for power_type in power_types:
#                self.cells[id]['power']['active_components'][component][power_type]['active'][duration] = power[power_type]

            print(window,power)
            self.cells[id]['power']['active_components'][component]['internal']['active'][duration] = power['internal']
            self.cells[id]['power']['active_components'][component]['switching']['active'][duration] = power['switching']
            
            self.cells[id]['nets']['active_component_nets'][component] = active_nets

    def set_inactive_window_dynamic_power(self,id,component):
        active_signals = self.cells[id]['active_components'][component]

        inactive_windows = self.cells[id]['component_inactive_cycles'][component]

        for window in inactive_windows:
            file_path = f"{self.tb}/vcd/{id}_{component}_inactive_{window['start']}_{window['end']}.vcd.pwr" # choose inactive window power file
            duration = f"{window['start']}_{window['end']}"

            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(active_signals)

            power, active_nets = self.NetPower.get_active_component_dynamic_power(active_signals)
#            power_types = self.cells[id]['power_types']
#            for power_type in power_types:
#                self.cells[id]['power']['active_components'][component][power_type]['inactive'][duration] = power[power_type]
            
            self.cells[id]['power']['active_components'][component]['internal']['inactive'][duration] = power['internal']
            self.cells[id]['power']['active_components'][component]['switching']['inactive'][duration] = power['switching']

    def set_per_cycle_power(self,id,component):
        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end'] + 5 * self.CLOCK_PERIOD
        active_signals = self.cells[id]['active_components'][component]
        next = start
        while (next < end):
            print(next)
            file_path = f"{self.tb}/vcd/{id}_{next}_{next + self.CLOCK_PERIOD}.vcd.pwr"
            duration = f"{next}_{next + self.CLOCK_PERIOD}"
            next = next + self.CLOCK_PERIOD
            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(active_signals)
            power, active_nets = self.NetPower.get_active_component_dynamic_power(active_signals)
            self.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] = power['internal']
            self.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] = power['switching']
            self.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration] = power['leakage']

    def set_leakage_power(self,id,component):
        active_signals = self.cells[id]['active_components'][component]
        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end']

        file_path = f"{self.tb}/vcd/{id}_total__{start}_{end}.vcd.pwr"
        self.NetPower.set_nets(file_path)
        self.NetPower.set_active_nets(active_signals)
        leakage_power, active_nets = self.NetPower.get_active_component_leakage_power(active_signals)

        self.cells[id]['power']['active_components'][component]['leakage'] = leakage_power

    def set_active_component_power(self,id):
        active_components = self.cells[id]['active_components']
        for component in active_components:
            print(component)
            self.set_per_cycle_power(id,component)
#            self.set_active_window_dynamic_power(id,component)
#            self.set_inactive_window_dynamic_power(id,component)
#            self.set_leakage_power(id,component)
#            self.cells[id]['nets']['count']['active'] += self.cells[id]['nets']['active_component_nets'][component]

    def set_inactive_component_power(self,id):

        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end']

        file_path = f"{self.tb}/vcd/{id}_total__{start}_{end}.vcd.pwr"
        self.NetPower.set_nets(file_path)

        active_components = self.cells[id]['active_components']

        for component in active_components:
            active_signals = active_components[component]
            self.NetPower.set_active_nets(active_signals)

        power, inactive_nets = self.NetPower.get_inactive_component_power()

        power_types = self.cells[id]['power_types']
        for power_type in power_types:
            self.cells[id]['power']['inactive_components'][power_type] = power[power_type]

        self.cells[id]['nets']['count']['inactive'] = inactive_nets

    def set_total_power(self,id):

        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end']

        file_path = f"{self.tb}/vcd/{id}_total__{start}_{end}.vcd.pwr"
        active_components = self.cells[id]['active_components']
        power_types = self.cells[id]['power_types']
        active_component_power = {ptype: 0 for ptype in power_types}

        active_windows = self.cells[id]['component_active_cycles'][component]

        for component in active_components:
            signals = self.cells[id]['active_components'][component]
            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(signals)
            dynamic_power, count = self.NetPower.get_active_component_dynamic_power(signals)
            leakage_power, count = self.NetPower.get_active_component_leakage_power(signals)
            active_component_power['internal'] += dynamic_power['internal']
            active_component_power['switching'] += dynamic_power['switching']
            active_component_power['leakage'] += leakage_power

        for power_type in power_types:
            active_power = active_component_power[power_type]
            inactive_power = self.cells[id]['power']['inactive_components'][power_type]
            total_power = inactive_power + active_power
            self.cells[id]['power']['total'][power_type] = total_power 

    def set_power(self):
        for id in self.cells:
            self.set_active_component_power(id)
#            self.set_inactive_component_power(id)
#            self.set_total_power(id)
#            self.cells[id]['nets']['count']['total'] = self.cells[id]['nets']['count']['active'] + self.cells[id]['nets']['count']['inactive']
#                         ' Inactive components: ', self.cells[id]['nets']['count']['inactive'],
#                         ' Total: ', self.cells[id]['nets']['count']['total'])

    def set_active_component_energy(self,id):
        active_components = self.cells[id]['active_components']

        for component in active_components:
            power = self.cells[id]['power']['active_components'][component]
            states = {'active', 'inactive'}
            for state in states:
                durations = power['internal'][state]
                for duration in durations:
                    start, end = map(int, duration.split('_'))
                    time = end - start
                    energy = time * power['internal'][state][duration]
                    self.cells[id]['energy']['active_components'][component]['internal'][state][duration] = energy
                    energy = time * power['switching'][state][duration]
                    self.cells[id]['energy']['active_components'][component]['switching'][state][duration] = energy

        for component in active_components:
            power = self.cells[id]['power']['active_components'][component]
            window = self.cells[id]['total_window']
            start = window['start']
            end = window['end']
            time = end - start
            energy = time * power['leakage']
            self.cells[id]['energy']['active_components'][component]['leakage'] = energy

    def set_inactive_component_energy(self,id):
        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end']
        time = end - start
        power = self.cells[id]['power']['inactive_components']
        power_types = self.cells[id]['power_types']
        
        energy = { power_type: time * power[power_type] 
                for power_type in power_types}

        self.cells[id]['energy']['inactive_components'] = energy

    def set_total_energy(self,id):
        window = self.cells[id]['total_window']
        start = window['start']
        end = window['end']
        time = end - start
        power = self.cells[id]['power']['total']
        power_types = self.cells[id]['power_types']
        energy = {power_type: time * power[power_type] 
                for power_type in power_types}

        self.cells[id]['energy']['total'] = energy

    def set_energy_error(self,id):
        inactive_energy = self.cells[id]['energy']['inactive_components']
        total_energy = self.cells[id]['energy']['total']
        power_types = self.cells[id]['power_types']

        active_energy = {ptype: 0 for ptype in power_types}

        for component in self.cells[id]['active_components']:
            states = {'active', 'inactive'}
            for state in states:
                durations = self.cells[id]['energy']['active_components'][component]['internal'][state] 
                for duration in durations:
                    active_energy['internal'] += self.cells[id]['energy']['active_components'][component]['internal'][state][duration]
                    active_energy['switching'] += self.cells[id]['energy']['active_components'][component]['switching'][state][duration]

        for component in self.cells[id]['active_components']:
            active_energy['leakage'] += self.cells[id]['energy']['active_components'][component]['leakage']

        estimated_energy = {power_type: active_energy[power_type] + inactive_energy[power_type]
                        for power_type in power_types}

        energy_error = {power_type: (total_energy[power_type] - estimated_energy[power_type]) * 100 /
                    max(total_energy[power_type], estimated_energy[power_type])
                    for power_type in power_types}

        self.cells[id]['energy']['estimate'] = estimated_energy
        self.cells[id]['energy']['error'] = energy_error

    def set_energy(self):
        for id in self.cells:
            self.set_active_component_energy(id)
            self.set_inactive_component_energy(id)
            self.set_total_energy(id)
            self.set_energy_error(id)
    
    def write_reports(self):
        file_path = f"{self.tb}/energy_report.json"
        with open(file_path, 'w') as outfile:
            for id in self.cells:
                json.dump(self.cells[id]['power'], outfile)
                json.dump(self.cells[id]['energy']['error'], outfile)

    def print_energy(self):
        for id in self.cells:
            power_types = self.cells[id]['power_types']
            energy = self.cells[id]['energy']
            for power_type in power_types:
                actual_energy = energy['total'][power_type]
                estimated_energy = energy['estimate'][power_type]
                energy_error = energy['error'][power_type]
                print(f"{power_type.capitalize()}: actual={actual_energy}, estimate={estimated_energy}, error={energy_error}")
