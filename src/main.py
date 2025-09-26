import logging
import sys, os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("log/app.log", encoding="utf-8")
    ]
)

if __name__ == "__main__":
    from logging import info
    info("Abobabebebe")
    print("nolog")
