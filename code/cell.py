import constants
from components import ComponentSet
from assembly import Assembly
from isa import ISA
from energy import CellProfiler
from helper_functions import AssemblyProcessing

class Cell():
    """
    Represents a processing element, (in our case DRA cell) with instructions, components, and energy information.
    """
    def __init__(self, cell_id, row, col, instructions, window):
        self.cell_id = cell_id
        self.row = row
        self.col = col
        self.total_window = window
        self.ISA = ISA()
        self.tile = self.ISA.get_tile(row,col)
        self.assembly = Assembly(instructions, window, self.ISA) 
        self.components = ComponentSet()
        self.profiler = CellProfiler()
        self.init_profiler()

    def init_profiler(self):
        self.profiler.init(self.total_window)

    def add_cell_components(self):
        """
        Adds active components to the cell based on instructions.
        """
        for idx,instr in enumerate(self.assembly.instructions):
            instr.set_components(self.row,self.col,self.ISA)
            for component in instr.components.active:
                self.components.add_active_component(component)
        self.components.reorder_components()

    def set_instr_active_components(self):
        """
        Sets active components for the instructions in the assembly.
        """
        self.assembly.set_instr_active_components(self.row, self.col)

    def set_instr_active_component_cycles(self):
        """
        Sets the active cycles of active components for the instructions in the assembly.
        """
        self.assembly.set_instr_active_component_cycles()

    def modify_cycles_of_dependent_instructions(self):
        """
        Modifies cycles of dependent instructions in the assembly.
        """
        self.assembly.modify_cycles_of_dependent_instructions()

    def set_component_active_cycles(self):
        """
        Sets active cycles for active components in the cell.
        """
        for component in self.components.active:
            active_window = []
            for idx, instr in enumerate(self.assembly.instructions):
                for instr_component in instr.components.active:
                    if component == instr_component:
                        active_window.append(instr_component.active_window)
            sorted_window = AssemblyProcessing.sort(active_window)
            for window in sorted_window:
                window['clock_cycles'] = int((window['end'] - window['start'] )/constants.CLOCK_PERIOD)
            
            component.active_window = sorted_window

    def set_component_inactive_cycles(self):   
        """
        Sets inactive cycles for active components in the cell.
        """
        for component in self.components.active:
            inactive_window = []
            start = self.total_window['start']
            for window in component.active_window:
                end = window['start']
                if (start != end):
                    inactive_window.append({'start': start, 'end': end, 'clock_cycles' : int((end-start)/constants.CLOCK_PERIOD) })
                start = window['end']
            end = self.total_window['end']
            if (start != end):
                inactive_window.append({'start': start, 'end': end, 'clock_cycles' : int((end-start)/constants.CLOCK_PERIOD) })
            component.inactive_window = inactive_window

    def init_component_energy_profiler(self):
        """
        Initializes energy profiler for active components in the cell.
        """
        for component in self.components.active:
            component.init_profiler(self.total_window)

    def set_remaining_power(self,iter):
        """
        Sets remaining power of the cell.
        """
        self.profiler.set_remaining_power(self.components.active)

    def print(self):
        print(f"Cell: {self.cell_id}")
        self.assembly.print()
        print(f"Active components:")
        self.components.print()
    