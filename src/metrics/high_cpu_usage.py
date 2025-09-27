import process_metrics as pm
from logging import info, warning, error

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'utime' in stat and 'stime' in stat and 'starttime' in stat:
        total_cpu_time = stat['utime'] + stat['stime']
        starttime = stat['starttime'] or 1
        cpu_usage_ratio = total_cpu_time / starttime
        if cpu_usage_ratio > 0.8:
            warning("Проблема: Высокая загрузка CPU обнаружена. Рекомендации: Снизьте приоритет процесса: renice +10 -p <pid>. Привяжите процесс к определённым ядрам: taskset -cp 0-3 <pid>. Увеличьте мощность процессора: cpupower frequency-set -g performance. Используйте профиль tuned для оптимизации: tuned-adm profile cpu-partitioning. Проверьте загрузку: pidstat -u -p <pid>.")
        else:
            info("Проблема: Высокая загрузка CPU не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python high_cpu_usage.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)