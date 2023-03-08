import os
#from threading import Thread
#from time import sleep
from joblib import Parallel, delayed

class Simulation():
    def __init__(self,tb,active_windows):
        self.TB_DIR_FILE = None
        self.component = None
        self.active_windows = active_windows
        self.run(tb)

    def run_sim(self,component,start,end):
        print(component,start,end)
#        os.environ['COMPONENT'] = component
#        os.environ['START_TIME'] = start
#        os.environ['END_TIME'] = end
        os.system("COMPONENT=" + component + " START_TIME=" + start + " END_TIME=" + end + " vsim -64 -c -do get_activity.do")
        os.system("COMPONENT=" + component + " START_TIME=" + start + " END_TIME=" + end + " innovus -stylus -no_gui -files get_power.tcl")


    def run(self,tb):
        os.chdir(tb)
        for component in self.active_windows:
#            threads = []
#            for window in self.active_windows[component]:
#                threads.append(Thread(target=self.run_sim, args=(component, str(window['start']), str(window['end']))))
            Parallel(n_jobs=4)(delayed(self.run_sim)(component, str(window['start']), str(window['end'])) for window in self.active_windows[component])
#            threads[-1].start()
#            for thread in threads:
#                thread.join()
