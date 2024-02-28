import json
import logging
import constants
from helper_functions import VesylaOutput
from cell import Cell

class Loader():
    def __init__(self,tb,logger):
        self.tb = tb
        self.ASSEMBLY_FILE = f"{tb}/sync_instr.json"
        self.PACKAGE_FILE = f"{tb}/const_package.vhd"
        self.cells = []
        self.window = {'start': 0, 'end': 0}    
        self.logger = logger

    def set_window(self):
        self.window['start'], self.window['end'] = VesylaOutput.return_execution_cycle(self.tb)

    def add_cell(self, cell_id, row, col, instructions):
        new_cell = Cell(cell_id, row, col, self.window)
        new_cell.set_assembly(instructions)
        self.cells.append(new_cell)
        logging.info(f"Added cell {cell_id} to the assembly")

    def read(self):
#        try:
         self.set_window()
         with open(self.ASSEMBLY_FILE) as file:
             data = json.load(file)   
             for cell in data:
                row = cell['row']
                col = cell['col']
                cell_id = f"cell_{row}_{col}"
                instructions = cell['instr_list']
                self.logger.info(f"Cell: {cell_id}")
                print(f"Cell: {cell_id}")
                if instructions is not None:
                    self.add_cell(cell_id, row, col, instructions)
#        except FileNotFoundError:
#            logging.error(f"File {self.ASSEMBLY_FILE} not found")
#        except json.decoder.JSONDecodeError:
#            logging.error(f"Invalid JSON file {self.ASSEMBLY_FILE}")

    def process(self):
        for cell in self.cells:
            print(f"Processing cell {cell.cell_id}")
            cell.set_pc()
            cell.set_delay_for_dpu()
#            cell.adjust_swb()
            cell.unroll_loop()
#            cell.append_segment_values()
            cell.add_active_cell_components()
            cell.add_inactive_cell_components()
            cell.set_instr_active_component_cycles()
#            cell.modify_cycles_of_dependent_instructions()
            cell.set_component_active_cycles()
            cell.adjust_raccu()
            cell.set_component_inactive_cycles()
            cell.init_component_energy_profiler()
            cell.set_dimarch_tiles()
