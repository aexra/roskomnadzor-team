import sys
from logging import info, warning, error

def analyze_metrics(metrics):
    limits = metrics.get('limits', {})
    max_files = int(limits.get('Max open files', {}).get('soft', '1024')) if 'Max open files' in limits else 1024
    if 'num_fds' in metrics and metrics['num_fds'] > 0.8 * max_files:
        warning("Проблема: Утечка файловых дескрипторов обнаружена. Рекомендации: Увеличьте лимит: ulimit -n 65535 или в /etc/security/limits.conf (* hard nofile 65535). Проверьте: ls /proc/<pid>/fd/ | wc -l или lsof -p <pid>. Для systemd: добавьте LimitNOFILE=65535 в unit-файл.")
    else:
        info("Проблема: Утечка файловых дескрипторов не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python fd_leak.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)