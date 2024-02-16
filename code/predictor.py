import os
import json
import logging
import matplotlib.pyplot as plt

class Predictor():
    def __init__(self, tb, start, end):
        self.tb = tb
        self.start = start
        self.end = end
        self.data = []
        self.running_average = []
        self.running_average_error = []
        self.avg_file =f"{self.tb}/avg_{self.start}_{self.end}.json"  

    def read_data(self):
        for i in range(self.start, self.end):
            file=f"{self.tb}/vcd/iter_{i}.json"
            if os.path.exists(file):
                with open(file, "r") as file:
                    self.data.append(json.load(file))

    def get_power(self,component, data):
        if("cell_" not in component):
            internal = data["active"]["power"]["internal"]
            switching = data["active"]["power"]["switching"]
            leakage = data["active"]["power"]["leakage"]
        else:
            internal = data["power"]["internal"]
            switching = data["power"]["switching"]
            leakage = data["power"]["leakage"]

        total = internal + switching + leakage

        return internal, switching, leakage, total

    def get_struct(self,component,value):
        struct = {}
        if("cell_" not in component):
            struct[component] = {
                    "active" : {
                        "window" : value["active"]["window"],
                        "cycles" : value["active"]["cycles"],
                        "power" : {
                            "internal" : "0",
                            "switching" : "0",
                            "leakage" : "0",
                            "total" : "0"
                        }
                    },
                    "inactive" : {
                        "window" : value["inactive"]["window"],
                        "cycles" : value["inactive"]["cycles"],
                        "power" : {
                            "internal" : value["inactive"]["power"]["internal"],
                            "switching" :value["inactive"]["power"]["switching"] ,
                            "leakage" : value["inactive"]["power"]["leakage"],
                            "total" : value["inactive"]["power"]["internal"] + value["inactive"]["power"]["switching"] + value["inactive"]["power"]["leakage"]
                        }
                    
                    }
            
            }
        else:
            struct[component] = {
                        "window" : value["window"],
                        "cycles" : value["cycles"],
                        "power" : {
                            "internal" : "0",
                            "switching" : "0",
                            "leakage" : "0",
                            "total" : "0"
                        }
                    }


        return struct

    def get_average(self, component, value, i):
        internal = []
        switching = []
        leakage = []
        total = []

        avg = self.get_struct(component, value)

        # Get a list of powers up to current i
        for i in range(self.start, i):
            i, s, l, t = self.get_power(component, self.data[i - self.start][component])
            internal.append(i)
            switching.append(s)
            leakage.append(l)
            total.append(t)
                
        avg_internal = sum(internal) / len(internal)
        avg_switching = sum(switching) / len(switching)
        avg_leakage = sum(leakage) / len(leakage)
        avg_total = sum(total) / len(total)

        if("cell_" not in component):
            avg[component]["active"]["power"]["internal"] = avg_internal
            avg[component]["active"]["power"]["switching"] = avg_switching
            avg[component]["active"]["power"]["leakage"] = avg_leakage
            avg[component]["active"]["power"]["total"] = avg_total
        else:
            avg[component]["power"]["internal"] = avg_internal
            avg[component]["power"]["switching"] = avg_switching
            avg[component]["power"]["leakage"] = avg_leakage
            avg[component]["power"]["total"] = avg_total


        return avg

    def get_error(self, component, value, i):
        internal = []
        switching = []
        leakage = []
        total = []

        error = self.get_struct(component, value)

        # Get a list of powers up to current i
        i1, s1, l1, t1 = self.get_power(component, self.running_average[i-1 -self.start][component])
        i2, s2, l2, t2 = self.get_power(component, self.running_average[i -self.start][component])

        if (max(i1,i2)== 0):
            error_internal = 0
        else:
            error_internal =  (abs(i1 - i2) / max(i1, i2) ) * 100
        if (max(s1,s2)== 0):
            error_switching = 0
        else:
            error_switching = (abs(s1 - s2) / max(s1, s2) ) * 100 
        if (max(l1,l2)== 0):
            error_leakage = 0
        else:
            error_leakage = (abs(l1 - l2) / max(l1, l2) ) * 100
        if (max(t1,t2)== 0):
            error_total = 0
        else:
            error_total = (abs(t1 - t2) / max(t1, t2) ) * 100

        if("cell_" not in component):
            error[component]["active"]["power"]["internal"] = error_internal
            error[component]["active"]["power"]["switching"] = error_switching
            error[component]["active"]["power"]["leakage"] = error_leakage
            error[component]["active"]["power"]["total"] = error_total
        else:
            error[component]["power"]["internal"] = error_internal
            error[component]["power"]["switching"] = error_switching
            error[component]["power"]["leakage"] = error_leakage
            error[component]["power"]["total"] = error_total


        return error

    def write_json(self):
        with open(self.avg_file, "w") as file:
            json.dump(self.running_average[(self.end - self.start -2)], file, indent=2)


    def get_running_error(self):
        for i in range(self.start + 1, self.end - 1):
            current_error = {}
            for component, value in self.running_average[i -self.start].items():
                current_error.update( self.get_error(component, value, i))
            self.running_average_error.append(current_error)
        print(self.running_average_error)

    def get_prediction(self):
        self.read_data()
        print(len(self.data))
        for i in range(self.start + 1, self.end):
            current_avg = {}
            for component,value in self.data[i - self.start].items():
                #if(component != "dimarch_agu"):
                #    continue
                current_avg.update( self.get_average(component, value, i) )
            self.running_average.append(current_avg)

    def plot_running_average_error(self):
        cell_error = []
        for i in range( 0, self.end - self.start -2):
            for component, value in self.running_average_error[i].items():
                if ("cell_" in component):
                    cell_error.append( self.running_average_error[i][component]["power"]["total"] )  
        plt.figure()
        plt.ylabel('Running average error')
        plt.xlabel('Samples')
        plt.title('Total')
        plt.plot(cell_error)
        plt.savefig('running_total_error')

        cell_error = []
        for i in range( 0, self.end - self.start -2):
            for component, value in self.running_average_error[i].items():
                if ("cell_" in component):
                    cell_error.append( self.running_average_error[i][component]["power"]["internal"] )  

        plt.figure()
        plt.plot(cell_error)
        plt.savefig('running_internal_error')

        cell_error = []
        for i in range( 0, self.end - self.start -2):
            for component, value in self.running_average_error[i].items():
                if ("cell_" in component):
                    cell_error.append( self.running_average_error[i][component]["power"]["switching"] )  

        plt.figure()
        plt.ylabel('Running average error')
        plt.xlabel('Samples')
        plt.title('Switching')
        plt.plot(cell_error)
        plt.savefig('running_switching_error')

        cell_error = []
        for i in range( 0, self.end - self.start -2):
            for component, value in self.running_average_error[i].items():
                if ("cell_" in component):
                    cell_error.append( self.running_average_error[i][component]["power"]["leakage"] )

        plt.figure()
        plt.ylabel('Running average error')
        plt.xlabel('Samples')
        plt.title('Leakage')
        plt.plot(cell_error)
        plt.savefig('running_leakage_error')
