import os
import logging

class Power():
    def __init__(self):
        self.POWER_FILE = ""
        self.nets = {}
        logfile = "signals.log"
        logging.basicConfig(filename=logfile, level=logging.DEBUG)

    def set_nets(self,powerfile):
        self.POWER_FILE = powerfile
        header = 104
        tail = 15
        with open(self.POWER_FILE) as file:
            lines = file.readlines()[header:-tail]
            for line in lines:
                line = " ".join(line.split()).split(" ")
                name = line[0]
                if name in self.nets:
                    label = self.nets[name]['label']
                else:
                    label = 'inactive'
                self.nets[name] = {'internal' : float(line[3]), 'switching' : float(line[4]), 'leakage' : float(line[5]), 'label' : label}
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

    def find_active_nets(self,signals):
        count = 0
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    if all(substring in name for substring in signal_substrings):
                        if (net['internal'] == 0):
                            print(net)

    def set_active_nets(self,signals):
        count = 0
        #logging.info('Signals: %s', signals)
        for signal in signals:
            signal_substrings = signal.split('*')
            for name in self.nets:
                net = self.nets[name]
                label = net['label']
                if (label == 'inactive'):
                    if all(substring in name for substring in signal_substrings):
                        self.nets[name]['label'] = signal
                        #Log the net name if the switching power is not 0
                        if (net['switching'] != 0):
                            logging.info('Net: %s', name)
                        count += 1

    def get_active_component_dynamic_power(self, signals):
        count = 0
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for signal in signals:
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

    def get_active_component_leakage_power(self, signals):
        count = 0
        internal_power = 0
        switching_power = 0
        leakage_power = 0
        for signal in signals:
            for name in self.nets:
                net = self.nets[name]
                if(net['label'] == signal):
                    leakage_power += net['leakage']
                    count += 1
        return(leakage_power,count)

    def get_remaining_power(self):
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
