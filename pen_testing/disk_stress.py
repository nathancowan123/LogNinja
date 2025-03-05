import os
import time
import threading

TEMP_DIR = "/tmp/logninja_stresstest"
os.makedirs(TEMP_DIR, exist_ok=True)

def disk_stress(file_num):
    """Continuously write large chunks to simulate heavy disk usage."""
    temp_file = f"{TEMP_DIR}/stress_{file_num}.tmp"
    print(f"📝 Writing to: {temp_file}")  # Debug print

    with open(temp_file, "w") as f:
        for i in range(5000):  # Increased iterations
            f.write("LogNinja Stress Test Data\n" * 100000)  # Bigger writes
            print(f"✅ {temp_file}: Written chunk {i + 1}/500")  # Debug print
            time.sleep(0.01)  # Reduce sleep to make it more aggressive

    # print(f"🗑️ Deleting file: {temp_file}")
    # os.remove(temp_file)

def run_stress_test(threads=5):
    """Launch multiple threads to increase disk usage pressure."""
    thread_list = []
    for i in range(threads):
        thread = threading.Thread(target=disk_stress, args=(i,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()  # Wait for all threads to finish

if __name__ == "__main__":
    run_stress_test(threads=10)  # Increase threads for more pressure
