class Power():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = {}

    def set_nets(self,powerfile):
        self.POWER_FILE = powerfile
        header = 103
        tail = 13
        with open(self.POWER_FILE) as file:
            lines = file.readlines()[header:-tail]
            for line in lines:
                line = " ".join(line.split()).split(" ")
                name = line[0]
                if name in self.nets:
                    label = self.nets[name]['label']
                else:
                    label = 'inactive'
                self.nets[name] = {'internal' : float(line[2]), 'switching' : float(line[3]), 'leakage' : float(line[4]), 'label' : label}
        inactive = 0
        total = 0
        active = 0
        for name in self.nets:
            net = self.nets[name]
            label = net['label']
            if (label == 'inactive'):
                inactive += 1
            else:
                active += 1
            total += 1
#        print("Active: ", active, " Inactive: ", inactive, ' added: ', inactive + active, ' Total: ', total)

    def set_active_nets(self,signals):
        count = 0
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    if all(substring in name for substring in signal_substrings):
                        self.nets[name]['label'] = signal
                        count += 1

    def get_active_component_power(self, signals):
        count = 0
        for signal in signals:
            internal_power = 0
            switching_power = 0
            leakage_power = 0
            for name in self.nets:
                net = self.nets[name]
                if(net['label'] == signal):
                    internal_power += net['internal']
                    switching_power += net['switching']
                    leakage_power += net['leakage']
                    count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
        return(power,count)

    def get_inactive_component_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        count = 0
        for name in self.nets:
            net = self.nets[name]
            if(net['label'] == 'inactive'):
                internal_power += net['internal']
                switching_power += net['switching']
                leakage_power += net['leakage']
                count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
#        print("Inactive net count: ", count)
        return(power,count)

    def get_total_power(self):
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        count = 0
        for name in self.nets:
            net = self.nets[name]
            internal_power += net['internal']
            switching_power += net['switching']
            leakage_power += net['leakage']
            count += 1
        power = {'internal': internal_power, 
                    'switching': switching_power,
                    'leakage': leakage_power
                    }
#        print("Total net count: ", count)
        return(power,count)
