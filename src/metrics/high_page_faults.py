import process_metrics as pm
from logging import info, warning, error

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'majflt' in stat and stat['majflt'] > 0 or 'minflt' in stat and stat['minflt'] > 1000:
        warning("Проблема: Частые page faults обнаружены. Рекомендации: Увеличьте объём памяти или включите hugepages: echo always > /sys/kernel/mm/transparent_hugepage/enabled. Снизьте использование свопа: echo \"vm.swappiness=10\" >> /etc/sysctl.conf && sysctl -p. Проверьте: ps -o min_flt,maj_flt -p <pid>.")
    else:
        info("Проблема: Частые page faults не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python high_page_faults.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)