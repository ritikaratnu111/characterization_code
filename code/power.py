class Power():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = []
        self.inactive_nets = []
        self.active_nets = []

    def set_nets(self,powerfile):
        self.POWER_FILE = powerfile
        header = 103
        tail = 13
        with open(self.POWER_FILE) as file:
            lines = file.readlines()[header:-tail]
            for line in lines:
                line = " ".join(line.split()).split(" ")
                line[5] = 'inactive'
                self.nets.append(line)

    def set_active_nets_legacy(self,signals):
        for signal in signals:
            all_module_signals = signal.split('*')
            for net in self.nets:
                net_name = net[0]
                if all(module_signal in net_name for module_signal in all_module_signals):
                    self.active_nets.append(net)

    def set_active_nets(self,signals):
        for signal in signals:
            all_module_signals = signal.split('*')
            for i in range(len(self.nets)):
                net = self.nets[i]
                net_name = net[0]
                if all(module_signal in net_name for module_signal in all_module_signals):
                    self.nets[i][5] = 'active'

    def set_inactive_nets(self):
        for net in self.nets:
            if net not in self.active_nets:
                self.inactive_nets.append(net)

    def get_active_component_power_legacy(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in self.active_nets:
            internal_power += float(net[2])
            switching_power += float(net[3])
            leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)

    def get_active_component_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in self.nets:
            if(net[5] == 'active'):
                internal_power += float(net[2])
                switching_power += float(net[3])
                leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)

    def get_inactive_component_power_legacy(self):
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

    def get_inactive_component_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in self.nets:
            if(net[5]== 'inactive'):
                internal_power += float(net[2])
                switching_power += float(net[3])
                leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)

    def get_total_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for net in self.nets:
            internal_power += float(net[2])
            switching_power += float(net[3])
            leakage_power += float(net[4])
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power)
