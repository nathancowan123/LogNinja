import psutil
import subprocess

def get_cpu_info():
    """Retrieve detailed CPU information."""
    try:
        cpu_model = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split(":")[1].strip()
        cpu_scaling_mhz = subprocess.check_output("lscpu | grep 'CPU(s) scaling MHz'", shell=True).decode().strip().split(":")[1].strip()
        numa_nodes = subprocess.check_output("lscpu | grep 'NUMA node0 CPU(s)'", shell=True).decode().strip().split(":")[1].strip()
        online_cpus = subprocess.check_output("lscpu | grep 'On-line CPU(s) list'", shell=True).decode().strip().split(":")[1].strip()
    except Exception:
        cpu_model, cpu_scaling_mhz, numa_nodes, online_cpus = "Unknown", "Unknown", "Unknown", "Unknown"

    return {
        "cpu_model": cpu_model,
        "num_physical_cores": psutil.cpu_count(logical=False),
        "num_logical_cores": psutil.cpu_count(logical=True),
        "hyper_threading": psutil.cpu_count(logical=True) > psutil.cpu_count(logical=False),
        "cpu_scaling_mhz": cpu_scaling_mhz,
        "numa_nodes": numa_nodes,
        "online_cpus": online_cpus,
    }
