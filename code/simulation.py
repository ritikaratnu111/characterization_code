import os
#from threading import Thread
#from time import sleep
from joblib import Parallel, delayed

class Simulation():
    def __init__(self,tb,active_components,active_windows,inactive_windows):
        self.TB_DIR_FILE = None
        self.component = None
        self.active_components = active_components
        self.active_windows = active_windows
        self.inactive_windows = inactive_windows
        self.run(tb)

    def run_sim(self,component,start,end,suffix):
        print(component,start,end)
        os.system("COMPONENT=" + component + " START_TIME=" + start + " END_TIME=" + end + " SUFFIX=" + suffix + " vsim -64 -c -do get_activity.do")
        os.system("COMPONENT=" + component + " START_TIME=" + start + " END_TIME=" + end + " SUFFIX=" + suffix + " innovus -stylus -no_gui -files get_power.tcl")

    def run(self,tb):
        os.chdir(tb)
        for component in self.active_components:
            for window in self.active_windows[component]:
                self.run_sim_active_windows(component, str(window['start']), str(window['end']), 'active')
            for window in self.inactive_windows[component]:
                self.run_sim_inactive_windows(component, str(window['start']), str(window['end']), 'inactive')
#            Parallel(n_jobs=4)(delayed(self.run_sim)(component, str(window['start']), str(window['end'])) for window in self.active_windows[component])
