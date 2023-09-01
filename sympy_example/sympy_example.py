import sympy as sp

def compute_linear_function(x_val, y_val, z_val):
    # Define the variables as symbolic symbols
    x, y, z = sp.symbols('x y z')
    
    # Define a linear multivariable function
    f = 3*x + 2*y - z
    
    # Define values for x, y, and z
    values = [
        (x, x_val),
        (y, y_val),
        (z, z_val)
    ]
    
    # Compute the function value for the specified variable values
    result = f.subs(values)
    return result

def main():
    x_value = 1
    y_value = 2
    z_value = 3
    
    # Call the function and print the result
    function_result = compute_linear_function(x_value, y_value, z_value)
    print(f"For x = {x_value}, y = {y_value}, z = {z_value}, f(x, y, z) =", function_result)

if __name__ == "__main__":
    main()
