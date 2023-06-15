import os
import logging
from assembly import Assembly
from simulation import Simulation
from energy import EnergyCalculator

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
                energy = EnergyCalculator()
                # Set assembly
                assembly.set_assembly_file(tb)
                assembly.set_model()
                # Log the cell ids of assembly cells dictionary in a nice format.
                logging.info('Cell ids: %s', assembly.cells.keys())
                # Log the active components line by line for all cells in assembly self.cells dictionary in a nice format.
                for id in assembly.cells:
                    for instr in assembly.cells[id]['instr_list']:
                        logging.info('%s %s ',instr['name'],instr['start_time'])
                    logging.info('Active window for cell %s: start: %s end: %s', id, 
                                                            assembly.cells[id]['total_window']['start'], 
                                                            assembly.cells[id]['total_window']['end'])
                    logging.info('Active components for cell %s:', id)
                    for component in assembly.cells[id]['active_components']:
                        logging.info('     %s: %s', component, assembly.cells[id]['active_components'][component])
                        logging.info('Active window       %s', assembly.cells[id]['component_active_cycles'][component])
                        logging.info('Inactive window     %s', assembly.cells[id]['component_inactive_cycles'][component])
                # Run simulations
#                simulation.set_input(assembly)
#                simulation.run(tb)
                # Set energy
                energy.set_assembly_file(tb)
                energy.set_input(assembly)
                energy.set_model()
                energy.set_per_cycle_power()
                # Set active component active window internal and switching energy using per cycle power reports
                energy.set_active_component_active_window_dynamic_energy()
                print("set_active_component_active_window_dynamic_energy() complete!")
                # Set active component inactive window internal and switching energy using per cycle power reports
                energy.set_active_component_inactive_window_dynamic_energy()
                print("set_active_component_inactive_window_dynamic_energy() complete!")
                # Set active component leakage energy using per cycle power reports
                energy.set_active_component_static_energy()
                print("set_active_component_static_energy() complete!")
                # Set inactive component energy using total power report
                energy.set_inactive_component_energy()
                print("set_inactive_component_energy() complete!")
                # Set model energy using the above active and inactive energy
                energy.set_model_energy()
                # Set reference energy using the total power report
                energy.set_reference_energy()
                # Set energy error between reference energy and model energy
                energy.set_energy_error()
               # Log the active components line by line for all cells in assembly self.cells dictionary in a nice format.
                for id in assembly.cells:
                    logging.info('Active components for cell %s:', id)
                    for component in assembly.cells[id]['active_components']:
                        logging.info('     %s: %s', component, assembly.cells[id]['active_components'][component])
                        for duration in energy.cells[id]['per_cycle_power']['active_components'][component]['internal']:
                            logging.info('     Duration %s: internal: %s, switching: %s, leakage: %s ', duration, 
                                               energy.cells[id]['per_cycle_power']['active_components'][component]['internal'][duration],
                                               energy.cells[id]['per_cycle_power']['active_components'][component]['switching'][duration],
                                               energy.cells[id]['per_cycle_power']['active_components'][component]['leakage'][duration])
                    logging.info('     Model energy: internal: %s, switching: %s, leakage: %s ', 
                                                    energy.cells[id]['energy']['model']['internal'],
                                                    energy.cells[id]['energy']['model']['switching'],
                                                    energy.cells[id]['energy']['model']['leakage'])
                    logging.info('     Reference energy: internal: %s, switching: %s, leakage: %s ', 
                                                    energy.cells[id]['energy']['reference']['internal'],
                                                    energy.cells[id]['energy']['reference']['switching'],
                                                    energy.cells[id]['energy']['reference']['leakage'])
                    logging.info('     Energy error: internal: %s, switching: %s, leakage: %s ', 
                                                    energy.cells[id]['energy']['error']['internal'],
                                                    energy.cells[id]['energy']['error']['switching'],
                                                    energy.cells[id]['energy']['error']['leakage'])
job = RunSimulations()
job.run_simulations()
