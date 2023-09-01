#Write python code that will cd into the testbench directory, read the mem_init_values.txt file and generate similar random mem_init_values_i.txt files inside a mem_init_values dircetory in the testbench directory.
import os
import sys
import random

TB_DIR_FILE = "../files/TB_DIR_FILE.txt"

location = []

def generate_random_256bit_value():
    random_value = random.getrandbits(256)
    binary_value = format(random_value, '0256b')
    return binary_value

def get_address_locations():
    with open('./mem_init_values.txt', 'r') as f:
        current = 0
        lines = f.readlines()
        for line in lines:
            address = line.split()[0]
            row = line.split()[1]
            col = line.split()[2]
            location.append([address, row, col])
            current += 1

def write_to_file(file_name):
    with open(file_name, 'w') as f:
        for i in range(len(location)):
            f.write(location[i][0] + " " + location[i][1] + " " + location[i][2] + " " + generate_random_256bit_value() + "\n")


with open(TB_DIR_FILE) as fp:
    Lines = fp.readlines()
    for line in Lines:
        tb = line.strip()
        os.chdir(tb)
        get_address_locations()
        for i in range(700,750):
            write_to_file("./mem_init_values/mem_init_values_" + str(i) + ".txt")
