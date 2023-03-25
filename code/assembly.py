from ISA import ISA
#from model import Model
import json
import re
#from power import Power
class Assembly():

    CLOCK_PERIOD = 12

    def __init__(self):
        self.ASSEMBLY_FILE = ""
        self.PACKAGE_FILE = ""
        self.CLOCK_PERIOD = 10
        self.half_period = 5
        self.execution_start_time = 0
        self.total_assembly_cycles = 0
        self.cells = {}

    def set_assembly_file(self, tb):
        self.ASSEMBLY_FILE = f"{tb}/sync_instr.json"
        self.PACKAGE_FILE = f"{tb}/const_package.vhd"

    def set_execution_start_time(self):
        with open(self.PACKAGE_FILE) as file:
            file_contents = file.read()
        execution_start_cycle = int(
            re.search(
                "CONSTANT execution_start_cycle\s*:\s*integer\s*:=\s*(\d+)\s*;",
                file_contents,
            ).group(1)
        )
        self.execution_start_time = self.CLOCK_PERIOD * execution_start_cycle + self.half_period

    def set_instructions(self):
        #These values will be read from the yaml assembly file
#        if (self.ASSEMBLY_FILE == '/home/ritika/silago/SiLagoNN/tb/char/data_transfer/assembly.txt'):
#            self.instructions = {'route': {'instr_delay': 234, 'no_of_hops' : 1} ,
#                                'sram': {'instr_delay': 246, 'no_of_hops' : 1} ,
#                                'refi': {'instr_delay': 258, 'init_delay' : 6, 'l1_iter' : 0, 'l2_iter' : 0}
#                                }
#            self.total_assembly_cycles = {'start': 234, 'end':330} 
        f = open(self.ASSEMBLY_FILE)
        data = json.load(f)
        for cell in data:
            row = cell['row']
            col = cell['col']
            extracted_instr_list = cell['instr_list']
            cell_id = f"cell_{row}_{col}"
            instr_list = [
                {
                    "id": instr["start"],
                    "name": instr["name"],
                    "start_time": self.execution_start_time + instr["start"] * self.CLOCK_PERIOD,
                    "segment_values": instr["segment_values"],
                }
                for instr in extracted_instr_list
            ]
            self.cells[cell_id] = {"row": row, "col": col, "instr_list": instr_list}
        f.close()

    def set_active_components(self):
        for id in self.cells:
            my_isa = ISA()
            active_components = []
            for instr in self.cells[id]['instr_list']:
                instr_components = my_isa.get_components(instr["name"])
                for component in instr_components:
                    if (component not in active_components):
                         active_components.append(component)
                self.cells[id]["active_components"] = active_components
                
    def set_instr_active_component_cycles(self):
        for id in self.cells:
            my_isa = ISA()
            active_component_cycles = []
            for idx, instr in enumerate(self.cells[id]['instr_list']):
                self.cells[id]['instr_list'][idx]['component_active_cycles'] = my_isa.get_active_cycles(instr)

    def set_component_active_cycles(self):
        for id in self.cells:
            self.cells[id]["component_active_cycles"] = {}
            my_isa = ISA()
            for component in self.cells[id]["active_components"]:
                active_window = []
                for idx, instr in enumerate(self.cells[id]['instr_list']):
                    if component in self.cells[id]['instr_list'][idx]['component_active_cycles']:
                        active_window.append(self.cells[id]['instr_list'][idx]['component_active_cycles'][component])                         
                self.cells[id]["component_active_cycles"][component] = active_window
        print(self.cells)

    def set_component_inactive_cycles(self):
        for component in self.active_components:
            inactive_window = []
            start = self.total_assembly_cycles['start']
            for window in self.active_windows[component]:
                end = window['start']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end})
                start = window['end']
            end = self.total_assembly_cycles['end']
            if (start != end):
                inactive_window.append({'start': start, 'end': end})
            self.inactive_windows[component] = inactive_window

    def set_assembly(self):
        self.set_instructions()
        self.set_active_components()
        self.set_instr_active_component_cycles()
#        self.set_component_active_cycles()
#        self.set_component_inactive_cycles()

assembly = Assembly()
assembly.set_assembly_file('/home/ritika/silago/SiLagoNN/tb/char/data_transfer')
assembly.set_execution_start_time()
assembly.set_instructions()
assembly.set_active_components()
assembly.set_instr_active_component_cycles()
assembly.set_component_active_cycles()