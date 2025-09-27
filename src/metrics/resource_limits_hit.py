import sys
from logging import info, warning, error

def analyze_metrics(metrics):
    limits = metrics.get('limits', {})
    if type(limits['Max processes']['soft']) is str:
        warning("Проблема: Процесс не имеет лимита. Рекомендации: Установите лимиты в /etc/security/limits.conf (например, * soft nproc 65535). Примените: ulimit -u 65535 или prlimit --pid <pid> --nofile=65535:65535. Проверьте: cat /proc/<pid>/limits.")
    elif 'Max processes' in limits and int(limits['Max processes']['soft']) < 1024:
        warning("Проблема: Достигнуты лимиты ресурсов обнаружены. Рекомендации: Увеличьте лимиты в /etc/security/limits.conf (например, * soft nproc 65535). Примените: ulimit -u 65535 или prlimit --pid <pid> --nofile=65535:65535. Проверьте: cat /proc/<pid>/limits.")
    else:
        info("Проблема: Достигнуты лимиты ресурсов не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python resource_limits_hit.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)
