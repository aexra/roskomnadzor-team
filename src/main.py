import logging
import sys
from datetime import datetime
import pkgutil
import importlib

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
    if len(sys.argv) != 2:
        print("Usage: python main.py <pid>")
        sys.exit(1)
    
    pid = sys.argv[1]
    
    import metrics
    from metrics import process_metrics
    data = process_metrics.get_process_metrics(pid)
    
    for importer, modname, ispkg in pkgutil.iter_modules(metrics.__path__, metrics.__name__ + "."):
        if modname.endswith(".process_metrics"):
            continue

        try:
            module = importlib.import_module(modname)
            
            if hasattr(module, "analyze_metrics"):
                logging.info(f"Running analysis from {modname}")
                module.analyze_metrics(data)
            else:
                logging.debug(f"Module {modname} has no 'analyze_metrics' function — skipping")
        except Exception as e:
            logging.error(f"Failed to import or run {modname}: {e}")
