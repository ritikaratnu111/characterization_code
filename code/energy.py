from power import Power
import json
import logging

class EnergyCalculator():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self, tb, assembly):
        self.tb = tb
        self.POWERFILES_PATH = f"{self.tb}/vcd/"
        self.assembly = assembly
        self.NetPower = Power()
        self.set_energy_structuctures()

    def set_energy_structuctures(self):
        for id in self.assembly.cells:
            
            self.assembly.cells[id]['power_types'] = {
                'internal','switching','leakage'
            }
            self.assembly.cells[id]['nets'] = {
                'active_component_nets' : {},
                'count' :                 {'active' : 0,'inactive' : 0,'total' : 0}
            }
            self.assembly.cells[id]['power'] = {
                'active_components' :   {},
                'inactive_components' : {'internal': 0,'switching' : 0,'leakage' : 0 },
                'total' :               {'internal': 0,'switching' : 0,'leakage' : 0 },
            }
            self.assembly.cells[id]['per_cycle_power'] = {
                'active_components' :   {},
                'inactive_components' : {'internal': 0,'switching' : 0,'leakage' : 0 },
                'total' :               {'internal': 0,'switching' : 0,'leakage' : 0 },
            }
            self.assembly.cells[id]['energy'] = {
                'predictor':{
                    'active_components' :   {},
                    'inactive_components' : {'internal': 0,'switching' : 0,'leakage' : 0 },
                    'total' :               {'internal': 0,'switching' : 0,'leakage' : 0 },
                },
                'actual':{
                    'active_components' :   {},
                    'inactive_components' : {'internal': 0,'switching' : 0,'leakage' : 0 },
                    'total' :               {'internal': 0,'switching' : 0,'leakage' : 0 },
                },
                'error':{
                    'active_components' :   {},
                    'inactive_components' : {'internal': 0,'switching' : 0,'leakage' : 0 },
                    'total' :               {'internal': 0,'switching' : 0,'leakage' : 0 },
                }
            }
            
            for component in self.assembly.cells[id]['active_components']:
                self.assembly.cells[id]['nets']['active_component_nets'][component] = 0
                self.assembly.cells[id]['power']['active_components'][component] = {
                    'internal' :    {'active' : {}, 'inactive' : {}},
                    'switching' :   {'active' : {}, 'inactive' : {}},
                    'leakage' :     0
                    }
                self.assembly.cells[id]['per_cycle_power']['active_components'][component] = {
                    'internal' : {},
                    'switching' : {},
                    'leakage' : {}
                    }
                self.assembly.cells[id]['energy']['predictor']['active_components'][component] = {
                    'internal' : {'active' : {}, 'inactive' : {}},
                    'switching' : {'active' : {}, 'inactive' : {}},
                    'leakage' : 0
                    }
                self.assembly.cells[id]['energy']['actual']['active_components'][component] = {
                    'internal' : {'active' : {}, 'inactive' : {}},
                    'switching' : {'active' : {}, 'inactive' : {}},
                    'leakage' : 0
                    }
                self.assembly.cells[id]['energy']['error']['active_components'][component] = {
                    'internal' : {'active' : {}, 'inactive' : {}},
                    'switching' : {'active' : {}, 'inactive' : {}},
                    'leakage' : 0
                    }


    def set_active_component_active_window_dynamic_energy(self):
        for id in self.assembly.cells:
            for component in self.assembly.cells[id]['active_components']:
                active_signals = self.assembly.cells[id]['active_components'][component]
                active_windows = self.assembly.cells[id]['component_active_cycles'][component]

                switching_energy = 0
                internal_energy = 0

                for window in active_windows:
                    start = window['start']
                    end = window['end']
                    duration = end - start
                    next = start
                    while (next < end):
                        duration = f"{next}_{next + self.CLOCK_PERIOD}"
                        switching_energy = switching_energy + self.assembly.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] * self.CLOCK_PERIOD
                        internal_energy = internal_energy + self.assembly.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] * self.CLOCK_PERIOD
                        next = next + self.CLOCK_PERIOD
                self.assembly.cells[id]['energy']['active_components'][component]['switching']['active'] = switching_energy
                self.assembly.cells[id]['energy']['active_components'][component]['internal']['active'] = internal_energy

    def set_active_component_inactive_window_dynamic_energy(self):
        for id in self.assembly.cells:
            for component in self.assembly.cells[id]['active_components']:
                active_signals = self.assembly.cells[id]['active_components'][component]
                inactive_windows = self.assembly.cells[id]['component_inactive_cycles'][component]

                switching_energy = 0
                internal_energy = 0

                for window in inactive_windows:
                    start = window['start']
                    end = window['end']
                    duration = end - start
                    next = start
                    while (next < end):
                        duration = f"{next}_{next + self.CLOCK_PERIOD}"
                        switching_energy = switching_energy + self.assembly.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] * self.CLOCK_PERIOD
                        internal_energy = internal_energy + self.assembly.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] * self.CLOCK_PERIOD
                        next = next + self.CLOCK_PERIOD
                self.assembly.cells[id]['energy']['active_components'][component]['switching']['inactive'] = switching_energy
                self.assembly.cells[id]['energy']['active_components'][component]['internal']['inactive'] = internal_energy
    
    def set_active_component_static_energy(self):
        for id in self.assembly.cells:
            for component in self.assembly.cells[id]['active_components']:
                active_signals = self.assembly.cells[id]['active_components'][component]

                leakage_energy = 0

                total_window = self.assembly.cells[id]['total_window']
                start = total_window['start']
                end = total_window['end']
                duration = end - start

                file_path = f"{self.tb}/vcd/{id}_total.vcd.pwr"
                self.NetPower.set_nets(file_path)
                self.NetPower.set_active_nets(active_signals)

                leakage_power, count = self.NetPower.get_active_component_leakage_power(active_signals)
                leakage_energy = leakage_power * duration
                self.assembly.cells[id]['energy']['active_components'][component]['leakage'] = leakage_energy


    def set_inactive_component_energy(self):
        for id in self.assembly.cells:
            total_window = self.assembly.cells[id]['total_window']

            leakage_energy = 0

            start = total_window['start']
            end = total_window['end']
            duration = end - start
            file_path = f"{self.POWERFILES_PATH}/total.vcd.pwr.nodimarch"
            self.NetPower.set_nets(file_path)

            active_components = self.assembly.cells[id]['active_components']

            print(active_components)

            for component in active_components:
                print(component)
                active_signals = active_components[component]
                self.NetPower.set_active_nets(active_signals)

            power, inactive_nets = self.NetPower.get_inactive_component_power()
            print(power)
            for type in self.assembly.cells[id]['power_types']:
                self.assembly.cells[id]['energy']['inactive_components'][type] = power[type] * duration

    def set_model_energy(self):
        for id in self.assembly.cells:

            for type in self.assembly.cells[id]['power_types']:
                self.assembly.cells[id]['energy']['model'][type] = self.assembly.cells[id]['energy']['inactive_components'][type]

            for component in self.assembly.cells[id]['active_components']:
                self.assembly.cells[id]['energy']['model']['internal'] += self.assembly.cells[id]['energy']['active_components'][component]['internal']['active']  \
                                                            + self.assembly.cells[id]['energy']['active_components'][component]['internal']['inactive'] 
                self.assembly.cells[id]['energy']['model']['switching'] += self.assembly.cells[id]['energy']['active_components'][component]['switching']['active']  \
                                                            + self.assembly.cells[id]['energy']['active_components'][component]['switching']['inactive'] 
                self.assembly.cells[id]['energy']['model']['leakage'] += self.assembly.cells[id]['energy']['active_components'][component]['leakage'] 

    def set_reference_energy(self):
        for id in self.assembly.cells:
            total_window = self.assembly.cells[id]['total_window']
            start = total_window['start']
            end = total_window['end']
            duration = end - start
            file_path = f"{self.tb}/vcd/{id}_total.vcd.pwr"
            self.NetPower.set_nets(file_path)

            power, total_nets = self.NetPower.get_total_power()
            for type in self.assembly.cells[id]['power_types']:
                self.assembly.cells[id]['energy']['reference'][type] = power[type] * duration

    def set_energy_error(self):
        for id in self.assembly.cells:
            for type in self.assembly.cells[id]['power_types']:
                self.assembly.cells[id]['energy']['error'][type] = (self.assembly.cells[id]['energy']['reference'][type] \
                                                            - self.assembly.cells[id]['energy']['model'][type]) * 100 \
                                                            /max(self.assembly.cells[id]['energy']['reference'][type],self.assembly.cells[id]['energy']['model'][type])

    def set_per_cycle_power(self):
    #Per cycle power of active component
        for id in self.assembly.cells:
            active_components = self.assembly.cells[id]['active_components']
            for component in active_components:
                print(component)
                logging.info('Component: %s', component)
                window = self.assembly.cells[id]['total_window']
                start = window['start'] 
                end = window['end'] 
                print(window)
                active_signals = self.assembly.cells[id]['active_components'][component]
                next = start
                while (next < end):
                    print(next)
                    file_path = f"{self.POWERFILES_PATH}/{next}_{next + self.CLOCK_PERIOD}.vcd.pwr"
                    duration = f"{next}_{next + self.CLOCK_PERIOD}"
                    next = next + self.CLOCK_PERIOD
                    self.NetPower.set_nets(file_path)
                    self.NetPower.set_active_nets(active_signals)
                    power, active_nets = self.NetPower.get_active_component_dynamic_power(active_signals)
                    for type in self.assembly.cells[id]['power_types']:
                        self.assembly.cells[id]['per_cycle_power']['active_components'][component][type][duration] = power[type]
#                    self.assembly.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration] = 0
#                    self.assembly.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration] = 0
#                    self.assembly.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration] = 0

    def log(self):
        #Log per cycle power of active component
        for id in self.assembly.cells:
            for component in self.assembly.cells[id]['active_components']:
                logging.info('Per cycle power for cell %s:', id)
                logging.info('     %s:', component)
                columns = ['Duration', 'Internal', 'Switching', 'Leakage']
                log_message = '  '.join([col.ljust(20) for col in columns])
                logging.info(log_message)
                for duration in self.assembly.cells[id]['per_cycle_power']['active_components'][component]['internal']:
                    logging.info('     %s %s %s %s ', duration.ljust(20), 
                                       str(round(self.assembly.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration],3)).ljust(20),
                                          str(round(self.assembly.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration],3)).ljust(20),
                                            str(round(self.assembly.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration],3)).ljust(20))
