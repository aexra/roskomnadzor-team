import logging
import sys, os
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"log/{datetime.now()}.log", encoding="utf-8")
    ]
)

if __name__ == "__main__":
    pass
