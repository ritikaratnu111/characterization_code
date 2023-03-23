import os
from assembly import Assembly
from simulation import Simulation
from energy_calculator import EnergyCalculator
from multiprocessing import Pool, cpu_count

class RunSimulations():
    def __init__(self):
        self.TB_DIR_FILE = None
#        self.set_fabric_path()
        self.set_fabric_path()
        self.set_tb_dir_file()
#        self.run_simulations()
    
    def set_fabric_path(self):
        os.environ['FABRIC_PATH'] ='/home/ritika/silago/SiLagoNN/'

    def set_tb_dir_file(self):
        self.TB_DIR_FILE = "../input_files/TB_DIR_FILE.txt"
        os.environ['VCD_DIR'] ='./vcd/'

    def simulate(self,tb,inactive_windows):
        Simulation(tb,inactive_windows)

    def run_simulations(self):
        with open(self.TB_DIR_FILE) as fp:
            Lines = fp.readlines()
            for line in Lines:
                tb = line.strip()
                assembly = Assembly(tb)
                Simulation(tb,assembly.active_components,assembly.active_windows,assembly.inactive_windows)       #SE,IE component_active.vcd for each component, SE,IE,LE inactive_components and LE of inactive components for 'total'
            EnergyCalculator(tb,assembly.active_components,assembly.active_windows,assembly.inactive_windows,assembly.total_assembly_cycles)

job = RunSimulations()
job.run_simulations()
#p = Pool(processes=cpu_count())
#p.map(job.run_simulations(), range(cpu_count()))
