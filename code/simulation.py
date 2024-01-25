import os
import random
import constants

CODE_PATH = '/home/ritika/silago/characterization_code/simulation_scripts/'

class Simulation():

    def trigger_vsim(iter, start, end, per_cycle_flag):
        script = f'{CODE_PATH}/get_activity.do'
        os.system(
            f" ITER={iter} START_TIME={start} END_TIME={end} CLOCK_PERIOD={constants.CLOCK_PERIOD} PER_CYCLE_FLAG={per_cycle_flag} vsim -64 -c -do {script}")

    def trigger_innovus(iter, start, end, per_cycle_flag):
        script = f'{CODE_PATH}/get_power.tcl'
        os.system(
            f" ITER={iter} START_TIME={start} END_TIME={end} CLOCK_PERIOD={constants.CLOCK_PERIOD} PER_CYCLE_FLAG={per_cycle_flag} innovus -stylus -no_gui -files {script}")

    def remove_file(file):
        os.remove(file)

    def generate_randomized_mem_init_files(start,end):
        locations = []
        os.makedirs("mem_init_values", exist_ok=True)
        with open('./mem_init_values.txt', 'r') as f:
            current = 0 
            lines = f.readlines()
            for line in lines:
                address = line.split()[0]
                row = line.split()[1]
                col = line.split()[2]
                locations.append([address, row, col])
                current += 1
        
        for i in range(start,end):
            randomized_filename = "./mem_init_values/mem_init_values_" + str(i) + ".txt"
            with open(randomized_filename, 'w') as f:
                for location in range(len(locations)):
                    address = locations[location][0]
                    row = locations[location][1]
                    col = locations[location][2]
                    value = format(random.getrandbits(256), '0256b')
                    f.write(address + " " + row + " " + col + " " + value + "\n")

    def update_mem_init_file(tb,i):
        tbfile = f"{tb}/testbench_rtl.vhd"
        with open(tbfile, 'r') as f:
            lines = f.readlines()
    
        update_mem_init_file_string = f'          file_open(fstatus, fptr, "./mem_init_values/mem_init_values_{i}.txt", read_mode);\n'
        print(lines[138])
        lines[138] = update_mem_init_file_string
        print(lines[138])


        with open(tbfile, 'w') as f:
            f.writelines(lines)

