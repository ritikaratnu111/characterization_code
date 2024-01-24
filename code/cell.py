import constants
from components import ComponentSet
from assembly import Assembly
from isa import ISA
from cell_profiler import CellProfiler
from helper_functions import AssemblyProcessing
import logging

class Cell():
    """
    Represents a processing element, (in our case DRA cell) with instructions, components, and energy information.
    """
    def __init__(self, cell_id, row, col, window):
        self.cell_id = cell_id
        self.row = row
        self.col = col
        self.total_window = window
        self.total_window['clock_cycles'] = int((self.total_window['end'] - self.total_window['start'] )/constants.CLOCK_PERIOD)
        self.ISA = ISA()
        self.drra_tile = self.ISA.get_drra_tile(row,col)
        self.dimarch_tiles = []
        self.tiles = []
        self.assembly = Assembly() 
        self.components = ComponentSet()
        self.profiler = CellProfiler()
        self.init_profiler()
        logging.info(f"Cell {self.cell_id} created")
        logging.info(f"Cell {self.cell_id} window: {self.total_window}")

    def set_assembly(self,instructions):
        self.assembly.set_ISA(self.ISA)
        self.assembly.set_hop_cycles(self.row,self.col)
        self.assembly.set_window(self.total_window)
        self.assembly.set_assembly(instructions)

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
        print(f"Adding active components to cell {self.cell_id}")
        for idx,instr in enumerate(self.assembly.instructions):
            instr.set_components(self.row,self.col,self.ISA)
            for component in instr.components.active:
                self.components.add_active_component(component)
        self.components.reorder_components()

    def add_inactive_cell_components(self):
        """
        Adds inactive components to the cell of the design.
        """
        self.ISA.update_inactive_components_tile_info(self.row,self.col)
        for component,info  in self.ISA.inactive_components.items():
            self.components.add_inactive_component(component,info,self.total_window)

    def set_pc(self):
        """
        Sets the program counter for the instructions in the assembly.
        """
        self.assembly.set_pc()
    
    def set_delay_for_dpu(self):
        self.assembly.set_delay_for_dpu_swb()

    def adjust_swb(self):
        self.assembly.adjust_swb()

    def unroll_loop(self):
        """
        Unrolls the loop in the assembly.
        """
        self.assembly.unroll_loop()

    def append_segment_values(self):
        self.assembly.append_segment_values()

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
                        if(instr_component.active_window['end'] - instr_component.active_window['start'] != 0):
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
        for component in self.components.inactive:
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

    def adjust_raccu(self):
        for component in self.components.active:
            if(component.name == "raccu"):
                start_window = {'start': self.assembly.window['start'], 
                                    'end': self.assembly.window['start'] + 4 * constants.CLOCK_PERIOD
                }
                component.active_window.append(start_window)
                sorted_window = AssemblyProcessing.sort(component.active_window)
                component.active_window = sorted_window

 
    def print(self):
        print(f"Cell: {self.cell_id}")
        self.assembly.print()
        print(f"Active components:")
        self.components.print()
    
