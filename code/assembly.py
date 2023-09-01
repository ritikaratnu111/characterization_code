from ISA import ISA
#from model import Model
import json
import re
import pprint
import logging
from helper_functions import VesylaOutput 
from helper_functions import AssemblyProcessing

CLOCK_PERIOD = 12
HALF_PERIOD = 6

class ActiveComponent():
    def __init__(self, name, signals, active, inactive):
        self.name = name
        self.signals = signals
        self.active = active if active is not None else {}
        self.inactive = inactive if inactive is not None else {}

    def __eq__(self, other):
        if isinstance(other, ActiveComponent):
            return (
                self.name == other.name and
                self.signals == other.signals 
#                self.active == other.active and
#                self.inactive == other.inactive
            )
        return False

    def print(self):
        print(f"Component: {self.name}, {self.active}, {self.inactive}")

class ComponentSet():
    def __init__(self, active_components=None):
        self.active_components = []

    def add_active_component(self,component):
        if (component not in self.active_components):
            self.active_components.append(component)

    def reorder_components(self):
        my_isa = ISA()
        component_hierarchy = my_isa.component_hierarchy
        component_hierarchy_dict = {component: index for index, component in enumerate(component_hierarchy)}
        sorted_components = sorted(self.active_components, key=lambda component: component_hierarchy_dict.get(component.name, float('inf')))
        self.active_components = sorted_components

    def add_active_window(self):
        for component in self.active_components:
            active_window = []
            start = self.total_window['start']
            for window in component.active:
                end = window['start']
                if (start != end):
                    active_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                active_window.append({'start': start, 'end': end})
            component.active = active_window
    
    def add_inactive_window(self):
        for component in self.active_components:
            inactive_window = []
            start = self.total_window['start']
            for window in component.active:
                end = window['start']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                inactive_window.append({'start': start, 'end': end})
            component.inactive = inactive_window

    def print(self):
        for component in self.active_components:
            component.print()

class Instr():
    def __init__(self, instr, window):
        self.id = instr['start']
        self.name = instr['name']
        self.start = window['start'] + instr['start'] * CLOCK_PERIOD  
        self.segment_values = instr['segment_values']
        self.components = ComponentSet()

    def set_components(self,row,col,my_isa):
        from_isa = my_isa.get_components(self.name,row,col,self.segment_values)
        for key,info in from_isa.items():
            name = info["name"]
            signals = info["signals"]
            active = info["active"]
            inactive = info["inactive"]
            new_component = ActiveComponent(name, signals, active, inactive)
            self.components.add_active_component(new_component)

    def set_active_cycles(self,my_isa):
        component_active_cycles = my_isa.get_active_cycles(self.start, self.name, self.segment_values)
        for component in self.components.active_components:
            component.active = component_active_cycles[component.name]

    def print(self):
        print(f"Instr: {self.name}")
        print(f"Active components of instruction:")
        self.components.print()

class CellAssembly():
    def __init__(self,instructions=None, window=None, ISA=None):
        self.instructions = []
        self.window = window if window is not None else {}
        self.ISA = ISA

        for instr in instructions:
            self.add_instr(instr, window)

    def add_instr(self, instr, window):
        new_instr = Instr(instr, window)
        self.instructions.append(new_instr)

    def add_assembly(self, assembly):
        if (assembly):
            for instr in assembly:
                self.add_instr(instr, self.window)

    def set_instr_active_components(self,row,col):
        for idx,instr in enumerate(self.instructions):
            instr.set_components(row,col,self.ISA)

    def set_instr_active_component_cycles(self):
        for idx,instr in enumerate(self.instructions):
            instr.set_active_cycles(self.ISA)

    def modify_cycles_of_dependent_instructions(self):
        for idx, instr in enumerate(self.instructions):
            if(instr.name == 'DPU'):
                dpu_end = instr.component_active_cycles['dpu']['end']
                wait_cycles = self.cells[id].cell_assembly[idx + 1].segment_values['cycle']
                wait_time = wait_cycles * self.CLOCK_PERIOD
                instr.component_active_cycles['dpu']['end'] =  dpu_end + wait_time
                instr.component_active_cycles['swb']['start'] =  dpu_end
                instr.component_active_cycles['swb']['end'] =  wait_time

    def print(self):
        for instr in self.instructions:
            instr.print()

