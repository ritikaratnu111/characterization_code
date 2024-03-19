from helper_functions import fabric, tbgen
from helper_functions import VesylaOutput
from create_average import Averager
from loader import Loader
from simulator import Simulator
from power_tracker import PowerParser
import logging
import os
import json

DB_PATH = '/media/storage1/ritika/characterization_code/db/'    

class DbGenerator():
    def __init__(self, start, end):
        self.testbenches = {}
        self.FABRIC_PATH = ""
        self.logger = None
        self.averager = Averager(start, end)
        self.start = start
        self.end = end
        logging.basicConfig(level=logging.DEBUG)

    def get_fabric(self):
        self.FABRIC_PATH = fabric.set_path()
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        self.testbenches = tbgen.set_testbenches("db")

    def update_logger(self, path, name, about):
        LOGFILE = f"{path}/dbgen.log"
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

    def predict(self, tb, cells):
        predictor = Predictor(tb, self.start, self.end)
        predictor.get_prediction()
        predictor.write_json()
        predictor.get_running_error()
        predictor.plot_running_average_error()

    def run_randomised_simulations(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                VesylaOutput.update_clock_period(tb)
                cells = self.get_cells(tb)
                self.simulate(tb, cells)
                self.get_power(tb, cells)

    def get_average(self):
        self.averager.across_tb(self.testbenches)

    def write_db(self):
        with open(f"{DB_PATH}/silago_db.json", "w") as file:
            json.dump(self.averager.data, file, indent=2)
        
