import multiprocessing
import time
import os

# Configuration
STRESS_DURATION = 60  # Run for 60 seconds
NUM_CORES = multiprocessing.cpu_count()  # Use ALL available CPU cores

def cpu_stress(core_id):
    """
    Max out CPU core with intense calculations.

    Features:
    - Utilizes floating-point calculations to generate sustained CPU load.
    - Runs the stress test for a configurable duration (STRESS_DURATION).
    - Prints real-time updates for each core, tracking execution status.
    """

    start_time = time.time()
    print(f"🔥 Core {core_id} is at max load...")

    while time.time() - start_time < STRESS_DURATION:
        _ = sum(x**0.5 for x in range(10**4))  # Heavier floating-point workload
    
    print(f"✅ Core {core_id} finished after {STRESS_DURATION} seconds.")

if __name__ == "__main__":
    """
    CPU Stress Test Runner

    Features:
    - Detects available CPU cores and runs a process on each core.
    - Spawns multiple worker processes for parallel stress testing.
    - Automatically distributes load across all available CPU cores.
    - Displays test start time, core assignments, and completion status.
    - Ensures all processes run concurrently and finish cleanly.
    """

    print(f"🚀 Starting MAX CPU Stress Test on {NUM_CORES} cores for {STRESS_DURATION} seconds...\n")

    # Create a process for each core
    processes = [multiprocessing.Process(target=cpu_stress, args=(i,)) for i in range(NUM_CORES)]
    
    # Start all processes
    for p in processes:
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    print("\n✅ MAX CPU Stress Test Complete! System should recover now.")
