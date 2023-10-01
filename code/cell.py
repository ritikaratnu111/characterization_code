import constants
from components import ComponentSet
from assembly import Assembly
from isa import ISA
from cell_profiler import CellProfiler
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
        self.drra_tile = self.ISA.get_drra_tile(row,col)
        self.dimarch_tiles = []
        self.tiles = []
        self.assembly = Assembly(instructions, window, self.ISA) 
        self.components = ComponentSet()
        self.profiler = CellProfiler()
        self.init_profiler()

    def init_profiler(self):
        window = {}
        window['start'] = self.total_window['start']
        window['end'] = self.total_window['end']
        window['clock_cycles'] = int((self.total_window['end'] - self.total_window['start'] )/constants.CLOCK_PERIOD)
        self.profiler.init(window)

    def add_active_cell_components(self):
        """
        Adds active components to the cell based on instructions.
        """
        for idx,instr in enumerate(self.assembly.instructions):
            instr.set_components(self.row,self.col,self.ISA)
            for component in instr.components.active:
                self.components.add_active_component(component)
        self.components.reorder_components()

        for component in self.components.active:
            print(f"Component: {component.name}")
            for signal in component.signals:
                print(f"Signal: {signal}")

    def add_inactive_cell_components(self):
        """
        Adds inactive components to the cell of the design.
        """
        for component in self.ISA.inactive_components:
            print(f"Component: {component.name}")
            self.components.add_inactive_component(component)

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

    def set_AEC_measurement(self,iter):
        """
        Sets AEC measurement for the cell.
        """
        self.profiler.set_AEC_measurement(self.components.active,iter)

    def set_dimarch_tiles(self):
        """
        Sets the dimarch tiles for the cell.
        """
        self.dimarch_tiles = self.ISA.get_dimarch_tiles()
        self.tiles.extend(self.dimarch_tiles)
        self.tiles.append(self.drra_tile)

    def set_remaining_measurement(self,reader,iter):
        """
        Sets total power of the cell.
        """
        self.profiler.set_remaining_measurement(reader,self.tiles,iter)

    def set_total_measurement(self,reader,iter):
        """
        Sets total power of the cell.
        """
        self.profiler.set_total_measurement(reader,self.tiles,iter)

    def set_diff_measurement(self):
        """
        Sets the difference between total and remaining power of the cell.
        """
        self.profiler.set_diff_measurement()

    def print(self):
        print(f"Cell: {self.cell_id}")
        self.assembly.print()
        print(f"Active components:")
        self.components.print()
    
