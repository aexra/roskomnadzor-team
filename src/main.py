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

def find_pids_by_name(process_name):
    import os
    pids = []
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open(f"/proc/{pid}/comm", "r") as f:
                comm = f.read().strip()
                if comm.lower() == process_name.lower():
                    pids.append(pid)
        except (FileNotFoundError, PermissionError):
            continue
    return pids

def get_pid_by_arg(input_arg):
    try:
        if input_arg.isdigit():
            pid = input_arg
        else:
            pids = find_pids_by_name(input_arg)
            if not pids:
                print(f"Процесс с именем '{input_arg}' не найден.")
                sys.exit(1)
            elif len(pids) > 1:
                print(f"Найдено несколько процессов с именем '{input_arg}':")
                for i, pid in enumerate(pids, 1):
                    try:
                        with open(f"/proc/{pid}/cmdline", "r") as f:
                            cmdline = f.read().replace('\x00', ' ').strip()
                        print(f"{i}. PID: {pid}, Командная строка: {cmdline}")
                    except FileNotFoundError:
                        print(f"{i}. PID: {pid}, Командная строка: недоступна")
                choice = input("Введите номер процесса (1, 2, ...): ")
                if not choice.isdigit() or int(choice) < 1 or int(choice) > len(pids):
                    print("Некорректный выбор.")
                    sys.exit(1)
                pid = pids[int(choice) - 1]
            else:
                pid = pids[0]
        return pid
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <pid>")
        sys.exit(1)
    
    arg = sys.argv[1]
    pid = get_pid_by_arg(arg)
    
    
    
    import metrics
    from metrics import process_metrics
    data = process_metrics.get_process_metrics(pid)
    
    for importer, modname, ispkg in pkgutil.iter_modules(metrics.__path__, metrics.__name__ + "."):
        if modname.endswith(".process_metrics") or modname.endswith(".Metric"):
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
