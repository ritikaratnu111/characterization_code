class RunSimulations():
    def __init__(self):
        self.FABRIC_PATH = None 
        self.TB_DIR_FILE = None
        self.set_fabric_path()
        self.set_tb_dir_file()
        self.run_simulations()
    
    def set_fabric_path(self):
        self.FABRIC_PATH = os.environ["FABRIC_PATH"]

    def set_tb_dir_file(self):
        self.TB_DIR_FILE = "../input_files/TB_DIR_FILE.txt"

    def run_simulations():
        with open(self.TB_DIR_FILE) as fp:
            tb = line.strip()
            assembly = Assembly(tb)
            for component in assembly.active_components:
                Simulation(tb,component,assembly.active_window)
                Simulation(tb,component,assembly.inactive_window)
                Simulation(tb,assembly.all_cycles)
            EnergyEstimator(tb,assembly.active_components,assembly.active_window,assembly.inactive_window,assembly.all_cycles)

RunSimulations()
