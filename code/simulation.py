import os

class Simulation():
    def __init__(self,tb,active_windows):
        self.TB_DIR_FILE = None
        self.component = None
        self.active_windows = active_windows
        self.run(tb)

    def run(self,tb):
        os.chdir(tb)
        for component in self.active_windows:
            for window in self.active_windows[component]:
                os.environ['COMPONENT'] = component
                os.environ['START_TIME'] = str(window['start'])
                os.environ['END_TIME'] = str(window['end'])
                os.system("vsim -64 -c -do get_activity.do")
                os.system("innovus -stylus -no_gui -files get_power.tcl")
