class Assembly():
    def __init__(self,tb):
        self.ASSEMBLY_FILE = ""
        self.instructions = {}
        self.active_components = {}
        self.active_component_cycles = {}
        self.active_windows = {}
        self.set_active_components()
        self.set_assembly_file(tb)
        self.set_assembly()

    def set_assembly_file(self, tb):
        self.ASSEMBLY_FILE = tb + "/assembly.txt"

    def set_assembly(self):
        self.instructions = {'route': [1],
                                'sram': [1],
                                'refi': [6,0,0]}

    def set_active_components(self):
        for instr,attributes in self.instructions:
            instr_active_components = ISA.get_active_components(instr)
            for component in instr_active_components:
                if not component in self.active_components:
                    self.active_components.append(component)

    def set_active_component_cycles():
        for instr,attributes in self.instructions:
            self.active_component_cycles = ISA.get_active_component_cycles(instr)

    def set_active_windows():
        for component in self.active_components:
            active_window = 0
            for component_active_cycles in self.active_component_cycles:
                if component = component_active_cycles.component:
                    self.active_window += component_active_cycles.cycles

