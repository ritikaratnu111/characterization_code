import os
import logging
import json
from loader import Loader
from characterize import Characterize
from helper_functions import VesylaOutput
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

class RunSimulations():
    def __init__(self):
        self.testbenches = {}
        self.LOGFILE = ""
        self.FABRIC_PATH = ""
        self.logger = None
        logging.basicConfig(level=logging.DEBUG)

    def set_logfile(self,path):
        self.LOGFILE = f"{path}/char_energy.log"
        print(f"Logfile: {self.LOGFILE}")
        try:
              # Use context manager for file operations
            with open(self.LOGFILE, 'w'): pass
            self.logger = logging.getLogger()
            handler = logging.FileHandler(self.LOGFILE)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        except Exception as e:
            print(f"Failed to set logfile: {e}")
            self.logger = None

    def set_fabric_path(self):
        self.FABRIC_PATH = '/home/ritika/silago/SiLagoNN/'
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        try:
            tb_file_path = "../input_files/testbenches.json"
            with open(tb_file_path) as file:
                self.testbenches = json.load(file)
        except FileNotFoundError:
            print(f"Testbench file '{tb_file_path}' not found.")
        except Exception as e:
            print(f"Error loading testbenches: {e}")

    def run_simulations(self):
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                self.set_logfile(info["path"])
                self.logger.info(f"Testbench: {name}")
                self.logger.info(f"About: {info['about']}")
                tb = info["path"]
                VesylaOutput.update_clock_period(tb)
                loader = Loader(tb,self.logger)
                loader.read()
                loader.process()
                start = 0
                end = 1
                vcd_dir = f"./vcd_{start}_{end}/"
                characterize = Characterize(tb, vcd_dir, loader.cells)
#                characterize.generate_randomized_mem_init_files(start,end)
                characterize.run_randomized_simulation(start,end)
#                characterize.run_simulation_per_cycle()
#                characterize.get_per_cycle_measurement()
                #characterize.get_AEC_measurements_from_per_cycle()
#                characterize.get_cell_measurements(start,end)
                characterize.get_average(start,end)
#                loader.log_window()
                #loader.log_AEC_measurements_from_per_cycle()
                #loader.log_cell_measurements()
                #loader.log_AEC_per_cycle_measurement()
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
    job.set_fabric_path()
    job.get_testbenches()
    job.run_simulations()
    return

if __name__ == "__main__":
    main()
