import json
import sympy as sp
JSON_FILE_PATH = '/home/ritika/Documents/silago/characterization_code/json_files/'    
class ISA():

    CLOCK_PERIOD = 12

    def __init__(self):

        self.segment_values = {}
        self.read_segment_values = {}
        self.components = {}
        self.active_cycles = {}
        self.dimarch_row = 0
        self.dimarch_col = 0
        self.tile_info =            json.load(open(f"{JSON_FILE_PATH}/tile_info.json"))
        self.segment_values =       json.load(open(f"{JSON_FILE_PATH}/instr_segment_values.json"))
        self.component_hierarchy =  json.load(open(f"{JSON_FILE_PATH}/components.json"))["component_hierarchy"]
        self.DRRA_components =      json.load(open(f"{JSON_FILE_PATH}/components.json"))["DRRA_components"]
        self.drra_signals =         json.load(open(f"{JSON_FILE_PATH}/drra_signals.json"))
        self.DIMARCH_components =   json.load(open(f"{JSON_FILE_PATH}/components.json"))["DIMARCH_components"]
        self.dimarch_signals =      json.load(open(f"{JSON_FILE_PATH}/dimarch_signals.json"))
        self.components =           json.load(open(f"{JSON_FILE_PATH}/instr_components.json"))
        self.instr_equations =      json.load(open(f"{JSON_FILE_PATH}/instr_equations.json"))


    def get_tile(self,row,col):
        return self.tile_info[str(row)][str(col)]

    def set_segment_values(self,name,segment_values):
        for attribute in self.segment_values[name]:
            self.segment_values[name][attribute]  = segment_values[attribute]
#        print(segment_values)
#        print(self.segment_values)
        
#Get components for instruction of each cell
    def get_components(self,instr_name,row,col,segment_values):

#        print(f"Row: {row}, Col: {col}")
        if (instr_name == "ROUTE"):
            self.dimarch_row = segment_values['vertical_hops'] + 1
            self.dimarch_col = segment_values['horizontal_hops'] + col
        instr_components = self.components[instr_name]
        updated_components = {}

        #For each component, get the signals
        for component in instr_components:
            signals = instr_components[component]
            updated_signals = []

            #For each signal, get the cell_signal
            if(component in self.DRRA_components):
                for signal in signals:
                    cell_signal = f"{self.drra_signals[str(row)][str(col)][component]}{signal}"
                    updated_signals.append(cell_signal)
                updated_components[component] = {   "name": component,
                                                    "signals": updated_signals,
                                                    "active": {},
                                                    "inactive": {}
                                                 }

            elif (component in self.DIMARCH_components):
                dimarch_row = self.dimarch_row
                dimarch_col = self.dimarch_col
                for signal in signals:
#                    print(f"Signal: {signal}, Row: {dimarch_row}, Col: {dimarch_col}")
                    cell_signal = f"{self.dimarch_signals[str(dimarch_row)][str(dimarch_col)][component]}{signal}"
                    updated_signals.append(cell_signal)
                updated_components[component] = {   "name": component,
                                                    "signals": updated_signals,
                                                    "active": {},
                                                    "inactive": {}
                                                 }
        return updated_components 

    def set_active_cycles(self,name,start, segment_values):
        components = self.components[name]
        if (name == "HALT"):
            variables = {}
        else:
            variables = segment_values
        variables['clock_period'] = self.CLOCK_PERIOD
        variables['offset'] = start
#        print(name,start,variables)
        equations = self.instr_equations[name]
        self.active_cycles[name] = {}

        symbols = {var: sp.symbols(var) for var in variables}
        values = [(symbols[var], val) for var, val in variables.items()]

        for component in components:
            self.active_cycles[name][component] = {}
            start_time = sp.sympify(equations[component]['start']).subs(values)
            end_time = sp.sympify(equations[component]['end']).subs(values)
 #           print(f"Component: {component}, Start time: {start_time}, End time: {end_time}")
            self.active_cycles[name][component] = {
                'start': start_time,
                'end': end_time
            }

    def get_active_cycles(self, start, name, segment_values):
        self.set_segment_values(name, segment_values)
        self.set_active_cycles(name,start, segment_values)
        return self.active_cycles[name]

    def set_ISA(self):
        self.set_components()

    def print_ISA(self):
        for key,value in self.segment_values.items():
            print(key, value)

