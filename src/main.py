import logging
import sys, os
from datetime import datetime

from metric.process_metrics import get_process_metrics

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
    get_process_metrics(pid)
