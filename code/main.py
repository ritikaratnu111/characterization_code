import os
from assembly import Assembly
from simulation import Simulation
from energy_calculator import EnergyCalculator

class RunSimulations():
    def __init__(self):
        self.TB_DIR_FILE = None
        self.set_fabric_path()
        self.set_tb_dir_file()
    
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
                assembly = Assembly()
                simulation = Simulation()
                energy_calculator = EnergyCalculator()
                assembly.set_assembly_file(tb)
                assembly.set_model()
#                simulation.set_input(assembly)
#                simulation.run(tb)
                energy_calculator.set_assembly_file(tb)
                energy_calculator.set_input(assembly)
                energy_calculator.set_model()
                energy_calculator.set_power()
#                energy_calculator.set_energy()
#                energy_calculator.print_energy()
#                energy_calculator.write_reports()

job = RunSimulations()
job.run_simulations()
