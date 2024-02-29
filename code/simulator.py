import os
import logging
import random
import constants
from openpyxl import Workbook
from simulation import Simulation
from innovus_reader import InnovusPowerParser
from measurement import Measurement

class Simulator():
	
    def __init__(self, tb, start, end):     
        self.tb = tb
        self.vcd_dir = f"./vcd/"
        os.environ['VCD_DIR'] = self.vcd_dir
        os.chdir(tb)
        os.makedirs(self.vcd_dir, exist_ok=True)
        self.start = start
        self.end = end
        self.total_window = {   'start': 1000000,
                                'end':0,
                                'clock_cycles': 0
                                }
        


    def run_simulation(self, window, i, uid):
        start = window['start']
        end = window['end']
        Simulation.trigger_vsim(i, start, end, False, uid)
        Simulation.trigger_innovus(i, start, end, False)
        Simulation.remove_file(f"{self.tb}/{self.vcd_dir}/iter_{i}.vcd")
        Simulation.remove_file(f"{self.tb}/testbench_rtl_{uid}.vhd")
        Simulation.remove_dir(f"{self.tb}/work_{uid}")

    def generate_randomized_mem_init_files(self):
        Simulation.generate_randomized_mem_init_files(start, end)

    def get_total_window(self,cells):
        for cell in cells:
            if (int(cell.total_window['start']) < self.total_window['start']) :
                self.total_window['start'] = cell.total_window['start']
            if (int(cell.total_window['end']) > self.total_window['end']):
                self.total_window['end'] = cell.total_window['end']

        self.total_window['clock_cycles'] = (self.total_window['end'] - self.total_window['start']) / constants.CLOCK_PERIOD
        print(self.total_window)

    def run_randomized_simulations(self, cells):

        self.get_total_window(cells)

        for i in range(self.start, self.end):
            pwr_file=f"{self.tb}/vcd/iter_{i}.vcd.pwr"

            if os.path.exists(pwr_file):
                continue
            else:
                Simulation.generate_randomized_mem_init_files(i)
                uid = Simulation.update_mem_init_file(self.tb, i)
                print("Running randomized simulation number ", i, "unique_id: ", uid)
                self.run_simulation(self.total_window, i, uid)
    
    def run_simulation_per_cycle(self, cells, i):
        uid = Simulation.update_mem_init_file(self.tb, 0)
        window = cells[0].total_window
        factor = int((window['end'] - window['start']) / 8)
        start = window['start'] + i * factor
        end = min(start + factor, window['end'])
        print(f"Window start: {window['start']}, Factor: {factor}, i: {i}")
        print("Capturing cycles" ,start,end)
        Simulation.trigger_vsim(0, start, end,  True, uid)
        Simulation.trigger_innovus(0, start, end,  True)

#
#    def get_AEC_measurements_from_per_cycle(self):
#        print("Getting per cycle component measurement")
#        for cell in self.cells:
#            logging.info("Setting component measurement from per_cycle for %s", cell.drra_tile)
#            for component in cell.components.active:
#                # if(component.name != "noc"):
#                #     continue
#                print(component.name)
#                logging.info("Setting active measurement from per_cycle for %s", component.name)
#                component.profiler.set_active_measurement_from_per_cycle()
#                component.profiler.set_inactive_measurement_from_per_cycle()
#                component.profiler.set_total_measurement_from_per_cycle(cell.total_window)
#                component.profiler.set_total_measurement_from_iter_file(self.reader, component.signals, 0, cell.total_window)
#
