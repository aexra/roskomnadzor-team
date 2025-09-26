import logging
import sys, os
from datetime import datetime

from metric.process_metrics import get_process_metrics

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"log/{datetime.now()}.log", encoding="utf-8")
    ]
)

if __name__ == "__main__":
    pid = sys.argv[1]
    get_process_metrics(pid)
