# This script will launch questasim activity simulations and innovus power simulations for each of the generated mem_init_values_i.txt files.
import os
import subprocess
import sys
ACTIVITY_FILE = '/home/ritika/silago/characterization_code/randomised_simulations/get_activity.do'
POWER_FILE = '/home/ritika/silago/characterization_code/randomised_simulations/get_power.tcl'

def update_tb(i):
    #Change the mem_init_values_i.txt file to be used in the testbench_file.vhd
    TBFILE = TB + 'testbench_file.vhd'
    with open(TBFILE, 'r') as f:
        lines = f.readlines()
        new_string = '		file_open(fstatus, fptr, "../mem_init_values/mem_init_values_' + str(i) + '.txt", read_mode);' + '\n'
        lines[144] = new_string
    
    #Write to the testbench_file.vhd
    with open(TBFILE, 'w') as f:
        f.writelines(lines)

def run_questasim_simulations(start_time,end_time,i):
    os.system('ITER=' +str(i) + ' START_TIME=' + str(start_time) + ' END_TIME=' + str(end_time)  + ' vsim -64 -c -do ' + ACTIVITY_FILE)

def run_innovus_simulations(start_time,end_time,i):
    os.system('ITER=' + str(i) + ' START_TIME=' + str(start_time) + ' END_TIME=' + str(end_time) + ' innovus -stylus -no_gui -files ' + POWER_FILE)

TB = sys.argv[1] + '/job1/'
start_time = sys.argv[2]
end_time = sys.argv[3]
start_iter = int(sys.argv[4])
end_iter = int(sys.argv[5])

os.chdir(TB)

for i in range(start_iter,end_iter):
    print(i)
    update_tb(i)
    run_questasim_simulations(start_time,end_time,i)
    run_innovus_simulations(start_time,end_time,i)
    os.system('rm activity_' + str(i) + '.vcd')
