import sys
from logging import info, warning, error

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'delayacct_blkio_ticks' in stat and stat['delayacct_blkio_ticks'] > 1000:
        warning("Проблема: Задержки планирования обнаружены. Рекомендации: Используйте быстрый планировщик: echo bfq > /sys/block/<disk>/queue/scheduler. Увеличьте приоритет I/O: ionice -c1 -p <pid>. Снизьте задержки: echo \"kernel.sched_latency_ns=10000000\" >> /etc/sysctl.conf && sysctl -p. Проверьте: cat /proc/<pid>/schedstat.")
    else:
        info("Проблема: Задержки планирования не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python scheduling_latency.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)