from ISA import ISA
#from model import Model
import json
import re
import pprint

#from power import Power
class Assembly():

    CLOCK_PERIOD = 12
    HALF_PERIOD = 6

    def __init__(self):
        self.ASSEMBLY_FILE = ""
        self.PACKAGE_FILE = ""
        self.cells = {}

    def set_assembly_file(self, tb):
        self.ASSEMBLY_FILE = f"{tb}/sync_instr.json"
        self.PACKAGE_FILE = f"{tb}/const_package.vhd"

    def set_instructions(self):
        with open(self.PACKAGE_FILE) as file:
            file_contents = file.read()
        execution_start_cycle = int(
            re.search(
                "CONSTANT execution_start_cycle\s*:\s*integer\s*:=\s*(\d+)\s*;",
                file_contents,
            ).group(1)
        )
        total_execution_cycle = int(
            re.search(
                "CONSTANT total_execution_cycle\s*:\s*integer\s*:=\s*(\d+)\s*;",
                file_contents,
            ).group(1)
        )
        execution_start_time = self.CLOCK_PERIOD * execution_start_cycle + self.HALF_PERIOD
        execution_end_time = self.CLOCK_PERIOD * total_execution_cycle + self.HALF_PERIOD

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
                    "start_time": execution_start_time + instr["start"] * self.CLOCK_PERIOD,
                    "segment_values": instr["segment_values"],
                }
                for instr in extracted_instr_list
            ]
            self.cells[cell_id] = {"row": row, "col": col, "instr_list": instr_list, 'total_window' : {'start' : execution_start_time, 'end' : execution_end_time}}
        f.close()

    def set_active_components(self):
        for id in self.cells:
            my_isa = ISA()
            active_components = {}
            for instr in self.cells[id]['instr_list']:
                instr_components = my_isa.get_components(instr["name"])
                print(instr_components)
                for component in instr_components:
                    if (component not in active_components):
                         active_components[component] = instr_components[component]
                         print(active_components)
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

    def set_component_inactive_cycles(self):
        for id in self.cells:
            self.cells[id]["component_inactive_cycles"] = {}
            my_isa = ISA()
            for component in self.cells[id]["active_components"]:
                inactive_window = []
                start = self.cells[id]['total_window']['start']
                for window in self.cells[id]['component_active_cycles'][component]:
                    end = window['start']
                    if (start != end):
                        inactive_window.append({'start': start, 'end': end})
                    start = window['end']
                end = self.cells[id]['total_window']['end']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end})
                self.cells[id]["component_inactive_cycles"][component] = inactive_window
#            pprint.PrettyPrinter(width=20).pprint(self.cells)   

    def set_model(self):
        self.set_instructions()
        self.set_active_components()
        self.set_instr_active_component_cycles()
        self.set_component_active_cycles()
        self.set_component_inactive_cycles()
        print(self.cells)

assembly = Assembly()
assembly.set_assembly_file('/home/ritika/silago/SiLagoNN/tb/char/data_transfer')
assembly.set_instructions()
assembly.set_active_components()
assembly.set_instr_active_component_cycles()
assembly.set_component_active_cycles()
assembly.set_component_inactive_cycles()
