class Assembly():
    def __init__(self):
        self._instructions = {}
        self._active_components = {}
        self._active_component_cycles = {}
        self._active_windows = {}

    def set_assembly(self, file):
        for instr in file:
            self._instructions += Instr(instr)

    def set_active_components():
        for instr in self._instructions:
            self._active_component[idx] = Model.get_active_component(instr)
    
    def set_active_component_cycles():
        for instr in self._instructions:
            self._active_component_cycles[idx] = Model.get_active_component_cycles(instr)

    def set_active_window():
        for component in self._active_components:
            self._active_window = 0
            for component_active_cycles in self._active_component_cycles:
                if component = component_active_cycles.component:
                    self._active_window += component_active_cycles.cycles
