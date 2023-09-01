import sympy as sp
import json

# Load equations from the JSON file
with open('sympy_example_2.json', 'r') as equations_file:
    equations = json.load(equations_file)

def calculate_time(equation_str, variables):
   
    symbols = {var: sp.symbols(var) for var in variables}

    equation = sp.sympify(equation_str)
    
    values = [(symbols[var], val) for var, val in variables.items()]
    
    result = equation.subs(values)
    print(f"symbols = {symbols}, equation = {equation}, values = {values}, result = {result}")
    return result

def main():
    variables = {
        "offset": 1,
        "wait_values": 2,
        "no_of_hops": 3,
        "no_of_rows": 4
    }

    components = {"sequencer", "noc"}

    for component in components:
        print(f"Component: {component}")
        component_equations = equations["ROUTE"][component]
        start_time = calculate_time(component_equations["start_time"], variables)
        print(f"Start time: {start_time}")
        end_time = calculate_time(component_equations["end_time"], variables)
        print(f"End time: {end_time}")

if __name__ == "__main__":
    main()
