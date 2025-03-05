import numpy as np
import time

def ram_stress():
    """Gradually increase RAM usage instead of an instant overload."""
    arrays = []
    for _ in range(5):  # Creates smaller chunks instead of one massive block
        arrays.append(np.ones((1000, 1000, 10)))  # 80MB per iteration
        time.sleep(2)  # Give the system time to adjust
    time.sleep(5)  # Hold memory for observation

if __name__ == "__main__":
    ram_stress()
