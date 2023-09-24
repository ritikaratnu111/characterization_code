import os
import logging
from loader import Loader
from characterize import Characterize
from helper_functions import VesylaOutput

class RunSimulations():
    def __init__(self):
        os.environ['FABRIC_PATH'] = '/home/ritika/silago/SiLagoNN/'
        self.TB_DIR_FILE = "../files/TB_DIR_FILE.txt"
        LOGFILE = "../log/output_test.log"
        os.remove(LOGFILE) if os.path.exists(LOGFILE) else None
        logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)

    def run_simulations(self):
        with open(self.TB_DIR_FILE) as fp:
            Lines = fp.readlines()
            for line in Lines:

                tb = line.split()[0]
                logging.info(f"Testbench: {tb}")
                print(f"Testbench: {tb}")
                VesylaOutput.update_clock_period(tb)

                loader = Loader(tb)
                loader.read()
                loader.process()
                loader.log()
                characterize = Characterize(tb,loader.cells)
#                characterize.run_simulation_per_cycle()
#                characterize.run_randomized_simulation(1)
#                characterize.get_per_cycle_power()
                characterize.get_active_AEC_power()
                characterize.get_inactive_AEC_power()
                characterize.get_active_AEC_energy()
                characterize.get_inactive_AEC_energy()
                characterize.get_remaining_power()
                characterize.get_total_power()
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
    job.run_simulations()
    return

if __name__ == "__main__":
    main()
