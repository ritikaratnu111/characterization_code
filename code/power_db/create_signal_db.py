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
        self.component = ""

    def set_assembly_file(self, tb):
        self.tb = tb

    def set_input(self,assembly):
        self.cells = assembly.cells

    def set_db(self):
        for id in self.cells:
            total_window = self.cells[id]['total_window']
            start = total_window['start']
            end = total_window['end'] + 5 * self.CLOCK_PERIOD
            self.logger.debug(f"Total active window for the cell {total_window['start']}, {total_window['end']}")
            for component in self.cells[id]['active_components']:

                start = total_window['start']

                self.db = {}
                component_active_windows = self.cells[id]['component_active_cycles'][component]
                signals = self.cells[id]['active_components'][component]
                logging.debug(f"Db for {self.component}: {signals}")
                while start < end:
                    next = start + self.CLOCK_PERIOD
                    file_path = f"{self.tb}/vcd/{id}_all__{start}_{next}.vcd.pwr"
                    print("first",start)
                    self.db[start] = self.NetPower.set_nets(file_path,signals)
                    self.NetPower.clear_nets()
                    nets = self.db[start]
                    start = next
                for window in component_active_windows:
                    self.logger.debug(f"{self.component} active window start: {window['start']}, end: {window['end']}")
                
                start = total_window['start']
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


tb = "/home/ritika/silago/SiLagoNN/tb/char/data_transfer_signal_db_debug"
assembly = Assembly()
assembly.set_assembly_file(tb)
assembly.set_model()
energy_calculator = EnergyCalculator()
energy_calculator.set_assembly_file(tb)
energy_calculator.set_input(assembly)
energy_calculator.set_db()
#                for net in nets:
#                    if (net == 'Silago_top_l_corner_inst_0_0/SILEGO_cell/MTRF_cell/seq_gen/instr_start_reg'):
#                        print(f"Current update for index... {start} Net: {net} Switching: {self.db[start][net]['switching']} ")
#                for index in self.db:
#                    nets = self.db[index]
#                    for net in nets:
#                        if (net == 'Silago_top_l_corner_inst_0_0/SILEGO_cell/MTRF_cell/seq_gen/instr_start_reg'):
#                            print(f"Iterating over all indexes.. Index: {index} Net: {net} Switching: {self.db[index][net]['switching']} ")
