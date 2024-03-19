import constants
from components import ComponentSet, ActiveComponent
import logging
class Instr():
    def __init__(self, id, name, start, pc, segment_values, components ):
        self.id = id
        self.name = name
        self.start = start
        self.pc = pc if pc is not None else 0
        self.segment_values = segment_values
        self.components = components if components is not None else ComponentSet()

    def set_pc(self,my_isa,prev_instr):

        self.pc = my_isa.get_pc(self.name,self.id,prev_instr)

    def set_tile(self,row,col,my_isa):
        my_isa.get_tile(self.name,row,col, self.segment_values)

    def set_components(self,row,col,my_isa):
        from_isa = my_isa.get_components(self.name,row,col,self.segment_values)
        for key,info in from_isa.items():
            name = info["name"]
            signals = info["signals"]
            active = info["active"]
            inactive = info["inactive"]
            c_internal = info["p_inactive_internal"]
            c_leakage = info["p_inactive_leakage"]
            new_component = ActiveComponent(name, signals, active, inactive, c_internal, c_leakage)
            self.components.add_active_component(new_component)

    def set_active_cycles(self,my_isa):
        active_cycles = my_isa.get_active_cycles(self.start, self.name, self.segment_values)
        mode = my_isa.get_mode(self.name)
        for component in self.components.active:
            component.active_window = active_cycles[component.name]
            component.mode = mode[component.name]
#            if(self.name == "DPU"):
#                print(self.name, component.name, component.mode)

    def print(self):
        print(f"Instr: {self.name}")
        print(f"Active components of instruction:")
        self.components.print()
