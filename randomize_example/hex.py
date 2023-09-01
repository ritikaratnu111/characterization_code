import random

# Define the number of values to select
num_values = 16

# Read the file and store the numbers in a list
with open('file.txt', 'r') as file:
    numbers = [int(line.strip()) for line in file]

# Select 16 random numbers from the list
selected_numbers = random.sample(numbers, num_values)

# Convert each number to 16-bit hexadecimal format and concatenate them
hex_string = ''.join(format(number, '04x') for number in selected_numbers)

# Convert each number to binary format and concatenate them
binary_string = ''.join(format(number, '016b') for number in selected_numbers)

# Print the resulting strings
print(hex_string)
print(binary_string)
