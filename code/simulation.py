import os
import subprocess
#from threading import Thread
#from time import sleep
#from joblib import Parallel, delayed

class Simulation():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.TB_DIR_FILE = None
        self.cells = {}

    def set_input(self,assembly):
        self.cells = assembly.cells

    def run_sim_active(self,component,window,id):
        start = str(window['start'])
        end = str(window['end'])
        suffix = 'active'
        print(component,start,end)
        os.system( "CELL=" + id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + start + 
                    " END_TIME=" + end + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
        os.system("CELL=" + id + 
                " COMPONENT=" + component + 
                " START_TIME=" + start + 
                " END_TIME=" + end + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )

    def run_sim_inactive(self,component,window,id):
        start = str(window['start'])
        end = str(window['end'])
        suffix = 'inactive'
        print(component,start,end)
        os.system( "CELL=" + id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + start + 
                    " END_TIME=" + end + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
        os.system("CELL=" + id + 
                " COMPONENT=" + component + 
                " START_TIME=" + start + 
                " END_TIME=" + end + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )

    def run_sim_total(self, window, id):
        start = str(window['start'])
        end = str(window['end'])
        component = 'total'
        suffix = ''
        print(component, start, end)
        args_vsim = ["vsim", "-64", "-c", "-do", "get_activity.do"]
        env_vsim = {"CELL": id, "COMPONENT": component, "START_TIME": start, "END_TIME": end, "SUFFIX": suffix}
        try:
            subprocess.run(args_vsim, env=env_vsim, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running vsim: {e}")
            return
        args_innovus = ["innovus", "-stylus", "-no_gui", "-files", "get_power.tcl"]
        env_innovus = {"CELL": id, "COMPONENT": component, "START_TIME": start, "END_TIME": end, "SUFFIX": suffix}
        try:
            subprocess.run(args_innovus, env=env_innovus, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running innovus: {e}")
            return
    

    def run_sim_cycle(self, window, id):
#        start = window['start']
#        end = window['end']
#        next = start + self.CLOCK_PERIOD
        start = window['end']
        end = start + 5 * self.CLOCK_PERIOD
        next = start + self.CLOCK_PERIOD
        component = 'all'
        suffix = ''
        while next <= end:
            os.system( "CELL=" + id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + str(start) + 
                    " END_TIME=" + str(next) + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
            os.system("CELL=" + id + 
                " COMPONENT=" + component + 
                " START_TIME=" + str(start) + 
                " END_TIME=" + str(next) + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )
            start = next
            next = start + self.CLOCK_PERIOD
            

    def run(self,tb):
        os.chdir(tb)
        for id in self.cells:
            total_window = self.cells[id]['total_window']
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
                    
