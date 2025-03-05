import multiprocessing
import time
import os

# Configuration
STRESS_DURATION = 30  # Duration of stress test in seconds
NUM_CORES = max(1, multiprocessing.cpu_count() - 1)  # Use all but one core

def cpu_stress(core_id):
    """Simulate CPU load with controlled execution and logging."""
    start_time = time.time()
    while time.time() - start_time < STRESS_DURATION:
        _ = sum(x**0.5 for x in range(10**6))  # Floating-point operation for real workload
        if core_id == 0:  # Log only from one core to avoid log spam
            elapsed = round(time.time() - start_time, 2)
            print(f"Core {core_id}: CPU Load Running... ({elapsed}s elapsed)")
        time.sleep(0.1)  # Let the system breathe

if __name__ == "__main__":
    print(f"Starting CPU Stress Test on {NUM_CORES} cores for {STRESS_DURATION} seconds...\n")
    processes = [multiprocessing.Process(target=cpu_stress, args=(i,)) for i in range(NUM_CORES)]
    
    for p in processes: p.start()
    for p in processes: p.join()

    print("\n✅ CPU Stress Test Complete!")
