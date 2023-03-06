import os
from assembly import Assembly
from simulation import Simulation

class RunSimulations():
    def __init__(self):
        self.TB_DIR_FILE = None
#        self.set_fabric_path()
        self.set_fabric_path()
        self.set_tb_dir_file()
        self.run_simulations()
    
    def set_fabric_path(self):
        os.environ['FABRIC_PATH'] ='/home/ritika/silago/SiLagoNN/'

    def set_tb_dir_file(self):
        self.TB_DIR_FILE = "../input_files/TB_DIR_FILE.txt"
        os.environ['VCD_DIR'] ='./vcd/'

    def run_simulations(self):
        with open(self.TB_DIR_FILE) as fp:
            Lines = fp.readlines()
            for line in Lines:
                tb = line.strip()
                assembly = Assembly(tb)
                os.environ['SUFFIX'] ='active'
                Simulation(tb,assembly.active_windows)       #SE,IE component_active.vcd for each component, SE,IE,LE inactive_components and LE of inactive components for 'total'
                os.environ['SUFFIX'] ='inactive'
                Simulation(tb,assembly.inactive_window)     #SE,IE component_inactive.vcd
#            EnergyEstimator(tb,assembly.active_components,assembly.active_window,assembly.inactive_window,assembly.all_cycles)

RunSimulations()
