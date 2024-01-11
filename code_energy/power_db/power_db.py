class Power():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = {}
        self.filtered_nets = {}

    def set_nets(self,powerfile,signals):
        self.POWER_FILE = powerfile
        header = 104
        tail = 15
        with open(self.POWER_FILE) as file:
            lines = file.readlines()[header:-tail]
            for line in lines:
                line = " ".join(line.split()).split(" ")
                name = line[0]
                self.nets[name] = {'internal' : float(line[3]), 'switching' : float(line[4]), 'leakage' : float(line[5])}
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                if all(substring in name for substring in signal_substrings):
                    self.filtered_nets[name] = net
#                    if (name == 'Silago_top_l_corner_inst_0_0/SILEGO_cell/MTRF_cell/seq_gen/instr_start_reg'):
#                        print("power_db ", self.filtered_nets[name])
        return self.filtered_nets

    def clear_nets(self):
        self.nets = {}
        self.filtered_nets = {}
