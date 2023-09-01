import os
import logging
from assembly import Assembly
from characterize import Characterize
from energy import EnergyCalculator
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

                assembly = Assembly(tb)
                assembly.read()
                assembly.set_active_components()
                assembly.set_component_active_cycles()
                assembly.set_component_inactive_cycles()
                assembly.log()
#
                characterize = Characterize(tb,assembly)
                characterize.run_randomized_simulation(3)
#                characterize.run_simulation_per_component()
#                characterize.get_per_cycle_power()
#                characterize.get_active_component_active_energy()
#                characterize.get_active_component_inactive_energy()
#                characterize.get_inactive_component_energy()
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
