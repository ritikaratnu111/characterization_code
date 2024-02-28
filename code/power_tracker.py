import os
import logging
import random
import constants
from openpyxl import Workbook
from innovus_reader import InnovusPowerParser
from measurement import Measurement
import json
import matplotlib.pyplot as plt
import numpy as np

class SimulationPowerTracker():
    def __init__(self, tb, start, end):     
        self.tb = tb
        self.start = start
        self.end = end
        self.reader = InnovusPowerParser()

    def get_per_cycle_measurement(self, cells):
            print("Getting per cycle measurement")
            per_cycle_window = []
            for cell in cells:
                current_start = cell.total_window['start']
                while current_start < cell.total_window['end']:
                    per_cycle_window.append({'start': current_start, 'end': current_start + constants.CLOCK_PERIOD, 'clock_cycles' : 1})
                    current_start += constants.CLOCK_PERIOD        
                logging.info("Setting per_cycle measurement for %s", cell.drra_tile)
                for component in cell.components.active:
                    logging.info("Setting per_cycle measurement for %s", component.name)
                    for window in per_cycle_window:
                        pwr_file = f"./vcd/{window['start']}.vcd.pwr"
                        if os.path.exists(pwr_file):
                            self.reader.update_nets(pwr_file)
                            # if(component.name != "noc"):
                            #     continue
                            logging.info(f"{component.name}, {window}, {pwr_file}")
                            component.profiler.set_per_cycle_measurement(self.reader, component.signals)

    def set_cell_measurement_and_nets(self, cell):
        print(cell.cell_id,cell.tiles,cell.total_window)
        cell.profiler.set_measurement(self.reader,cell.tiles, cell.components.active)
        nets = cell.profiler.measurement_set.actual.nets
        return nets

    def set_component_measurement_and_nets(self, component):
        logging.info('%s %s %s',component.name, component.signals, component.active_window)
        component.profiler.set_measurement(self.reader)
        nets = component.profiler.measurement.actual.nets
        return nets

    def update_cell_measurement(self, cell, component):
        T = cell.total_window['clock_cycles']
        cell.profiler.measurement_set.active.add(
            T, T, T,
            cell.profiler.measurement_set.active, 
            component.profiler.measurement.predicted
            )
        cell.profiler.measurement_set.set_predicted()
        cell.profiler.measurement_set.set_error()
        cell.profiler.measurement_set.error.log()

    def get_measurements(self, cells):
        for i in range(self.start,self.end):
            self.reader = InnovusPowerParser()
            pwr_file=f"{self.tb}/vcd/iter_{i}.vcd.pwr"
            json_file=f"{self.tb}/vcd/iter_{i}.json"

            if os.path.exists(pwr_file) and not os.path.exists(json_file):
                total_nets = 0
                balance = 0
                accounted_nets = 0
                self.reader.update_nets(pwr_file)

                for cell in cells:
                    total_nets = self.set_cell_measurement_and_nets(cell)
                    balance_nets = total_nets

                    logging.debug('%s %s', balance_nets, (balance_nets / total_nets) * 100)
                    
                    self.reader.remove_labels(cell.tiles)
                    
                    for component in cell.components.active:
                        self.reader.get_count_of_inactive_labels(cell.tiles)
                        #if(component.name != "dpu"):
                        #    continue
                        component_nets = self.set_component_measurement_and_nets(component)
                        accounted_nets += component_nets
                        balance_nets = total_nets - accounted_nets
                        self.update_cell_measurement(cell, component)

                        logging.info('%s %s %s',component_nets, balance_nets, (balance_nets / total_nets) * 100)
#                        
                self.write_json(i,cells)

    def get_component_dict(self, component):
        dict = {
                "active": {
                    "window": f"{component.profiler.active_window['windows']}" if component.active_window else "None",
                    "cycles": component.profiler.active_window['clock_cycles'] if component.active_window else 0,
                    "power": {
                        "internal": component.profiler.measurement.active.power.internal,
                        "switching": component.profiler.measurement.active.power.switching,
                        "leakage": component.profiler.measurement.active.power.leakage
                    }
                },
                "inactive": {
                    "window": f"{component.profiler.inactive_window['windows']}" if component.inactive_window else "None",
                    "cycles": component.profiler.inactive_window['clock_cycles'] if component.inactive_window else 0,
                    "power": {
                        "internal": component.profiler.measurement.inactive.power.internal,
                        "switching": component.profiler.measurement.inactive.power.switching,
                        "leakage": component.profiler.measurement.inactive.power.leakage
                    }
                }
            }
        return dict

    def get_cell_dict(self, cell):
        dict = {
                "window": f"{cell.total_window}",
                "cycles": cell.total_window['clock_cycles'],
                "power": {
                    "internal": cell.profiler.measurement_set.actual.power.internal,
                    "switching": cell.profiler.measurement_set.actual.power.switching,
                    "leakage": cell.profiler.measurement_set.actual.power.leakage
                }
            }
        return dict


    def write_json(self,i,cells):
        data = {}
        for cell in cells:
            for component in cell.components.active:
                #if(component.name != "dpu"):
                #    continue
                #Write the component, active cycles of the component, and power of all three types in a json file in the same directory
                #as the testbench
                data[component.name] = self.get_component_dict(component)
            data[cell.cell_id] = self.get_cell_dict(cell)
        with open(f"{self.tb}/vcd/iter_{i}.json", "w") as file:
            json.dump(data, file, indent=2)


#            for component in cell.components.active:
#                component.profiler.set_avg_measurement_size(num_iterations)
#                for i in range(num_iterations):
#                    file_path = f"{self.tb}/vcd/iter_{i}.json"
#                    with open(file_path, 'r') as file:
#                        data = json.load(file)
#                    component_data = data.get(component.name, {})
#                    active_measurement = Measurement()
#                    inactive_measurement = Measurement()
#                    if 'active' in component_data:
#                        active_measurement.power.internal = component_data.get('active', {}).get('power', {}).get('internal', 0)
#                        active_measurement.power.switching = component_data.get('active', {}).get('power', {}).get('switching', 0)
#                        active_measurement.power.leakage = component_data.get('active', {}).get('power', {}).get('leakage', 0)
#                        active_measurement.power.total = active_measurement.power.internal + active_measurement.power.switching + active_measurement.power.leakage
#                        cycles = int(component_data.get('active', {}).get('cycles', 0))
#                        active_measurement.set_window({'start': 0, 'end': cycles * constants.CLOCK_PERIOD, 'clock_cycles': cycles})
#                        active_measurement.get_energy()
#
#                    if 'inactive' in component_data:
#                        inactive_measurement.power.internal = component_data.get('inactive', {}).get('power', {}).get('internal', 0)
#                        inactive_measurement.power.switching = component_data.get('inactive', {}).get('power', {}).get('switching', 0)
#                        inactive_measurement.power.leakage = component_data.get('inactive', {}).get('power', {}).get('leakage', 0)
#                        inactive_measurement.power.total = inactive_measurement.power.internal + inactive_measurement.power.switching + inactive_measurement.power.leakage
#                        cycles = int(component_data.get('inactive', {}).get('cycles', 0))
#                        inactive_measurement.set_window({'start': 0, 'end': cycles * constants.CLOCK_PERIOD, 'clock_cycles': cycles})
#                    component.profiler.add_avg_measurement(active_measurement, inactive_measurement, i)
#                    if(component.name == "noc"):
#                        component.profiler.print_avg_results(i)
