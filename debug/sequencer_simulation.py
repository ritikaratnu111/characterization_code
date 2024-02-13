import os
import subprocess
#from threading import Thread
#from time import sleep
#from joblib import Parallel, delayed
ACTIVITY_FILE = '/home/ritika/silago/characterization_code/code/get_activity.do'
POWER_FILE = '/home/ritika/silago/characterization_code/code/get_power.tcl'

class Simulation():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.TB_DIR_FILE = "../input_files/TB_DIR_FILE.txt"
        os.environ['FABRIC_PATH'] = '/media/storage1/ritika/SiLagoNN/'
        os.environ['VCD_DIR'] ='./vcd/'

    def run_sim_cycle(self):
        id = '0'
        start = 366
        end = 534
#        os.system(
#                " START_TIME=" + str(start) + 
#                " END_TIME=" + str(end) + 
#                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
#                " vsim -64 -c -do " + ACTIVITY_FILE
#                )
        os.system(
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(end) + 
                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
                " innovus -stylus -no_gui -files " + POWER_FILE
                )

    def run(self):
        with open(self.TB_DIR_FILE) as fp:
            Lines = fp.readlines()
            for line in Lines:
                tb = line.strip()
                os.chdir(tb)
                self.run_sim_cycle()

simulation = Simulation()
simulation.run()

#            active_components = self.cells[id]["active_components"]
#            self.run_sim_total(total_window, id)
#            for component in active_components:
#                active_windows = self.cells[id]['component_active_cycles'][component]
#                inactive_windows = self.cells[id]['component_inactive_cycles'][component]
#                for window in active_windows:
#                    self.run_sim_active(component, window, id)
#                for window in inactive_windows:
#                    self.run_sim_inactive(component, window, id)
                    
