import sys,os
import logging
import json
from helper_functions import VesylaOutput
from loader import Loader
from simulator import Simulator
from power_tracker import SimulationPowerTracker
from cross_algorithm_predictor import Predictor

logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

class RunSimulations():
    def __init__(self,predict_start,predict_end, test_start, test_end):
        self.predict_start = predict_start
        self.predict_end = predict_end
        self.test_start = test_start
        self.test_end = test_end
        self.testbenches = {}
        self.algorithms = {}
        self.LOGFILE = ""
        self.FABRIC_PATH = ""
        self.logger = None
        logging.basicConfig(level=logging.DEBUG)

    def set_logfile(self,path):
        self.LOGFILE = f"{path}/char_test.log"
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

    def get_algorithms(self):
        try:
            algorithms_path = "../input_files/algorithms.json"
            
            with open(algorithms_path) as file:
                self.algorithms = json.load(file)
        except FileNotFoundError:
            print(f"Testbench file '{tb_file_path}' not found.")
        except Exception as e:
            print(f"Error loading testbenches: {e}") 

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
                # Log testbench info
                self.set_logfile(info["path"])
                self.logger.info(f"Testbench: {name}")
                self.logger.info(f"About: {info['about']}")
                # Update clock period to the netlist period
                VesylaOutput.update_clock_period(tb)
                # Objects for characterization
                loader = Loader(tb,self.logger)
                simulator = Simulator(tb, self.predict_start, self.predict_end)
                power_tracker = SimulationPowerTracker(tb, self.predict_start, self.predict_end)

                # Load the instructions
                loader.read()
                loader.process()
                cells = loader.cells
                # Run post layout simulations
#                simulator.run_randomized_simulations(cells)
#                simulator.run_simulation_per_cycle()
#                simulator.get_per_cycle_measurement()

                # Get power measurements
                power_tracker.get_measurements(cells)  

                # Predict the measurments from the simulations of this testbench
#                comparator = Comparator(characterize, predictor)
#                comparator.log()
#                comparator.print()

    def get_prediction_and_error(self):
        predictor = Predictor(self.predict_start,self.predict_end, self.test_start, self.test_end)
        avg_algorithms = self.algorithms['train']['blas']["l1"]
        predictor.average_algorithms(avg_algorithms)
        test_algorithms = self.algorithms['test']['blas']["l1"]
        predictor.test_algorithms(test_algorithms)
#        predictor.test('VEC_SUB', '/media/storage1/ritika/SiLagoNN/tb/char/blas/l1_vec_ops/vec_sub/top/')
#        predictor.test('VEC_DOT', '/media/storage1/ritika/SiLagoNN/tb/char/blas/l1_vec_ops/vec_dot/top/')
#        predictor.test('VEC_SCALE', '/media/storage1/ritika/SiLagoNN/tb/char/blas/l1_vec_ops/vec_scale/top/')
#        predictor.test('VEC_AXPY', '/media/storage1/ritika/SiLagoNN/tb/char/blas/l1_vec_ops/axpy/top/')

def main():
    predict_start = int(sys.argv[1])
    predict_end = int(sys.argv[2])
    test_start = int(sys.argv[3])
    test_end = int(sys.argv[4])
    job = RunSimulations(predict_start,predict_end, test_start, test_end)
    job.set_fabric_path()
    job.get_testbenches()
    job.get_algorithms()
    job.run_simulations()
    job.get_prediction_and_error()
    return

if __name__ == "__main__":
    main()
