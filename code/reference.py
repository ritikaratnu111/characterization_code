from helper_functions import fabric, tbgen
from helper_functions import VesylaOutput
from loader import Loader
from simulator import Simulator
from power_tracker import PowerParser
from power import Power
import json
import os
import logging

SILAGO_DB_PATH = '/media/storage1/ritika/characterization_code/db/silago_db.json'    
JSON_FILE_PATH = '/media/storage1/ritika/characterization_code/json_files/'    

class PostLayoutEnergyCalculator():

    def __init__(self, start, end):
        self.data = {}
        self.logger = None
        self.start = start
        self.end = end
        logging.basicConfig(level=logging.DEBUG)
        self.averager = Averager(start, end)

    def get_fabric(self):
        self.FABRIC_PATH = fabric.set_path()
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        self.testbenches = tbgen.set_testbenches("blas")

    def update_logger(self, path, name, about):
        LOGFILE = f"{path}/reference.log"
        try:
            with open(LOGFILE, 'w'): pass
            self.logger = logging.getLogger()
            handler = logging.FileHandler(LOGFILE)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.info(f"Testbench: {name}")
            self.logger.info(f"About: {about}")
        except Exception as e:
            print(f"Failed to set logfile: {e}")
            self.logger = None

    def get_cells(self, tb):
        loader = Loader(tb,self.logger)
        loader.read()
        loader.process()
        cells = loader.cells
        return cells

    def simulate(self, tb, cells):
        simulator = Simulator(tb, self.start, self.end)
        simulator.run_randomized_simulations(cells)
#        simulator.run_simulation_per_cycle()
#        simulator.get_per_cycle_measurement()

    def get_power(self, tb, cells):
        power_parser = PowerParser(tb, self.start, self.end)
        power_parser.get_measurements(cells)  
        power_parser.write_json(cells)  

    def run_randomised_simulations(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                VesylaOutput.update_clock_period(tb)
                cells = self.get_cells(tb)
                self.simulate(tb, cells)
                self.get_power(tb, cells)

    def get_energy(self, cells):
        for i in range(self.start,self.end):
            self.reader = InnovusPowerParser()
            pwr_file=f"{self.tb}/vcd/iter_{i}.vcd.pwr"
            json_file=f"{self.tb}/vcd/iter_{i}.json"

            if not os.path.exists(pwr_file):
                self.run_randomized_simulations()

            elif os.path.exists(pwr_file) and not os.path.exists(json_file):
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

    def get_post_layout_energy(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                cells = self.get_cells(tb)
                self.get_energy(cells)
                self.write_reference(tb)
                    

    def get_average(self):
        self.averager.across_tb(self.testbenches)

    def write_reference(self, tb):
        with open(f"{tb}/reference.json", "w") as file:
            json.dump(self.data, file, indent=2)
