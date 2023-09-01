# Initial values from the first experiment
x_initial = 2
y_initial = 3
z_initial = 2 * x_initial + 7 * y_initial

# Measurements of z from other experiments, write 100 such measurements
measurements_z = [24.35, 24.98, 24.64, 24.25, 25.53, 24.38, 24.41, 25.08, 25.44, 24.69, 25.43, 24.17, 24.92, 25.64, 24.97, 25.64, 24.75, 25.43, 24.69, 25.38, 24.99, 24.32, 25.60, 24.26, 24.72, 24.55, 24.85, 24.52, 25.57, 24.79, 25.37, 25.29, 24.18, 25.67, 24.38, 24.18, 25.64, 24.28, 24.96, 24.88, 25.64, 25.06, 25.36, 25.60, 25.18, 25.30, 24.52, 25.60, 24.68, 24.47, 24.98, 24.65, 24.40, 25.22, 24.89, 25.29, 24.94, 24.68, 25.36, 25.07, 25.45, 24.81, 24.63, 25.04, 24.83, 25.20, 24.23, 24.63, 24.74, 24.74, 24.40, 24.63, 25.56, 24.51, 25.24, 25.15, 25.42, 24.48, 25.59, 25.48, 25.08, 24.84, 25.26, 25.09, 25.33, 24.50, 25.00, 25.06, 24.80, 25.43, 24.27, 25.03, 25.22, 24.54, 24.42, 24.84, 25.16, 24.46, 25.03, 24.25, 24.56, 25.13, 24.21, 24.35, 25.50, 25.33, 25.21, 24.50]

# Number of iterations for adjustment
num_iterations = 1000

# Range of adjustments for x and y
x_adjustment_range =0.9
y_adjustment_range = 0.5

# Define the allowable ranges for x and y
x_range = [x_initial - x_adjustment_range, x_initial + x_adjustment_range]
y_range = [y_initial - y_adjustment_range, y_initial + y_adjustment_range]

# Iterative adjustment
for _ in range(num_iterations):
    for measured_z in measurements_z:
        deviation = measured_z - z_initial
        
        # Test a range of adjustments for x and y
        for x_adjustment in [x_adjustment_range, -x_adjustment_range]:
            for y_adjustment in [y_adjustment_range, -y_adjustment_range]:
                x_test = x_initial + (x_adjustment / 4.0)
                y_test = y_initial + (y_adjustment / 5.0)
                
                # Check if adjusted x and y are within the allowed ranges
                if x_range[0] <= x_test <= x_range[1] and y_range[0] <= y_test <= y_range[1]:
                    z_test = 4 * x_test + 5 * y_test
                    
                    # Calculate the deviation between the test z and measured z
                    deviation_test = measured_z - z_test
                    
                    # If this adjustment reduces the deviation, update the values
                    if abs(deviation_test) < abs(deviation):
                        x_initial = x_test
                        y_initial = y_test
                        z_initial = z_test
                        deviation = deviation_test

# Final adjusted values of x and y
final_x = x_initial
final_y = y_initial

print(f"Final adjusted x: {final_x}")
print(f"Final adjusted y: {final_y}")

#Print percentage error with measurements_z with the final adjusted values of x and y
for measured_z in measurements_z:
    z_test = 4 * final_x + 5 * final_y
    print(f"Percentage error: {100 * (measured_z - z_test) / measured_z}%")