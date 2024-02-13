import logging
from power_db import Power
import json
from assembly import Assembly

class EnergyCalculator():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.tb = ""
        self.db = {}
        logging.basicConfig(filename='sequencer_output.log', level=logging.DEBUG)
        self.logger=logging.getLogger() 
        self.logger.setLevel(logging.DEBUG) 
        self.NetPower = Power()
        self.component = ""

    def set_assembly_file(self, tb):
        self.tb = tb

    def set_db(self):
        start = 378
        end = 500
        self.db = {}
        id = '0'
        signals = ['NOC', 'pc_reg']
        logging.debug(f"Db for {self.component}: {signals}")
        while start < end:
            next = start + self.CLOCK_PERIOD
            file_path = f"{self.tb}/vcd/{id}_sequencer__{start}_{next}.vcd.pwr"
            print("first",start)
            self.db[start] = self.NetPower.set_nets(file_path,signals)
            self.NetPower.clear_nets()
            nets = self.db[start]
            start = next
        
        start = 378
        print(start)
        while start < end - 1 * self.CLOCK_PERIOD:
            select_nets = {}
            total_net_count = 0
            select_net_count = 0
            print("second",start)
            for net in self.db[start]:
                if (self.db[start][net]['switching'] != self.db[start + self.CLOCK_PERIOD][net]['switching']):
                    select_nets[net] = {'prev': self.db[start][net]['switching'], 'next': self.db[start + self.CLOCK_PERIOD][net]['switching']}
                    select_net_count += 1
                total_net_count += 1
            self.logger.debug(f"Nets that change value between cycles {start},{start + self.CLOCK_PERIOD} and {start + self.CLOCK_PERIOD},{start + 2*self.CLOCK_PERIOD} are {select_net_count} out of {total_net_count} total nets")
            for net in select_nets:
                self.logger.debug(f"Nets: {net} Prev: {select_nets[net]['prev']} Next: {select_nets[net]['next']}")
            start = start + self.CLOCK_PERIOD


tb = "/media/storage1/ritika/SiLagoNN/tb/char/sequencer"
energy_calculator = EnergyCalculator()
energy_calculator.set_assembly_file(tb)
energy_calculator.set_db()
