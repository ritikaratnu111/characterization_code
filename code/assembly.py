import constants
from instr import Instr

class Assembly():
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
                dpu_end = instr.components.active[1].active_window['end']
                wait_cycles = self.instructions[idx + 1].segment_values['cycle']
                print(f"Wait cycles: {wait_cycles}")
                wait_time = wait_cycles * constants.CLOCK_PERIOD
                for component in instr.components.active:
                    if component.name == 'dpu':
                        component.active_window['end'] = dpu_end + wait_time
                    elif component.name == 'swb':
                        component.active_window['start'] = dpu_end
                        component.active_window['end'] = dpu_end + wait_time

    def print(self):
        for instr in self.instructions:
            instr.print()