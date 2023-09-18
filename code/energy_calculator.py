from power import Power
import json
import logging

class EnergyCalculator():

    def __init__(self, tb, loader.cells):
        self.tb = tb
        self.POWERFILES_PATH = f"{self.tb}/vcd/"
        self.cells = loader.cells
        self.NetPower = Power()

    def set_active_component_dynamic_energy(self,file):
        for cell in self.cells:
            for component in cell.components.active:
                duration = cell.total_window['end'] - cell.total_window['start']
                internal_energy = 0
                switching_energy = 0
                self.NetPower.set_nets(file)
                self.NetPower.set_active_nets(component.signals)
                power, active_nets = self.NetPower.get_active_component_dynamic_power(component.signals)
                internal_energy = power['internal'] * duration
                switching_energy = power['switching'] * duration
                component.PowerProfile.active.energy.internal = internal_energy
                component.PowerProfile.active.energy.switching = switching_energy


    def set_active_component_static_energy(self,file):
        for cell in self.cells:
            for component in cell.components.active:
                duration = cell.total_window['end'] - cell.total_window['start']
                leakage_energy = 0
                self.NetPower.set_nets(file)
                self.NetPower.set_active_nets(component.signals)
                leakage_power, count = self.NetPower.get_active_component_leakage_power(component.signals)
                leakage_energy = leakage_power * duration
                component.PowerProfile.active.energy.leakage = leakage_energy


    def set_inactive_component_energy(self,file):
        for cell in self.cells:
            leakage_energy = 0
            duration = cell.total_window['end'] - cell.total_window['start']
            self.NetPower.set_nets(file)
            active_components = cell.components.active

            for component in active_components:
                print(component)
                active_signals = component.signals
                self.NetPower.set_active_nets(active_signals)

            power, inactive_nets = self.NetPower.get_inactive_component_power()

            cell.PowerProfile.inactive.energy.internal = power['internal'] * duration
            cell.PowerProfile.inactive.energy.switching = power['switching'] * duration
            cell.PowerProfile.inactive.energy.leakage = power['leakage'] * duration
            cell.PowerProfile.inactive.energy.window = cell.total_window


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
