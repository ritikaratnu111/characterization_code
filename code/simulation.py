import os
#from threading import Thread
#from time import sleep
#from joblib import Parallel, delayed

class Simulation():
    def __init__(self):
        self.TB_DIR_FILE = None
        self.cells = {}

    def set_input(self,assembly):
        self.cells = assembly.cells

    def run_sim_active(self,component,window):
        start = str(window['start'])
        end = str(window['end'])
        suffix = 'active'
        print(component,start,end)
        os.system( "CELL=" + self.cell_id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + start + 
                    " END_TIME=" + end + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
        os.system("CELL=" + self.cell_id + 
                " COMPONENT=" + component + 
                " START_TIME=" + start + 
                " END_TIME=" + end + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )

    def run_sim_inactive(self,component,window):
        start = str(window['start'])
        end = str(window['end'])
        suffix = 'inactive'
        print(component,start,end)
        os.system( "CELL=" + self.cell_id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + start + 
                    " END_TIME=" + end + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
        os.system("CELL=" + self.cell_id + 
                " COMPONENT=" + component + 
                " START_TIME=" + start + 
                " END_TIME=" + end + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )

    def run_sim_total(self,window):
        start = str(window['start'])
        end = str(window['end'])
        component = 'total'
        suffix = ''
        print(component,start,end)
        os.system( "CELL=" + self.cell_id + 
                    " COMPONENT=" + component + 
                    " START_TIME=" + start + 
                    " END_TIME=" + end + 
                    " SUFFIX=" + suffix + 
                    " vsim -64 -c -do get_activity.do"
                    )
        os.system("CELL=" + self.cell_id + 
                " COMPONENT=" + component + 
                " START_TIME=" + start + 
                " END_TIME=" + end + 
                " SUFFIX=" + suffix + 
                " innovus -stylus -no_gui -files get_power.tcl"
                )

    def run(self,tb):
        os.chdir(tb)
        for id in self.cells:
            self.run_sim_total(self.cells[id]['total_window'])
            for component in self.cells[id]["active_components"]:
                for window in self.active_windows[component]:
                    self.run_sim_active(component, window)
                for window in self.inactive_windows[component]:
                    self.run_sim_inactive(component, window)
                    
