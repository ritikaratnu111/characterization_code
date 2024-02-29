import os
import json
import logging
import matplotlib.pyplot as plt
JSON_FILE_PATH = '/media/storage1/ritika/characterization_code/json_files/'    

class Predictor():
    def __init__(self, predict_start, predict_end, test_start, test_end):
        self.predict_start = predict_start
        self.predict_end = predict_end
        self.test_start = test_start
        self.test_end = test_end
        self.average_data = json.load(open(f"{JSON_FILE_PATH}/prediction_format.json"))['cell_0_1']
        self.test_data = json.load(open(f"{JSON_FILE_PATH}/prediction_format.json"))['cell_0_1']
        self.error = json.load(open(f"{JSON_FILE_PATH}/prediction_format.json"))['cell_0_1']

    def average_algorithm(self, path, start, end):
        data = json.load(open(f"{JSON_FILE_PATH}/prediction_format.json"))['cell_0_1']
        num_iterations = end - start
        print("Num iterations for training", num_iterations)
        for i in range(start, end):
            file = f"{path}/vcd/iter_{i}.json"
            if os.path.exists(file):
                with open(file, "r") as file:
                    iter_data = json.load(file)
            for component, info in data.items():
                if (component in iter_data):
                    if("cell_" not in component):
                        info['active']['internal']    += iter_data[component]['active']['power']['internal'] / num_iterations
                        info['active']['switching']   += iter_data[component]['active']['power']['switching'] / num_iterations
                        info['active']['leakage']     += iter_data[component]['active']['power']['leakage'] / num_iterations
                        info['active']['total']       += (iter_data[component]['active']['power']['internal'] + iter_data[component]['active']['power']['switching'] + iter_data[component]['active']['power']['leakage']) / num_iterations
                        info['inactive']['internal']  += iter_data[component]['inactive']['power']['internal'] / num_iterations
                        info['inactive']['switching'] += iter_data[component]['inactive']['power']['switching'] / num_iterations
                        info['inactive']['leakage']   += iter_data[component]['inactive']['power']['leakage'] / num_iterations
                        info['active']['total']       += (iter_data[component]['inactive']['power']['internal'] + iter_data[component]['inactive']['power']['switching'] + iter_data[component]['inactive']['power']['leakage']) / num_iterations
                    else:
                        info['internal']    += iter_data[component]['power']['internal'] / num_iterations
                        info['switching']   += iter_data[component]['power']['switching'] / num_iterations
                        info['leakage']     += iter_data[component]['power']['leakage'] / num_iterations
                        info['total']       += (iter_data[component]['power']['internal'] + iter_data[component]['power']['switching'] + iter_data[component]['power']['leakage']) / num_iterations

        return data                    


    def average_algorithms(self, algorithms):
        num_algorithms = len(algorithms)
        print("Num algorithms: ", num_algorithms)
        for algorithm,path in algorithms.items():
            algorithm_data = self.average_algorithm( path, self.predict_start, self.predict_end)
            for component, info in self.average_data.items():
                if("cell_" not in component):
                    info['active']['internal']    += algorithm_data[component]['active']['internal'] / num_algorithms
                    info['active']['switching']   += algorithm_data[component]['active']['switching'] / num_algorithms
                    info['active']['leakage']     += algorithm_data[component]['active']['leakage'] / num_algorithms
                    info['active']['total']       += algorithm_data[component]['active']['total'] / num_algorithms
                    info['inactive']['internal']  += algorithm_data[component]['inactive']['internal'] / num_algorithms
                    info['inactive']['switching'] += algorithm_data[component]['inactive']['switching'] / num_algorithms
                    info['inactive']['leakage']   += algorithm_data[component]['inactive']['leakage'] / num_algorithms
                    info['inactive']['total']     += algorithm_data[component]['inactive']['total'] / num_algorithms
                else:             
                    info['internal']    += algorithm_data[component]['internal'] / num_algorithms
                    info['switching']   += algorithm_data[component]['switching'] / num_algorithms
                    info['leakage']     += algorithm_data[component]['leakage'] / num_algorithms
                    info['total']       += algorithm_data[component]['total'] / num_algorithms

    def get_power(self,component, data):
        internal  = data["internal"]
        switching = data["switching"]
        leakage   = data["leakage"]
        total = internal + switching + leakage
        return internal, switching, leakage, total

    def test_algorithms(self,algorithms):
        
        num_algorithms = len(algorithms)
        print("Num algorithms: ", num_algorithms)
        for algorithm,path in algorithms.items():
            test_data = self.average_algorithm( path, self.test_start, self.test_end)
            self.error = json.load(open(f"{JSON_FILE_PATH}/prediction_format.json"))['cell_0_1']
            
            for component, info in self.test_data.items():
                if("cell_" not in component):
                    info['active']['internal']    = test_data[component]['active']['internal']     
                    info['active']['switching']   = test_data[component]['active']['switching']    
                    info['active']['leakage']     = test_data[component]['active']['leakage']      
                    info['active']['total']       = test_data[component]['active']['total']        
                    info['inactive']['internal']  = test_data[component]['inactive']['internal']   
                    info['inactive']['switching'] = test_data[component]['inactive']['switching']  
                    info['inactive']['leakage']   = test_data[component]['inactive']['leakage']    
                    info['inactive']['total']     = test_data[component]['inactive']['total']      
                else:             
                    info['internal']    = test_data[component]['internal']     
                    info['switching']   = test_data[component]['switching']    
                    info['leakage']     = test_data[component]['leakage']      
                    info['total']       = test_data[component]['total']        

        
            
            for component, info in self.error.items():
                if(component in self.test_data):
                    if("cell_" not in component):
                        i1, s1, l1, t1 = self.get_power(component, self.average_data[component]['active'])
                        i2, s2, l2, t2 = self.get_power(component, self.test_data[component]['active'])
                        if (max(i1,i2)== 0):
                            info['active']['internal']      = 0
                        else:
                            info['active']['internal']      =  (abs(i1 - i2) / max(i1, i2) ) * 100
                        if (max(s1,s2)== 0):
                            info['active']['switching']     = 0
                        else:
                            info['active']['switching']     = (abs(s1 - s2) / max(s1, s2) ) * 100
                        if (max(l1,l2)== 0):
                            info['active']['leakage']       = 0
                        else:
                            info['active']['leakage']       = (abs(l1 - l2) / max(l1, l2) ) * 100 
                        if (max(t1,t2)== 0):
                            info['active']['total']         = 0
                        else:
                            info['active']['total']         = (abs(t1 - t2) / max(t1, t2) ) * 100 
                
                        i1, s1, l1, t1 = self.get_power(component, self.average_data[component]['inactive'])
                        i2, s2, l2, t2 = self.get_power(component, self.test_data[component]['inactive'])
                        
                        if (max(i1,i2)== 0):
                            info['inactive']['internal']    = 0
                        else:
                            info['inactive']['internal']    =  (abs(i1 - i2) / max(i1, i2) ) * 100
                        if (max(s1,s2)== 0):
                            info['inactive']['switching']   = 0
                        else:
                            info['inactive']['switching']   = (abs(s1 - s2) / max(s1, s2) ) * 100 
                        if (max(l1,l2)== 0):
                            info['inactive']['leakage']     = 0
                        else:
                            info['inactive']['leakage']     = (abs(l1 - l2) / max(l1, l2) ) * 100
                        if (max(t1,t2)== 0):
                            info['inactive']['total']       = 0
                        else:
                            info['inactive']['total']       = (abs(t1 - t2) / max(t1, t2) ) * 100
                    else:

                        i1, s1, l1, t1 = self.get_power(component, self.average_data[component])
                        i2, s2, l2, t2 = self.get_power(component, self.test_data[component])
                    
                        if (max(i1,i2)== 0):
                            info['internal']                = 0
                        else:
                            info['internal']                =  (abs(i1 - i2) / max(i1, i2) ) * 100
                        if (max(s1,s2)== 0):
                            info['switching']               = 0
                        else:
                            info['switching']               = (abs(s1 - s2) / max(s1, s2) ) * 100 
                        if (max(l1,l2)== 0):
                            info['leakage']                 = 0
                        else:
                            info['leakage']                 = (abs(l1 - l2) / max(l1, l2) ) * 100
                        if (max(t1,t2)== 0):
                            info['total']                   = 0
                        else:
                            info['total']                   = (abs(t1 - t2) / max(t1, t2) ) * 100

            logging.info('----------------------------------------------------------------------------------------------')
            logging.info('{:10} {:20} {:20} {:20} {:20}'.format( algorithm, 'internal', 'switching', 'leakage', 'total'))
            logging.info('----------------------------------------------------------------------------------------------')
#            logging.info('     %s %s %s %s', 'Data',
#                '{:4f}'.format(self.test_data['cell_0_1']['power']['internal']).ljust(20),
#                '{:4f}'.format(self.test_data['cell_0_1']['power']['switching']).ljust(20),
#                '{:4f}'.format(self.test_data['cell_0_1']['power']['leakage']).ljust(20))
            logging.info('    %s %s %s %s %s', 'Error',
                '{:4f}'.format(self.error['cell_0_1']['internal']).ljust(20),
                '{:4f}'.format(self.error['cell_0_1']['switching']).ljust(20),
                '{:4f}'.format(self.error['cell_0_1']['leakage']).ljust(20),
                '{:4f}'.format(self.error['cell_0_1']['total']).ljust(20))
