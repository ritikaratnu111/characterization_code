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
        self.NetPower = Power()
        logging.basicConfig(filename='output.log', level=logging.DEBUG)

    def set_assembly_file(self, tb):
        self.tb = tb

    def set_input(self,assembly):
        self.cells = assembly.cells

    def set_db(self):
        component = "sequencer"
        for id in self.cells:
            active_signals = self.cells[id]['active_components'][component]
            logging.debug(f"Db for {component}: {active_signals}")
            window = self.cells[id]['total_window']
            start = window['start']
            end = window['end']
            next = start + self.CLOCK_PERIOD
            while next <= end:
                file_path = f"{self.tb}/vcd/{id}_all__{start}_{next}.vcd.pwr"
                self.db[start] = self.NetPower.set_nets(file_path,active_signals)
                start = next
                next = start + self.CLOCK_PERIOD
        print(self.db)

    def filter_db(self):

tb = "/home/ritika/silago/SiLagoNN/tb/char/data_transfer"
assembly = Assembly()
assembly.set_assembly_file(tb)
assembly.set_model()
energy_calculator = EnergyCalculator()
energy_calculator.set_assembly_file(tb)
energy_calculator.set_input(assembly)
energy_calculator.set_db()
