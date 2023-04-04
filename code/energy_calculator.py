import logging
from power import Power

class EnergyCalculator():
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
                    'leakage' : {
                        'active' : {}, 
                        'inactive' : {}}}
                self.cells[id]['energy']['active_components'][component] = {
                    'internal' : {
                        'active' : {}, 
                        'inactive' : {}},
                    'switching' : {
                        'active' : {}, 
                        'inactive' : {}},
                    'leakage' : {
                        'active' : {}, 
                        'inactive' : {}}}

    def set_active_window_power(self,id,component):
        active_signals = self.cells[id]['active_components'][component]
        logging.debug(f"Active power for {component}: {active_signals}")

        active_windows = self.cells[id]['component_active_cycles'][component]

        for window in active_windows:
            file_path = f"{self.tb}/vcd/{id}_{component}_active_{window['start']}_{window['end']}.vcd.pwr" #choose active window power file
            duration = f"{window['start']}_{window['end']}"

            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(active_signals)

            power, active_nets = self.NetPower.get_active_component_power(signals)
            power_types = self.cell['id']['power_types']
            for power_type in power_types:
                self.cells[id]['power']['active_components'][component][power_type]['active'][duration] = power[power_type]
            
            self.cells[id]['nets']['active_component_nets'][component] = active_nets

    def set_inactive_window_power(self,id,component):
        active_signals = self.cells[id]['active_components'][component]
        logging.debug(f"Active power for {component}: {signals}")

        active_windows = self.cells[id]['component_active_cycles'][component]

        for window in active_windows:
            file_path = f"{self.tb}/vcd/{self.id}_{component}_inactive_{window['start']}_{window['end']}.vcd.pwr" # choose inactive window power file
            duration = f"{window['start']}_{window['end']}"

            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(active_signals)

            power, active_nets = self.NetPower.get_active_component_power(signals)
            power_types = self.cell['id']['power_types']
            for power_type in power_types:
                self.cells[id]['power']['active_components'][component][power_type]['inactive'][duration] = power[power_type]
            
            self.cells[id]['nets']['active_component_nets'][component] = active_nets

    def set_active_component_power(self,id):
        logging.debug("Computing active component power...")

        active_components = self.cells[id]['active_components']

        for component in active_components:
            self.set_active_window_power(id,component)
            self.set_inactive_window_power(id,component)
            self.cells[id]['nets']['count']['active'] += self.cells[id]['nets']['active_component_nets'][component]

    def set_inactive_component_power(self,id):
        logging.debug("Computing inactive component power... ")

        file_path = f"{self.tb}/vcd/{self.cell_id}_total__{self.total_window['start']}_{self.total_window['end']}.vcd.pwr"
        self.NetPower.set_nets(file_path)

        duration = f"{self.total_window['start']}_{self.total_window['end']}"
        active_components = self.cells[id]['active_components']

        for component in active_components:
            active_signals = active_components[component]
            self.NetPower.set_active_nets(active_signals)

        power, inactive_nets = self.NetPower.get_inactive_component_power()

        power_types = self.cell['id']['power_types']
        for power_type in power_types:
            self.cells[id]['power']['inactive_components'][power_type] = power[power_type]

        self.cells[id]['nets']['count']['inactive'] = inactive_nets

    def set_total_power(self,id):
        logging.debug("Computing total component power... ")
        file_path = f"{self.tb}/vcd/{self.cell_id}_total__{self.total_window['start']}_{self.total_window['end']}.vcd.pwr"

        active_components = self.cells[id]['active_components']
        power_types = self.cell['id']['power_types']
        active_component_power = {ptype: 0 for ptype in power_types}

        for component in active_components:
            signals = self.cells[id]['active_components'][component]
            logging.debug(f"Actual power for: {component} {signals}")
            self.NetPower.set_nets(file_path)
            self.NetPower.set_active_nets(signals)
            power, count = self.NetPower.get_active_component_power(signals)
            power_types = self.cell['id']['power_types']
            for power_type in power_types:
                active_component_power[power_type] += power[power_type]

        for power_type in power_types:
            active_power = active_component_power[power_type]
            inactive_power = self.cells[id]['power']['inactive_components'][power_type]
            total_power = inactive_power + active_power
            self.cells[id]['power']['total'][power_type] = total_power 

    def set_power(self):
        for id in self.cells:
            self.set_active_component_power(id)
            self.set_inactive_component_power(id)
            self.set_total_power(id)
            self.cells[id]['nets']['count']['total'] = self.cells[id]['nets']['count']['active'] + self.cells[id]['nets']['count']['inactive']
            logging.debug('Net count... :')
            logging.debug('Active components: ', self.cells[id]['nets']['count']['active'],
                         ' Inactive components: ', self.cells[id]['nets']['count']['inactive'],
                         ' Total: ', self.cells[id]['nets']['count']['total'])

    def set_active_component_energy(self,id):
        logging.debug("Computing active component energy... ")
        logging.debug('Active component, state, duration:')
        
        active_components = self.cells[id]['active_components']

        power_types = self.cell['id']['power_types']

        for component in active_components:
            power = self.cells[id]['power']['active_components'][component]
            for power_type in power_types:
                states = power[power_type]
                for state in states:
                    durations = power[power_type][state]
                    for duration in durations:
                        start, end = map(int, duration.split('_'))
                        time = end - start
                        energy = time * power[power_type][state][duration]
                        self.cells[id]['active_components'][component][power_type][state][duration] = energy

    def set_inactive_component_energy(self,id):
        logging.debug("Computing inactive component energy... ")
        start, end = map(int, duration.split('_'))
        time = end - start
        power = self.cells[id]['power']['inactive_components']
        power_types = self.cell['id']['power_types']
        
        energy = { power_type: time * power[power_type] 
                for power_type in power_types}

        self.cells[id]['energy']['inactive_components'] = energy

    def set_total_energy(self,id):
        logging.debug("Computing total component energy... ")
        start, end = map(int, duration.split('_'))
        time = end - start
        power = self.cells[id]['power']['total']
        power_types = self.cell[id]['power_types']
        energy = {power_type: time * power[power_type] 
                for power_type in power_types}

        self.cells[id]['energy']['total'] = energy

    def set_energy_error(self,id):
        inactive_energy = self.cells[id]['energy']['inactive_components']
        total_energy = self.cells[id]['energy']['total']
        power_types = self.cell[id]['power_types']

        active_energy = {power_type: sum(
                    self.cells[id]['active_components'][component][power_type][state][duration]
        for component in self.cells[id]['active_components']
        for state in states
        for duration in durations)
                     for power_type in power_types}

        estimated_energy = {power_type: active_energy[power_type] + inactive_energy[power_type]
                        for power_type in power_types}

        energy_error = {power_type: (total_energy[power_type] - estimated_energy[power_type]) * 100 /
                    max(total_energy[power_type], estimated_energy[power_type])
                    for power_type in power_types}

        self.cells[id]['energy']['estimate'][power_type] = estimate
        self.cells[id]['energy']['error'][power_type] = error

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
            power_types = self.cell[id]['power_types']
            energy = self.cells[id]['energy']
            for power_type in power_types:
                actual_energy = energy['total'][power_type]
                estimated_energy = energy['estimated'][power_type]
                energy_error = energy['error'][power_type]
                print(f"{power_type.capitalize()}: actual={actual_energy}, estimate={estimated_energy}, error={energy_error}")
