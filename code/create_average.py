import sys, os
import json
JSON_FILE_PATH = '/media/storage1/ritika/characterization_code/json_files/'    

class Averager():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.data = {}

    def read_data(self, tb, i):
        current_data = {}
        file=f"{tb}/vcd/iter_{i}.json"
        if os.path.exists(file):
            with open(file, "r") as file:
                current_data = json.load(file)
        return current_data

    def get_data(self, tb):
        simulations = []
        for i in range(self.start, self.end):
            current_data = self.read_data(tb, i)
            simulations.append(current_data)
        return simulations

    def get_struct(self):
        struct = json.load(open(f"{JSON_FILE_PATH}/format.json"))
        return struct

    def average_randomized_simulations_per_tb(self, tb):
        simulations = self.get_data(tb)
        data = self.get_struct()
        for simulation in simulations:
            for component, component_info in simulation.items():
                for mode, mode_info in component_info['mode'].items():
                    for state, state_info in mode_info.items():
                        for type, value in state_info["power"].items():
                            data[component]["mode"][mode][state]["power"][type] = (data[component]["mode"][mode][state]["power"][type] + value) / len(simulations)
        return data

    def across_tb(self, testbenches):
        self.data = self.get_struct()
        for name, info in testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                data = self.average_randomized_simulations_per_tb(tb) 
                for component, component_info in data.items():
                    for mode, mode_info in component_info['mode'].items():
                        for state, state_info in mode_info.items():
                            for type, value in state_info["power"].items():
                                self.data[component]["mode"][mode][state]["power"][type] = (self.data[component]["mode"][mode][state]["power"][type] + value) / len(testbenches)
