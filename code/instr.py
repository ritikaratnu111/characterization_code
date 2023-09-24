import constants
from components import ComponentSet, ActiveComponent

class Instr():
    def __init__(self, instr, window):
        self.id = instr['start']
        self.name = instr['name']
        self.start = window['start'] + instr['start'] * constants.CLOCK_PERIOD  
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
        for component in self.components.active:
            component.active_window = component_active_cycles[component.name]

    def print(self):
        print(f"Instr: {self.name}")
        print(f"Active components of instruction:")
        self.components.print()
