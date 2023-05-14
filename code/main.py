import os
import logging
from assembly import Assembly
from simulation import Simulation
from energy_calculator import EnergyCalculator

class RunSimulations():
    def __init__(self):
        self.TB_DIR_FILE = None
        self.set_fabric_path()
        self.set_tb_dir_file()
        logfile = "output.log"
        os.remove(logfile) if os.path.exists(logfile) else None
        logging.basicConfig(filename=logfile, level=logging.DEBUG)

    def set_fabric_path(self):
        os.environ['FABRIC_PATH'] = '/home/ritika/silago/SiLagoNN/'

    def set_tb_dir_file(self):
        self.TB_DIR_FILE = "../input_files/TB_DIR_FILE.txt"
        os.environ['VCD_DIR'] ='./vcd/'

    def run_simulations(self):
        with open(self.TB_DIR_FILE) as fp:
            Lines = fp.readlines()
            for line in Lines:
                tb = line.strip()
                # Create classes
                assembly = Assembly()
                simulation = Simulation()
                energy_calculator = EnergyCalculator()
                # Set assembly
                assembly.set_assembly_file(tb)
                assembly.set_model()
                # Log the cell ids of assembly cells dictionary in a nice format.
                logging.info('Cell ids: %s', assembly.cells.keys())
                # Log the active components line by line for all cells in assembly self.cells dictionary in a nice format.
                for id in assembly.cells:
                    logging.info('Active components for cell %s:', id)
                    for component in assembly.cells[id]['active_components']:
                        logging.info('     %s: %s', component, assembly.cells[id]['active_components'][component])
                        logging.info('     %s', assembly.cells[id]['component_active_cycles'][component])
                # Run simulations
                simulation.set_input(assembly)
                simulation.run(tb)
                # Set energy
                energy_calculator.set_assembly_file(tb)
                energy_calculator.set_input(assembly)
                energy_calculator.set_model()
                energy_calculator.set_power()
#                # Log the active components line by line for all cells in assembly self.cells dictionary in a nice format.
#                for id in assembly.cells:
#                    logging.info('Active components for cell %s:', id)
#                    for component in assembly.cells[id]['active_components']:
#                        logging.info('     %s: %s', component, assembly.cells[id]['active_components'][component])
#                        for duration in energy_calculator.cells[id]['per_cycle_power']['active_components'][component]['internal']:
#                            logging.info('     Duration %s: internal: %s, switching: %s, leakage: %s ', duration, 
#                                               energy_calculator.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration],
#                                               energy_calculator.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration],
#                                               energy_calculator.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration])
#                energy_calculator.set_energy()
#                energy_calculator.print_energy()
#                energy_calculator.write_reports()

job = RunSimulations()
job.run_simulations()
