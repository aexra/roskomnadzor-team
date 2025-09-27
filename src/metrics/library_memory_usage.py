import process_metrics as pm
from logging import info, warning, error

def analyze_metrics(metrics):
    statm = metrics.get('statm', {})
    if 'trs' in statm and statm['trs'] > 1000:
        warning("Проблема: Память библиотек обнаружена. Рекомендации: Оптимизируйте библиотеки: ldconfig или используйте статическую линковку. Снизьте использование памяти: echo \"vm.overcommit_memory=2\" >> /etc/sysctl.conf && sysctl -p. Проверьте: cat /proc/<pid>/statm | awk '{print $2,$3,$4}'.")
    else:
        info("Проблема: Память библиотек не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python library_memory_usage.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)