#            for component in cell.components.active:
#                print(component.name, component.active_window, component.signals)
                #logging.info(component.name, component.active_window)
        self.get_dependency()

    def get_dependency(self):
        for cell in self.cells:
            if cell.cell_id == "cell_1_0":
                for component in cell.components.active:
                    if (component.name == "bus_selector" or component.name == "noc"):
                        self.set_dependency("cell_0_0",component)

    def set_dependency(self,cell_id,dependent_component):                
        for cell in self.cells:
            if cell.cell_id == cell_id:
                for component in cell.components.active:
                    if component.name == dependent_component.name:
                        for window in dependent_component.active_window:
                            component.active_window.append(window)
                    cell.set_component_inactive_cycles()

    def print(self):
        for cell in self.cells:
            cell.print()

    def log_window(self):
        for cell in self.cells:
            self.logger.info('---------------------------------Logging windows--------------')
            for component in cell.components.active:
                self.logger.info(f"{component.name}")
                self.logger.info(f"{component.signals}")
                self.logger.info('-----------------------Model-------------------------------')
                for window in component.active_window:
                    self.logger.info('  active : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
                for window in component.inactive_window:
                    self.logger.info('inactive : %s %s %s ', str(window['start']).ljust(20), 
                                                       str(window['end']).ljust(20),
                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
                self.logger.info('-----------------------Actual------------------------------')
                for window in component.profiler.per_cycle_active_window:
                    self.logger.info('  active : %s %s %s ', str(window[0]).ljust(20), 
                                                       str(window[1]).ljust(20),
                                                       str(int((window[1] - window[0])/constants.CLOCK_PERIOD)).ljust(20))

    def log_AEC_per_cycle_measurement(self):
        self.logger.info('---------------------All Data------------------------------')
        for cell in self.cells:
            for component in cell.components.active:
                self.logger.info(f"{component.name}")
                for measurement in component.profiler.per_cycle_measurement:
                    measurement.log_power()

    def log_AEC_measurements_from_per_cycle(self):
        for cell in self.cells:
            nets = 0
            self.logger.info('-------------------AEC measurement from per_cycle data----------------------')
            for component in cell.components.active:
                #if(component.name != "noc"):
                #    continue
                self.logger.info(f"{component.name}")
                self.logger.info(f"Total accounted nets without {component.name}: {nets}")
                self.logger.info('-------------------active power-----------------------------------------')
                for measurement in component.profiler.active_measurement_from_per_cycle:
                    measurement.log_power()
                self.logger.info('-------------------inactive power---------------------------------------')
                for measurement in component.profiler.inactive_measurement_from_per_cycle:
                    measurement.log_power()
                self.logger.info('-------------------active energy----------------------------------------')
                for measurement in component.profiler.active_measurement_from_per_cycle:
                    measurement.log_energy()
                self.logger.info('-------------------inactive energy--------------------------------------')
                for measurement in component.profiler.inactive_measurement_from_per_cycle:
                    measurement.log_energy()
                self.logger.info('total energy from per_cycle data')
                component.profiler.total_measurement_from_per_cycle.log_energy()
                self.logger.info('total energy from iter file data')
                component.profiler.total_measurement_from_iter_file.log_energy()
                nets += component.profiler.total_measurement_from_per_cycle.nets
                self.logger.info(f"Total accounted nets with {component.name}: {nets}")

            for component in cell.components.inactive:
                #if(component.name != "data_selector"):
                #    continue
                self.logger.info(f"{component.name}")
                self.logger.info('-------------------active power-----------------------------------------')
                for measurement in component.profiler.active_measurement_from_per_cycle:
                    measurement.log_power()
                self.logger.info('-------------------inactive power---------------------------------------')
                for measurement in component.profiler.inactive_measurement_from_per_cycle:
                    measurement.log_power()
                self.logger.info('-------------------active energy----------------------------------------')
                for measurement in component.profiler.active_measurement_from_per_cycle:
                    measurement.log_energy()
                self.logger.info('-------------------inactive energy--------------------------------------')
                for measurement in component.profiler.inactive_measurement_from_per_cycle:
                    measurement.log_energy()
                nets += component.profiler.total_measurement_from_per_cycle.nets
                self.logger.info('total energy from per_cycle data')
                component.profiler.total_measurement_from_per_cycle.log_energy()
                self.logger.info('total energy from iter file data')
                component.profiler.total_measurement_from_iter_file.log_energy()
                nets += component.profiler.total_measurement_from_per_cycle.nets
                self.logger.info(f"Total accounted nets with {component.name}: {nets}")

    def log_cell_measurements(self):
        self.logger.info('-------------------Cell measurement----------------------')
        for cell in self.cells:
            self.logger.info(f"Total nets in cell: {cell.cell_id} {cell.profiler.total_measurement.nets}")
            self.logger.info('-------------------active energy----------------------------------------')
            cell.profiler.active_AEC_measurement.log_energy()
            self.logger.info('-------------------inactive energy--------------------------------------')
            cell.profiler.inactive_AEC_measurement.log_energy()
            self.logger.info('-------------------total energy-----------------------------------------')
            cell.profiler.total_measurement.log_energy()
            self.logger.info('-------------------error energy-----------------------------------------')
            cell.profiler.error_measurement.log_energy()        

    def log(self):
        for cell in self.cells:
            self.logger.info('Active components for cell %s:', id)
            columns = ['      start', '  end', 'cycles']
            log_message = '    '.join([col.ljust(20) for col in columns])
            self.logger.info(log_message)
            self.logger.info(f"{cell.cell_id} Assembly: {cell.assembly.window['start']} {cell.assembly.window['end']}")
    
#            self.logger.info(f"Loop info:")
#            for loop_instr_pc, loop_info in cell.assembly.loop_instr.items():
#                self.logger.info(f"Loop start: {loop_info['start']} Loop end: {loop_info['end']}")
    #            self.logger.info(f"Loop instructions:")
    #            for instr in loop_info['repeating_instructions']:
    #                self.logger.info(f"{instr.name} {instr.start} {instr.pc}")
    #            self.logger.info(f"Unrolled instructions:")
    #            for instr in loop_info['unrolled_instructions']:
    #                self.logger.info(f"{instr.name} {instr.start} {instr.pc}")
    
#            self.logger.info('-----------------------------------------------------------')
#            self.logger.info(f"Instructions:")
#            for instr in cell.assembly.instructions:
#                self.logger.info(f"{instr.name} {instr.start} {instr.pc}")
            
#            for instr in cell.assembly.instructions:
#                self.logger.info(f"Instruction: {instr.name} {instr.start} {instr.pc}")
#    


#            for component in cell.components.inactive:
#                self.logger.info('-----------------------------------------------------------')
#                self.logger.info(f"{component.name}")
#                self.logger.info(f"{component.signals}")
#                self.logger.info('-----------------------------------------------------------')
#    
#                window = component.window
#                self.logger.info('inactive : %s %s %s ', str(window['start']).ljust(20), 
#                                                       str(window['end']).ljust(20),
#                                                       str(int((window['end'] - window['start'])/constants.CLOCK_PERIOD)).ljust(20))
