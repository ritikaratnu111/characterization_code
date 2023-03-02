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
            for line in fp:
                tb = line.strip()
                Assembly(tb)
                EnergyEstimate(tb)
                Simulate(tb)
                Compare(tb)

RunSimulations()
