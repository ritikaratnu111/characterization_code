import sys,os
from create_db import DbGenerator
from energy_calculator import ComposableEnergyEstimator

#logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

#
#    def get_algorithm_predictions(self):
#        try:
#            algorithm_file_path = "../input_files/algorithms.json"
#            with open(tb_file_path) as file:
#                self.algorithms = json.load(file)
#        except FileNotFoundError:
#            print(f"Testbench file '{tb_file_path}' not found.")
#        except Exception as e:
#            print(f"Error loading testbenches: {e}")
#        
#        for name, info in self.algorithms.items():
            

def main():
    
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    
    dbgen = DbGenerator(start, end)
    dbgen.get_fabric()
    dbgen.get_testbenches()
    dbgen.run_randomised_simulations()
    dbgen.get_average()
    dbgen.write_db()
    #job.get_algorithm_predictions()
    ecal = ComposableEnergyEstimator()
    ecal.get_fabric()
    ecal.get_testbenches()
    ecal.get_estimates()
    
    reference = PostLayoutEnergyCalculator(start, end)
    reference.get_fabric()
    reference.get_testbenches()
    reference.get_energy()

    return

if __name__ == "__main__":
    main()
