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
                'reference' : {
                    'internal': 0,
                    'switching' : 0,
                    'leakage' : 0 },
                'model' : {
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

    def set_active_component_active_window_dynamic_energy(self):
        for id in self.cells:
            for component in self.cells[id]['active_components']:
                active_signals = self.cells[id]['active_components'][component]
                active_windows = self.cells[id]['component_active_cycles'][component]

                switching_energy = 0
                internal_energy = 0

                for window in active_windows:
                    start = window['start']
                    end = window['end']
                    duration = end - start
                    next = start
                    while (next < end):
                        duration = f"{next}_{next + self.CLOCK_PERIOD}"
                        switching_energy = switching_energy + self.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] * self.CLOCK_PERIOD
                        internal_energy = internal_energy + self.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] * self.CLOCK_PERIOD
                        next = next + self.CLOCK_PERIOD
                self.cells[id]['energy']['active_components'][component]['switching']['active'] = switching_energy
                self.cells[id]['energy']['active_components'][component]['internal']['active'] = internal_energy

    def set_active_component_inactive_window_dynamic_energy(self):
        for id in self.cells:
            for component in self.cells[id]['active_components']:
                active_signals = self.cells[id]['active_components'][component]
                inactive_windows = self.cells[id]['component_inactive_cycles'][component]

                switching_energy = 0
                internal_energy = 0

                for window in inactive_windows:
                    start = window['start']
                    end = window['end']
                    duration = end - start
                    next = start
                    while (next < end):
                        duration = f"{next}_{next + self.CLOCK_PERIOD}"
                        switching_energy = switching_energy + self.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] * self.CLOCK_PERIOD
                        internal_energy = internal_energy + self.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] * self.CLOCK_PERIOD
                        next = next + self.CLOCK_PERIOD
                self.cells[id]['energy']['active_components'][component]['switching']['inactive'] = switching_energy
                self.cells[id]['energy']['active_components'][component]['internal']['inactive'] = internal_energy
    
    def set_active_component_static_energy(self):
        for id in self.cells:
            for component in self.cells[id]['active_components']:
                active_signals = self.cells[id]['active_components'][component]

                leakage_energy = 0

                total_window = self.cells[id]['total_window']
                start = total_window['start']
                end = total_window['end']
                duration = end - start

                file_path = f"{self.tb}/vcd/{id}_total.vcd.pwr"
                self.NetPower.set_nets(file_path)
                self.NetPower.set_active_nets(active_signals)

                leakage_power, count = self.NetPower.get_active_component_leakage_power(active_signals)
                leakage_energy = leakage_power * duration
                self.cells[id]['energy']['active_components'][component]['leakage'] = leakage_energy


    def set_inactive_component_energy(self):
        for id in self.cells:
            total_window = self.cells[id]['total_window']

            leakage_energy = 0

            start = total_window['start']
            end = total_window['end']
            duration = end - start
            file_path = f"{self.tb}/vcd/{id}_total.vcd.pwr"
            self.NetPower.set_nets(file_path)

            active_components = self.cells[id]['active_components']

            for component in active_components:
                active_signals = active_components[component]
                self.NetPower.set_active_nets(active_signals)

            power, inactive_nets = self.NetPower.get_inactive_component_power()
            for type in self.cells[id]['power_types']:
                self.cells[id]['energy']['inactive_components'][type] = power[type] * duration

    def set_model_energy(self):
        for id in self.cells:

            for type in self.cells[id]['power_types']:
                self.cells[id]['energy']['model'][type] = self.cells[id]['energy']['inactive_components'][type]

            for component in self.cells[id]['active_components']:
                self.cells[id]['energy']['model']['internal'] += self.cells[id]['energy']['active_components'][component]['internal']['active']  \
                                                            + self.cells[id]['energy']['active_components'][component]['internal']['inactive'] 
                self.cells[id]['energy']['model']['switching'] += self.cells[id]['energy']['active_components'][component]['switching']['active']  \
                                                            + self.cells[id]['energy']['active_components'][component]['switching']['inactive'] 
                self.cells[id]['energy']['model']['leakage'] += self.cells[id]['energy']['active_components'][component]['leakage'] 

    def set_reference_energy(self):
        for id in self.cells:
            total_window = self.cells[id]['total_window']
            start = total_window['start']
            end = total_window['end']
            duration = end - start
            file_path = f"{self.tb}/vcd/{id}_total.vcd.pwr"
            self.NetPower.set_nets(file_path)

            power, total_nets = self.NetPower.get_total_power()
            for type in self.cells[id]['power_types']:
                self.cells[id]['energy']['reference'][type] = power[type] * duration

    def set_energy_error(self):
        for id in self.cells:
            for type in self.cells[id]['power_types']:
                self.cells[id]['energy']['error'][type] = (self.cells[id]['energy']['reference'][type] \
                                                            - self.cells[id]['energy']['model'][type]) * 100 \
                                                            /max(self.cells[id]['energy']['reference'][type],self.cells[id]['energy']['model'][type])

    def set_per_cycle_power(self):
    #Per cycle power of active component
        for id in self.cells:
            active_components = self.cells[id]['active_components']
            for component in active_components:
                print(component)
                window = self.cells[id]['total_window']
                start = window['start']
                end = window['end'] 
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
                    for type in self.cells[id]['power_types']:
                        self.cells[id]['per_cycle_power']['active_components'][component][type][duration] = power[type]
#                    self.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] = 0
#                    self.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] = 0
#                    self.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration] = 0
