import os
import math

def big_function():
    total = 0
    for i in range(100):
        for j in range(100):
            total += i * j
    
    # Using math properly
    sqrt_value = math.sqrt(total)

    # Using os properly
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)

    print("Square Root of Total:", sqrt_value)

    return total