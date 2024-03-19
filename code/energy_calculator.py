from helper_functions import fabric, tbgen
from helper_functions import VesylaOutput
from loader import Loader
from simulator import Simulator
from power_tracker import PowerParser
from power import Power
import json
import os
import logging

SILAGO_DB_PATH = '/media/storage1/ritika/characterization_code/db/silago_db.json'    
JSON_FILE_PATH = '/media/storage1/ritika/characterization_code/json_files/'    

class ComposableEnergyEstimator():

    def __init__(self):
        self.db = {}
        self.data = {}
        self.logger = None
        logging.basicConfig(level=logging.DEBUG)

    def get_fabric(self):
        self.FABRIC_PATH = fabric.set_path()
        os.environ['FABRIC_PATH'] = self.FABRIC_PATH

    def get_testbenches(self):
        self.testbenches = tbgen.set_testbenches("blas")

    def update_logger(self, path, name, about):
        LOGFILE = f"{path}/estimator.log"
        try:
            with open(LOGFILE, 'w'): pass
            self.logger = logging.getLogger()
            handler = logging.FileHandler(LOGFILE)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.info(f"Testbench: {name}")
            self.logger.info(f"About: {about}")
        except Exception as e:
            print(f"Failed to set logfile: {e}")
            self.logger = None

    def get_data_struct(self):
        self.data = json.load(open(f"{JSON_FILE_PATH}/energy_format.json"))

    def get_activity(self, tb):
        loader = Loader(tb,self.logger)
        loader.read()
        loader.process()
        cells = loader.cells
        return cells

    def get_db(self):
        self.db = json.load(open(f"{SILAGO_DB_PATH}"))
    
    def get_component_dict(self, component, measurement):
        dict = {
                "mode": {
                    str(component.mode): {
                        "active": {
                            "window": f"{component.profiler.active_window['windows']}" if component.active_window else "None",
                            "cycles": component.profiler.active_window['clock_cycles'] if component.active_window else 0,
                            "power": {
                                "internal": measurement["mode"][str(component.mode)]["active"]["power"]["internal"],
                                "switching": measurement["mode"][str(component.mode)]["active"]["power"]["switching"],
                                "leakage": measurement["mode"][str(component.mode)]["active"]["power"]["leakage"]
                                },
                            "energy": {
                                "internal": measurement["mode"][str(component.mode)]["active"]["power"]["internal"] * component.profiler.active_window['clock_cycles'] if component.active_window else 0 ,
                                "switching": measurement["mode"][str(component.mode)]["active"]["power"]["switching"] * component.profiler.active_window['clock_cycles'] if component.active_window else 0 ,
                                "leakage": measurement["mode"][str(component.mode)]["active"]["power"]["leakage"] * component.profiler.active_window['clock_cycles'] if component.active_window else 0 
                                }
                        },
                        "inactive": {
                            "window": f"{component.profiler.inactive_window['windows']}" if component.inactive_window else "None",
                            "cycles": component.profiler.inactive_window['clock_cycles'] if component.inactive_window else 0,
                            "power": {
                                "internal": measurement["mode"][str(component.mode)]["inactive"]["power"]["internal"],
                                "switching": measurement["mode"][str(component.mode)]["inactive"]["power"]["switching"],
                                "leakage": measurement["mode"][str(component.mode)]["inactive"]["power"]["leakage"]
                            },
                            "energy": {
                                "internal": measurement["mode"][str(component.mode)]["inactive"]["power"]["internal"] * component.profiler.inactive_window['clock_cycles'] if component.inactive_window else 0 ,
                                "switching": measurement["mode"][str(component.mode)]["inactive"]["power"]["switching"] * component.profiler.inactive_window['clock_cycles'] if component.inactive_window else 0 ,
                                "leakage": measurement["mode"][str(component.mode)]["inactive"]["power"]["leakage"] * component.profiler.inactive_window['clock_cycles'] if component.inactive_window else 0 
                                }
                        }
                    }
                }
            }
        return dict

    def get_energy(self, cells):
        self.get_data_struct()
        for cell in cells:
            for component in cell.components.active:
                measurement = self.db[component.name]
                self.data[component.name] = self.get_component_dict(component, measurement)
    
    def get_estimates(self):
        self.get_db()
        for name, info in self.testbenches.items():
            if info["to_run"] == True:
                tb = info["path"]
                self.update_logger(tb, name, info['about'])
                cells = self.get_activity(tb)
                self.get_energy(cells)
                self.write_estimate(tb)
    
    def write_estimate(self, tb):
        with open(f"{tb}/estimate.json", "w") as file:
            json.dump(self.data, file, indent=2)
