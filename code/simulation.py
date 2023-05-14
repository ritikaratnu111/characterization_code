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
        self.TB_DIR_FILE = None
        self.cells = {}

    def set_input(self,assembly):
        self.cells = assembly.cells

    # def run_sim_active(self,component,window,id):
    #     start = str(window['start'])
    #     end = str(window['end'])
    #     suffix = 'active'
    #     print(component,start,end)
    #     os.system( "CELL=" + id + 
    #                 " COMPONENT=" + component + 
    #                 " START_TIME=" + start + 
    #                 " END_TIME=" + end + 
    #                 " SUFFIX=" + suffix + 
    #                 " vsim -64 -c -do get_activity.do"
    #                 )
    #     os.system("CELL=" + id + 
    #             " COMPONENT=" + component + 
    #             " START_TIME=" + start + 
    #             " END_TIME=" + end + 
    #             " SUFFIX=" + suffix + 
    #             " innovus -stylus -no_gui -files get_power.tcl"
    #             )

    # def run_sim_inactive(self,component,window,id):
    #     start = str(window['start'])
    #     end = str(window['end'])
    #     suffix = 'inactive'
    #     print(component,start,end)
    #     os.system( "CELL=" + id + 
    #                 " COMPONENT=" + component + 
    #                 " START_TIME=" + start + 
    #                 " END_TIME=" + end + 
    #                 " SUFFIX=" + suffix + 
    #                 " vsim -64 -c -do " + ACTIVITY_FILE
    #                 )
    #     os.system("CELL=" + id + 
    #             " COMPONENT=" + component + 
    #             " START_TIME=" + start + 
    #             " END_TIME=" + end + 
    #             " SUFFIX=" + suffix + 
    #             " innovus -stylus -no_gui -files " + POWER_FILE
    #             )

    def run_sim_total(self, window, id):
        start = str(window['start'])
        end = window['end'] + 5 * self.CLOCK_PERIOD
        os.system(
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(end) + 
                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
                " CELL_ID=" + id +
                " PER_CYCLE_FLAG=false" +
                " vsim -64 -c -do " + ACTIVITY_FILE
                )
        os.system(
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(end) + 
                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
                " CELL_ID=" + id + 
                " PER_CYCLE_FLAG=false" +
                " innovus -stylus -no_gui -files " + POWER_FILE
                )

    def run_sim_cycle(self, window, id):
        start = window['start']
        end = window['end'] + 5 * self.CLOCK_PERIOD
        os.system(
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(end) + 
                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
                " CELL_ID=" + id + 
                " PER_CYCLE_FLAG=true" +
                " vsim -64 -c -do " + ACTIVITY_FILE
                )
        os.system(
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(end) + 
                " CLOCK_PERIOD=" + str(self.CLOCK_PERIOD) + 
                " CELL_ID=" + id + 
                " PER_CYCLE_FLAG=true" +
                " innovus -stylus -no_gui -files " + POWER_FILE
                )

    def run(self,tb):
        os.chdir(tb)
        os.makedirs("vcd", exist_ok=True)

        for id in self.cells:
            total_window = self.cells[id]['total_window']
            self.run_sim_total(total_window,id)
            self.run_sim_cycle(total_window,id)
#            active_components = self.cells[id]["active_components"]
#            self.run_sim_total(total_window, id)
#            for component in active_components:
#                active_windows = self.cells[id]['component_active_cycles'][component]
#                inactive_windows = self.cells[id]['component_inactive_cycles'][component]
#                for window in active_windows:
#                    self.run_sim_active(component, window, id)
#                for window in inactive_windows:
#                    self.run_sim_inactive(component, window, id)
                    
