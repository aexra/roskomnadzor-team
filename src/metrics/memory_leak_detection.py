import sys
from logging import info, warning, error

def analyze_metrics(metrics):
    statm = metrics.get('statm', {})
    if 'resident' in statm:
        resident_kb = statm['resident'] * 4
        if resident_kb > 1024 * 1024:
            warning("Проблема: Утечка памяти обнаружена. Рекомендации: Ограничьте память процесса в /etc/security/limits.conf (например, * soft rss 1024000). Настройте систему на строгую работу с памятью: echo \"vm.overcommit_memory=1\" >> /etc/sysctl.conf && sysctl -p. Следите за памятью: smem или pmap -x <pid>.")
        else:
            info("Проблема: Утечка памяти не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python memory_leak_detection.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)