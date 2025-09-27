import logging
import sys, os
from metrics import process_metrics, \
    fd_leak, \
    high_cpu_usage, \
    high_page_faults, \
    io_bottleneck, \
    library_memory_usage, \
    memory_leak_detection, \
    memory_overcommit, \
    priority_inversion, \
    resource_limits_hit, \
    scheduling_latency, \
    signal_overload, \
    stack_overflow_risk, \
    thread_concurrency_issue, \
    zombie_processes
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"log/{timestamp}.log"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_filename, encoding="utf-8")
    ]
)

if __name__ == "__main__":
    pid = sys.argv[1]
    metrics = process_metrics.get_process_metrics(pid)
    for metric in [
        fd_leak,
        high_cpu_usage,
        high_page_faults,
        io_bottleneck,
        library_memory_usage,
        memory_leak_detection,
        memory_overcommit,
        priority_inversion,
        # resource_limits_hit,
        scheduling_latency,
        signal_overload,
        stack_overflow_risk,
        thread_concurrency_issue,
        zombie_processes
    ]:
        metric.analyze_metrics(metrics)
