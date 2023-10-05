import json
import logging
import constants
from helper_functions import VesylaOutput
from cell import Cell

class Loader():
    def __init__(self,tb,logger):
        self.tb = tb
        self.ASSEMBLY_FILE = f"{tb}/sync_instr.json"
        self.PACKAGE_FILE = f"{tb}/const_package.vhd"
        self.cells = []
        self.window = {'start': 0, 'end': 0}    
        self.logger = logger

    def set_window(self):
        self.window['start'], self.window['end'] = VesylaOutput.return_execution_cycle(self.tb)

    def add_cell(self, cell_id, row, col, instructions):
        print(f"Adding cell {cell_id} to the assembly")
        new_cell = Cell(cell_id, row, col, instructions, self.window)
        self.cells.append(new_cell)
        logging.info(f"Added cell {cell_id} to the assembly")

    def read(self):
#        try:
         self.set_window()
         with open(self.ASSEMBLY_FILE) as file:
             data = json.load(file)   
             for cell in data:
                row = cell['row']
                col = cell['col']
                cell_id = f"cell_{row}_{col}"
                instructions = cell['instr_list']
                self.logger.info(f"Cell: {cell_id}")
                print(f"Cell: {cell_id}")
                if instructions is not None:
                    self.add_cell(cell_id, row, col, instructions)
#        except FileNotFoundError:
#            logging.error(f"File {self.ASSEMBLY_FILE} not found")
#        except json.decoder.JSONDecodeError:
#            logging.error(f"Invalid JSON file {self.ASSEMBLY_FILE}")

    def process(self):
        for cell in self.cells:
            print(f"Processing cell {cell.cell_id}")
            cell.add_active_cell_components()
            cell.add_inactive_cell_components()
            cell.set_instr_active_component_cycles()
            cell.modify_cycles_of_dependent_instructions()
            cell.set_component_active_cycles()
            cell.set_component_inactive_cycles()
            cell.init_component_energy_profiler()
            cell.set_dimarch_tiles()

    def print(self):
        for cell in self.cells:
            cell.print()

    def log(self):
        for cell in self.cells:
            self.logger.info('Active components for cell %s:', id)
            columns = ['      start', '  end', 'cycles']
            log_message = '    '.join([col.ljust(20) for col in columns])
            self.logger.info(log_message)
            self.logger.info(f"Assembly: {cell.total_window['start']} {cell.total_window['end']}")
            for component in cell.components.active:
                self.logger.info('-----------------------------------------------------------')
                self.logger.info(f"{component.name}")
                self.logger.info(f"{component.signals}")
                self.logger.info('-----------------------------------------------------------')
                for window in component.active_window:
                    self.logger.info('  active : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
                for window in component.inactive_window:
                    self.logger.info('inactive : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
            for component in cell.components.inactive:
                self.logger.info('-----------------------------------------------------------')
                self.logger.info(f"{component.name}")
                self.logger.info(f"{component.signals}")
                self.logger.info('-----------------------------------------------------------')

                window = component.window
                self.logger.info('inactive : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
