import requests
import threading
import time
import random

# ✅ API Endpoints
BASE_URL = "http://localhost:8100/traffic"
RATE_LIMIT_TEST = f"{BASE_URL}/test"
TRIGGER_500_TEST = f"{BASE_URL}/trigger-500"

# ✅ Simulate Rate Limit Attack (Burst Requests)
def stress_test_rate_limit():
    print("🚀 Testing Rate Limiting (10 requests per second)...")
    for i in range(20):  # Exceeds rate limit
        response = requests.get(RATE_LIMIT_TEST)
        print(f"Request {i+1}: {response.status_code} - {response.text}")
        time.sleep(0.05)  # Send requests quickly

# ✅ Simulate 500 Error Attacks
def test_500_error():
    print("💥 Triggering HTTP 500 Errors...")
    for i in range(5):
        response = requests.get(TRIGGER_500_TEST)
        print(f"500 Error Test {i+1}: {response.status_code} - {response.text}")
        time.sleep(1)

# ✅ Simulate Random Unauthorized Access Requests
def random_traffic_test():
    endpoints = ["/admin", "/login", "/api/data", "/unknown"]
    print("🔍 Sending Random Unauthorized Requests...")
    for i in range(10):
        endpoint = random.choice(endpoints)
        url = f"http://localhost:8100{endpoint}"
        response = requests.get(url)
        print(f"Random Request {i+1}: {response.status_code} - {endpoint}")
        time.sleep(0.5)

# ✅ Run All Tests in Threads
if __name__ == "__main__":
    threads = [
        threading.Thread(target=stress_test_rate_limit),
        threading.Thread(target=test_500_error),
        threading.Thread(target=random_traffic_test),
    ]
    
    print("\n🚧 **STARTING WEB TRAFFIC PEN TEST** 🚧\n")
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()

    print("\n✅ **WEB TRAFFIC TEST COMPLETE** ✅\n")
