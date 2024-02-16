import os, shutil
import random
import constants
import uuid

CODE_PATH = '/media/storage1/ritika/characterization_code/simulation_scripts/'

class Simulation():

    def trigger_vsim(iter, start, end, per_cycle_flag, uid):
        script = f'{CODE_PATH}/get_activity.do'
        os.system(
            f" ITER={iter} START_TIME={start} END_TIME={end} CLOCK_PERIOD={constants.CLOCK_PERIOD} PER_CYCLE_FLAG={per_cycle_flag} UNID={uid} vsim -64 -c -do {script}")

    def trigger_innovus(iter, start, end, per_cycle_flag):
        script = f'{CODE_PATH}/get_power.tcl'
        os.system(
            f" ITER={iter} START_TIME={start} END_TIME={end} CLOCK_PERIOD={constants.CLOCK_PERIOD} PER_CYCLE_FLAG={per_cycle_flag} innovus -stylus -no_gui -files {script}")

    def remove_file(file):
        os.remove(file)

    def remove_dir(dir):
        shutil.rmtree(dir)

    def generate_randomized_mem_init_files(i):
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
        
        randomized_filename = "./mem_init_values/mem_init_values_" + str(i) + ".txt"
        with open(randomized_filename, 'w') as f:
            for location in range(len(locations)):
                address = locations[location][0]
                row = locations[location][1]
                col = locations[location][2]
                # Generate 16 random 16-bit numbers within the range of -100 to 100
                values = [random.randint(-100, 100) for _ in range(16)]
                # Convert each 16-bit number to a binary string with leading zeros
                binary_values = [format(value & 0xFFFF, '016b') for value in values]
                # Concatenate the binary strings to get a 256-bit binary string
                value = ''.join(binary_values)
                f.write(address + " " + row + " " + col + " " + value + "\n")

    def update_mem_init_file(tb,i):
        tbfile = f"{tb}/testbench_rtl.vhd"
        uid = str(uuid.uuid4())
        tbout = f"testbench_rtl_{uid}.vhd"
        tboutfile = f"{tb}/{tbout}"
        with open(tbfile, 'r') as f:
            lines = f.readlines()
        update_mem_init_file_string = f'          file_open(fstatus, fptr, "./mem_init_values/mem_init_values_{i}.txt", read_mode);\n'
        lines[138] = update_mem_init_file_string
        with open(tboutfile, 'w') as f:
            f.writelines(lines)
        return uid   

