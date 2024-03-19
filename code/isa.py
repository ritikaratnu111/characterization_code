import json
import sympy as sp
import constants
JSON_FILE_PATH = '/media/storage1/ritika/characterization_code/json_files/'    
class ISA():


    def __init__(self):

        self.segment_values = {}
        self.read_segment_values = {}
        self.components = {}
        self.active_cycles = {}
        self.component_modes = {}
        self.dimarch_row = 0
        self.dimarch_col = 0
        self.dimarch_tiles = []
        self.drra_tile_info =            json.load(open(f"{JSON_FILE_PATH}/drra_tile_info.json"))
        self.dimarch_tile_info =            json.load(open(f"{JSON_FILE_PATH}/dimarch_tile_info.json"))
        self.segment_values =       json.load(open(f"{JSON_FILE_PATH}/instr_segment_values.json"))
        self.component_hierarchy =  json.load(open(f"{JSON_FILE_PATH}/components.json"))["active_components"]["component_hierarchy"]
        self.DRRA_components =      json.load(open(f"{JSON_FILE_PATH}/components.json"))["active_components"]["DRRA_components"]
        self.drra_signals =         json.load(open(f"{JSON_FILE_PATH}/drra_signals.json"))
        self.DIMARCH_components =   json.load(open(f"{JSON_FILE_PATH}/components.json"))["active_components"]["DIMARCH_components"]
#        self.tile_components =   json.load(open(f"{JSON_FILE_PATH}/components.json"))["active_components"]["tile_components"]
        self.dimarch_signals =      json.load(open(f"{JSON_FILE_PATH}/dimarch_signals.json"))
        self.components =           json.load(open(f"{JSON_FILE_PATH}/instr_components.json"))
        self.instr_equations =      json.load(open(f"{JSON_FILE_PATH}/instr_equations.json"))
        self.pc_info =      json.load(open(f"{JSON_FILE_PATH}/pc_info.json"))
        self.inactive_components =  json.load(open(f"{JSON_FILE_PATH}/components.json"))["inactive_components"]["component_hierarchy"]


    def get_drra_tile(self,row,col):
        return self.drra_tile_info[str(row)][str(col)]

    def get_dimarch_tile(self,row,col):
        return self.dimarch_tile_info[str(row)][str(col)]

    def get_dimarch_tiles(self):
        return self.dimarch_tiles

    def set_segment_values(self,name,segment_values):
        for attribute in self.segment_values[name]:
            self.segment_values[name][attribute]  = segment_values[attribute]
#        print(segment_values)
#        print(self.segment_values)

    def get_pc(self,name,id,prev_instr):
        variables = {}

        start = id
        
        if (name != "HALT") and prev_instr.segment_values.get('extra') is not None:
            extra = prev_instr.segment_values['extra']
        else:
            extra = 0

        variables['start'] = start
        variables['extra'] = extra
        
        symbols = {var: sp.symbols(var) for var in variables}
        values = [(symbols[var], val) for var, val in variables.items()]  

        add_pc = sp.sympify(self.pc_info[prev_instr.name]).subs(values)

        return prev_instr.pc + add_pc

    def update_inactive_components_tile_info(self,row,col):
        for component,info in self.inactive_components.items():
            signals = info["signals"] 
            updated_signals = []
            for signal in signals:
                cell_signal = f"{self.drra_signals[str(row)][str(col)]}{signal}"
                updated_signals.append(cell_signal)
            info["signals"] = updated_signals

#Get components for instruction of each cell

    def get_tile(self,instr_name,row,col, segment_values):
        if (instr_name == "ROUTE"):
            print("Route instr")
            self.dimarch_row = segment_values['vertical_hops'] + 1
            self.dimarch_col = segment_values['horizontal_hops'] + col
            print(self.dimarch_row, self.dimarch_col)
        

    def get_components(self,instr_name,row,col,segment_values):

        #Append tile only if the tile is not present already in the list
        if (self.get_dimarch_tile(self.dimarch_row,self.dimarch_col)) not in self.dimarch_tiles:
            self.dimarch_tiles.append(self.get_dimarch_tile(self.dimarch_row,self.dimarch_col))
        instr_components = self.components[instr_name]
        updated_components = {}

        #For each component, get the signals
        for component in instr_components:
            updated_signals = []
            if (component in self.DRRA_components):
                signals = self.DRRA_components[component]["signals"]
                p_inactive_internal = self.DRRA_components[component]["mode"]["running"]["inactive"]["internal"]
                p_inactive_leakage = self.DRRA_components[component]["mode"]["running"]["inactive"]["leakage"]
                for signal in signals:
                    cell_signal = f"{self.drra_signals[str(row)][str(col)]}{signal}"
                    updated_signals.append(cell_signal)
            
            if (component in self.DIMARCH_components):
                signals = self.DIMARCH_components[component]["signals"]
                p_inactive_internal = self.DIMARCH_components[component]["mode"]["running"]["inactive"]["internal"]
                p_inactive_leakage = self.DIMARCH_components[component]["mode"]["running"]["inactive"]["leakage"]
                dimarch_row = self.dimarch_row
                dimarch_col = self.dimarch_col
                for signal in signals:
                    cell_signal = f"{self.dimarch_signals[str(dimarch_row)][str(dimarch_col)]}{signal}"
                    updated_signals.append(cell_signal)
            
            updated_components[component] = {   "name": component,
                                                    "signals": updated_signals,
                                                    "active": {},
                                                    "inactive": {},
                                                    "p_inactive_internal": p_inactive_internal,
                                                    "p_inactive_leakage": p_inactive_leakage
                                                 }
#            elif (component in self.tile_components):
#                signals = self.tile_components[component]["signals"]

            #For each signal, get the cell_signal
#            elif (component in self.tile_components):
#                for signal in signals:
#                    cell_signal = f"{self.drra_signals[str(row)][str(col)]}{signal}"
#                    updated_signals.append(cell_signal)
#                updated_components[component] = {   "name": component,
#                                                        "signals": updated_signals,
#                                                        "active": {},
#                                                        "inactive": {}
#                                                     }
        return updated_components 

    def set_active_cycles(self,name,start, segment_values):
        components = self.components[name]
        if (name == "HALT"):
            variables = {}
        else:
            variables = segment_values
        variables['clock_period'] = constants.CLOCK_PERIOD
        variables['offset'] = start
#        print(name,start,variables)
        equations = self.instr_equations[name]
        self.active_cycles[name] = {}
        self.component_modes[name] = {}

        symbols = {var: sp.symbols(var) for var in variables}
        values = [(symbols[var], val) for var, val in variables.items()]

        for component in components:
            self.active_cycles[name][component] = {}
            start_time = sp.sympify(equations[component]['start']).subs(values)
            end_time = sp.sympify(equations[component]['end']).subs(values)
            mode = sp.sympify(equations[component]['mode']).subs(values)
 #           print(f"Component: {component}, Start time: {start_time}, End time: {end_time}")
            self.active_cycles[name][component] = {
                'start': start_time,
                'end': end_time
            }
            self.component_modes[name][component] = mode

    def get_mode(self, name):
         return self.component_modes[name]

    def get_active_cycles(self, start, name, segment_values):
        self.set_segment_values(name, segment_values)
        self.set_active_cycles(name,start, segment_values)
        return self.active_cycles[name]

    def set_ISA(self):
        self.set_components()

    def print_ISA(self):
        for key,value in self.segment_values.items():
            print(key, value)

