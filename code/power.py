class Power():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = []
        self.inactive_nets = []

    def set_nets(self,powerfile):
        self.POWER_FILE = powerfile
        with open(self.POWER_FILE) as file:
            lines = file.readlines()
            for line in lines:
                line = " ".join(line.split()).split(" ")
                self.nets.append(line)

    def get_active_component_power(self,signals):
        hit_nets = []
        for signal in signals:
            all_module_signals = signal.split('*')
            for net in self.nets:
                net_name = net[0]
                if all(module_signal in net_name for module_signal in all_module_signals):
                    hit_nets.append(net)
                else:
                    self.inactive_nets.append(net)
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in hit_nets:
            internal_power += float(net[2])
            switching_power += float(net[3])
            leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)

    def get_inactive_component_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in self.inactive_nets:
            internal_power += float(net[2])
            switching_power += float(net[3])
            leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)
