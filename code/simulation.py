import os

class Simulate():
    def __init__(self,tb):
        self.TB_DIR_FILE = None
        self.run(tb)

    def run(self,tb):
                os.chdir(tb)
                os.system("export FABRIC_PATH = ")
                os.system("export START_TIME = ")
                os.sytem("export END_TIME= ")
                os.system("vsim -64 -c -do get_activity.do")
                os.system("innovus -stylus -no_gui -files get_power.tcl")
