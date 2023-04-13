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
                self.nets[name] = {'internal' : float(line[2]), 'switching' : float(line[3]), 'leakage' : float(line[4])}
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                if all(substring in name for substring in signal_substrings):
                    self.filtered_nets[name] = net
        return self.filtered_nets
