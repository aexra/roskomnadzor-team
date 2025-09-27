import sys
from logging import info, warning, error

def analyze_metrics(metrics):
    status = metrics.get('status', {})
    vm_size = int(status.get('VmSize', '0k').split()[0]) if 'VmSize' in status else 0
    vm_rss = int(status.get('VmRSS', '0k').split()[0]) if 'VmRSS' in status else 0
    if vm_size > 2 * vm_rss:
        warning("Проблема: Проблемы overcommit памяти обнаружены. Рекомендации: Настройте строгую память: echo \"vm.overcommit_memory=2\" >> /etc/sysctl.conf && sysctl -p. Настройте OOM killer: echo 10 > /proc/<pid>/oom_score_adj. Проверьте: grep -E 'VmSize|VmRSS' /proc/<pid>/status.")
    else:
        info("Проблема: Проблемы overcommit памяти не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python memory_overcommit.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)