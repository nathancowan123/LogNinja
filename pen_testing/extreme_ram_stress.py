import numpy as np
import time
import psutil
import os

# 🚨 CONFIGURATION
MAX_RAM_PERCENT = 95  # Maximum % of RAM usage before stopping
HOLD_TIME = 10        # Time to hold memory before releasing
CHUNK_SIZE_MB = 200   # Size of each allocated chunk in MB

def get_ram_usage():
    """Returns the current RAM usage percentage."""
    return psutil.virtual_memory().percent

def extreme_ram_stress():
    """Gradually increases RAM usage until the max limit is reached."""
    arrays = []
    print("🚀 Starting extreme RAM stress test...")
    
    try:
        while get_ram_usage() < MAX_RAM_PERCENT:
            chunk_size = (CHUNK_SIZE_MB * 1024 * 1024) // np.dtype(np.float64).itemsize  # Convert MB to NumPy elements
            arrays.append(np.ones(chunk_size, dtype=np.float64))  # Allocate memory
            
            ram_usage = get_ram_usage()
            print(f"🧠 RAM Usage: {ram_usage:.2f}%")

            if ram_usage >= MAX_RAM_PERCENT:
                print(f"🚨 Max RAM limit reached ({MAX_RAM_PERCENT}%)! Holding for {HOLD_TIME} seconds...")
                time.sleep(HOLD_TIME)
                break
            
            time.sleep(1)  # Slow the increase for system stability

    except MemoryError:
        print("💀 OUT OF MEMORY! The system ran out of available RAM.")
    
    finally:
        print("🛑 Releasing memory...")
        arrays.clear()
        time.sleep(3)
        print("✅ Memory successfully released.")

if __name__ == "__main__":
    extreme_ram_stress()
