import os
import logging
import json
from loader import Loader
from characterize import Characterize
from helper_functions import VesylaOutput

class RunSimulations():
    def __init__(self):
        self.testbenches = {}
        self.LOGFILE = ""
        self.FABRIC_PATH = ""
        self.logger = None

    def set_logfile(self):
        self.LOGFILE = "../log/output.log"
        if os.path.exists(self.LOGFILE):
            os.remove(self.LOGFILE)
        else:
            None
        logging.basicConfig(filename=self.LOGFILE, level=logging.DEBUG)
        self.logger = logging.getLogger()

    def set_fabric_path(self):
        self.FABRIC_PATH = '/home/ritika/silago/SiLagoNN/'
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        TB_FILE_PATH = "../input_files/testbenches.json"
        self.testbenches = json.load(open(TB_FILE_PATH))

    def run_simulations(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                self.logger.info(f"Testbench: {name}")
                self.logger.info(f"About: {info['about']}")
                tb = info["path"]
                VesylaOutput.update_clock_period(tb)
                loader = Loader(tb,self.logger)
                loader.read()
                loader.process()
                loader.log()
                characterize = Characterize(tb,loader.cells)
                characterize.run_simulation_per_cycle()
#                characterize.run_randomized_simulation(1)
#                characterize.get_per_cycle_measurement()
#                characterize.get_AEC_measurement()
#                characterize.get_remaining_measurement()
#                characterize.get_total_measurement()
#                characterize.get_diff_measurement()
#                characterize.write_db()
#                characterize.log()
#
#                predictor = Predictor(tb,assembly)
#                predictor.read_db()
#                predictor.get_active_component_active_energy()
#                predictor.get_active_component_inactive_energy()
#                predictor.get_inactive_component_energy()
#                predictor.get_total_energy()
#                predictor.log()
#
#                comparator = Comparator(characterize, predictor)
#                comparator.log()
#                comparator.print()
            
def main():
    job = RunSimulations()
    job.set_logfile()
    job.set_fabric_path()
    job.get_testbenches()
    job.run_simulations()
    return

if __name__ == "__main__":
    main()
