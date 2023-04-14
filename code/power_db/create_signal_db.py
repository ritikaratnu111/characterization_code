import logging
from power_db import Power
import json
from assembly import Assembly

class EnergyCalculator():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.tb = ""
        self.cells = {}
        self.db = {}
        logging.basicConfig(filename='output.log', level=logging.DEBUG)
        self.logger=logging.getLogger() 
        self.logger.setLevel(logging.DEBUG) 
        self.NetPower = Power()

    def set_assembly_file(self, tb):
        self.tb = tb

    def set_input(self,assembly):
        self.cells = assembly.cells

    #Store the signals for component from all cycles in a dictionary
    def set_db(self):
        component = "sequencer"
        for id in self.cells:
            signals = self.cells[id]['active_components'][component]
            logging.debug(f"Db for {component}: {signals}")
            window = self.cells[id]['total_window']
            start = window['start']
            end = window['end']
            while start < end:
                next = start + self.CLOCK_PERIOD
                file_path = f"{self.tb}/vcd/{id}_all__{start}_{next}.vcd.pwr"
                print(start)
                self.db[start] = self.NetPower.set_nets(file_path,signals)
                self.NetPower.clear_nets()
                nets = self.db[start]
                start = next
                
    #Filter the signals for component from all cycles in a dictionary
    def filter_db(self):
        component = "sequencer"
        for id in self.cells:
            window = self.cells[id]['total_window']
            start = window['start']
            end = window['end']

            while start < end - self.CLOCK_PERIOD:
                select_nets = {}
                total_net_count = 0
                select_net_count = 0
                print(start)
                for net in self.db[start]:
                    if (self.db[start][net]['switching'] != self.db[start + self.CLOCK_PERIOD][net]['switching']):
                        select_nets[net] = {'prev': self.db[start][net]['switching'], 'next': self.db[start + self.CLOCK_PERIOD][net]['switching']}
                        select_net_count += 1
                    total_net_count += 1
                self.logger.debug(f"Prev cycle: {start} Next cycle: {start + self.CLOCK_PERIOD} Total nets: {total_net_count} Select nets: {select_net_count}")
                for net in select_nets:
                    self.logger.debug(f"Nets: {net} Prev: {select_nets[net]['prev']} Next: {select_nets[net]['next']}")
                start = start + self.CLOCK_PERIOD

tb = "/home/ritika/silago/SiLagoNN/tb/char/data_transfer"
assembly = Assembly()
assembly.set_assembly_file(tb)
assembly.set_model()
energy_calculator = EnergyCalculator()
energy_calculator.set_assembly_file(tb)
energy_calculator.set_input(assembly)
energy_calculator.set_db()
energy_calculator.filter_db()
#                for net in nets:
#                    if (net == 'Silago_top_l_corner_inst_0_0/SILEGO_cell/MTRF_cell/seq_gen/instr_start_reg'):
#                        print(f"Current update for index... {start} Net: {net} Switching: {self.db[start][net]['switching']} ")
#                for index in self.db:
#                    nets = self.db[index]
#                    for net in nets:
#                        if (net == 'Silago_top_l_corner_inst_0_0/SILEGO_cell/MTRF_cell/seq_gen/instr_start_reg'):
#                            print(f"Iterating over all indexes.. Index: {index} Net: {net} Switching: {self.db[index][net]['switching']} ")
