import sys,os
import logging
import json
from helper_functions import VesylaOutput
from loader import Loader
from simulator import Simulator
from power_tracker import SimulationPowerTracker
from predictor import Predictor
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
        self.FABRIC_PATH = '/media/storage1/ritika/SiLagoNN/'
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
                # Get info
                tb = info["path"]
                start = int(sys.argv[1])
                end = int(sys.argv[2])
                # Log testbench info
                self.set_logfile(info["path"])
                self.logger.info(f"Testbench: {name}")
                self.logger.info(f"About: {info['about']}")
                # Update clock period to the netlist period
                VesylaOutput.update_clock_period(tb)
                # Objects for characterization
                loader = Loader(tb,self.logger)
                simulator = Simulator(tb, start, end)
                power_tracker = SimulationPowerTracker(tb, start, end)
                predictor = Predictor(tb, start, end)

                # Load the instructions
                loader.read()
                loader.process()
                cells = loader.cells
                # Run post layout simulations
                simulator.run_randomized_simulations(cells)
#                simulator.run_simulation_per_cycle()
#                simulator.get_per_cycle_measurement()

                # Get power measurements
                power_tracker.get_measurements(cells)  

                # Predict the measurments from the simulations of this testbench
                predictor.get_prediction()
                predictor.write_json()
                predictor.get_running_error()
                predictor.plot_running_average_error()
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
