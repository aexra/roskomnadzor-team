import process_metrics as pm
from logging import info, warning, error

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'num_threads' in stat and stat['num_threads'] > 100:
        warning("Проблема: Проблемы многопоточности обнаружены. Рекомендации: Ограничьте потоки в /etc/security/limits.conf (например, * soft nproc 1024). Привяжите потоки к ядрам: taskset -c 0-7 <pid>. Проверьте: ls /proc/<pid>/task/ | wc -l.")
    else:
        info("Проблема: Проблемы многопоточности не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python thread_concurrency_issue.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)