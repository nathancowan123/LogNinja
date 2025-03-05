workers = 2
threads = 2
timeout = 30
preload_app = True
worker_class = "sync"  # 👈 Change this from "gthread" to "sync"

def on_starting(server):
    from app.services.system_monitor import run_system_monitor
    import multiprocessing
    monitor_process = multiprocessing.Process(target=run_system_monitor, daemon=True)
    monitor_process.start()
    server.log.info("🚀 System Monitor Process Started in Gunicorn Master")
