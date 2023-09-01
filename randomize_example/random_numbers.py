import random

def generate_integer_gaussian_numbers(mu, sigma, n):
    """
    Generate n integer random numbers with a Gaussian distribution.

    mu: mean of the distribution
    sigma: standard deviation of the distribution
    n: number of random numbers to generate
    """
    numbers = []
    while len(numbers) < n:
        number = round(random.gauss(mu, sigma))
        numbers.append(number)
    return numbers

# Example usage
mean = 100  # Mean of the distribution
std_dev = 20  # Standard deviation of the distribution
num_samples = 100000  # Number of random numbers to generate

random_numbers = generate_integer_gaussian_numbers(mean, std_dev, num_samples)

# Write numbers to a file
file_path = "random_numbers.txt"
with open(file_path, "w") as file:
    for number in random_numbers:
        file.write(str(number) + "\n")

print(f"Random numbers written to {file_path}.")

