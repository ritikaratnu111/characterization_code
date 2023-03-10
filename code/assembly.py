from ISA import ISA
from model import Model
#from power import Power

class Assembly():
    def __init__(self,tb):
        self.ASSEMBLY_FILE = ""
        self.total_assembly_cycles = 0
        self.instructions = {}
        self.active_components = {}
        self.instr_active_component_cycles = {}
        self.active_component_cycles = {}
        self.active_windows = {}
        self.inactive_windows = {}
        self.model = Model()
        self.set_assembly_file(tb)
        self.set_assembly()

    def set_assembly_file(self, tb):
        self.ASSEMBLY_FILE = tb + "/assembly.txt"

    def set_instructions(self):
        #These values will be read from the yaml assembly file
        if (self.ASSEMBLY_FILE == '/home/ritika/silago/SiLagoNN/tb/char/data_transfer/assembly.txt'):
            self.instructions = {'route': {'instr_delay': 234, 'no_of_hops' : 1} ,
                                'sram': {'instr_delay': 246, 'no_of_hops' : 1} ,
                                'refi': {'instr_delay': 258, 'init_delay' : 6, 'l1_iter' : 0, 'l2_iter' : 0}
                                }
            self.total_assembly_cycles = {'start': 234, 'end':330} 

    def set_model_attributes(self):
        for instr in self.instructions:
            self.model.set_model(instr,self.instructions[instr])

    def set_active_components(self):
        for instr in self.instructions:
            instr_components = self.model.ISA.components[instr]
            for component in instr_components:
                if (component not in self.active_components):
                    self.active_components[component] = instr_components[component]
#        print(self.active_components)

    def set_instr_active_component_cycles(self):
        for instr in self.instructions:
            self.instr_active_component_cycles[instr] = self.model.ISA.active_cycles[instr]
#            print(instr, self.instr_active_component_cycles[instr])

#    def active_component_cycles(self):
#        for component in self.active_components:
#            cycles = {}
#            for instr in self.instructions:
#                cycles = self.instructions[instr]

    def set_component_active_cycles(self):
        for component in self.active_components:
#            print(component)
            active_window = []
            for instr in self.instructions:
                if component in (self.instr_active_component_cycles[instr]):
                    active_window.append(self.instr_active_component_cycles[instr][component])
            self.active_windows[component] = active_window
        self.active_windows['total'] = [self.total_assembly_cycles]

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
        self.set_model_attributes()
        self.set_active_components()
        self.set_instr_active_component_cycles()
        self.set_component_active_cycles()
        self.set_component_inactive_cycles()

Assembly('/home/ritika/silago/SiLagoNN/tb/char/data_transfer')