class Cell():
    def __init__(self, cell_id, row, col, instructions, window):
        self.cell_id = cell_id
        self.row = row
        self.col = col
        self.total_window = window
        self.ISA = ISA()
        self.cell_assembly = CellAssembly(instructions, window, self.ISA) 
        self.active_components = ComponentSet()
        self.tile = self.ISA.get_tile(row,col)

    def add_cell_components(self):
        for idx,instr in enumerate(self.cell_assembly.instructions):
            instr.set_components(self.row,self.col,self.ISA)
            for component in instr.components.active_components:
                self.active_components.add_active_component(component)
        self.active_components.reorder_components()

    def set_instr_active_components(self):
        self.cell_assembly.set_instr_active_components(self.row, self.col)

    def set_instr_active_component_cycles(self):
        self.cell_assembly.set_instr_active_component_cycles()

    def modify_cycles_of_dependent_instructions(self):
        self.cell_assembly.modify_cycles_of_dependent_instructions()

    def set_component_active_cycles(self):
        for component in self.active_components.active_components:
            print(f"Current Component: {component.name}")
            active_window = []
            for idx, instr in enumerate(self.cell_assembly.instructions):
                for instr_component in instr.components.active_components:
                    if component == instr_component:
                        active_window.append(instr_component.active)
            sorted_window = AssemblyProcessing.sort(active_window)
            for window in sorted_window:
                window['clock_cycles'] = int((window['end'] - window['start'] )/CLOCK_PERIOD)
            
            component.active = sorted_window

    def set_component_inactive_cycles(self):
        for component in self.active_components.active_components:
            inactive_window = []
            start = self.total_window['start']
            for window in component.active:
                end = window['start']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                inactive_window.append({'start': start, 'end': end})
            component.inactive = inactive_window

    def print(self):
        print(f"Cell: {self.cell_id}")
        self.cell_assembly.print()
        print(f"Active components:")
        self.active_components.print()

class Assembly():
    def __init__(self,tb):
        self.tb = tb
        self.ASSEMBLY_FILE = f"{tb}/sync_instr.json"
        self.PACKAGE_FILE = f"{tb}/const_package.vhd"
        self.cells = []
        self.window = {'start': 0, 'end': 0}    

    def set_window(self):
        self.window['start'], self.window['end'] = VesylaOutput.return_execution_cycle(self.tb)

    def add_cell(self, cell_id, row, col, instructions):
        new_cell = Cell(cell_id, row, col, instructions, self.window)
        self.cells.append(new_cell)
        print(f"Added cell {cell_id} to the assembly")

    def read(self):
        self.set_window()
        f = open(self.ASSEMBLY_FILE)
        data = json.load(f)
        for cell in data:
            row = cell['row']
            col = cell['col']
            cell_id = f"cell_{row}_{col}"
            instructions = cell['instr_list']
            if instructions is not None:
                self.add_cell(cell_id, row, col, instructions)
        f.close()

    def set_active_components(self):
        for cell in self.cells:
            cell.add_cell_components()

    def set_instr_active_component_cycles(self):
        for cell in self.cells:
            cell.set_instr_active_component_cycles()
            cell.modify_cycles_of_dependent_instructions()

    def set_component_active_cycles(self):
        for cell in self.cells:
            cell.set_instr_active_component_cycles()
            cell.modify_cycles_of_dependent_instructions()
            cell.set_component_active_cycles()

    def set_component_inactive_cycles(self):
        for cell in self.cells:
            cell.set_component_inactive_cycles()

    def print(self):
        for cell in self.cells:
            cell.print()

    def log(self):
        for cell in self.cells:
            logging.info('Active components for cell %s:', id)
            columns = ['      start', '  end', 'cycles']
            log_message = '    '.join([col.ljust(20) for col in columns])
            logging.info(log_message)
            logging.info(f"Assembly: {cell.total_window['start']} {cell.total_window['end']}")
            for component in cell.active_components.active_components:
                logging.info('-----------------------------------------------------------')
                logging.info(f"{component.name}")
                logging.info('-----------------------------------------------------------')
                for window in component.active:
                    logging.info('  active : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/CLOCK_PERIOD)).ljust(20))
                for window in component.inactive:
                    logging.info('inactive : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/CLOCK_PERIOD)).ljust(20))
