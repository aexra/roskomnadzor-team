import process_metrics as pm

def analyze_metrics(metrics):
    status = metrics.get('status', {})
    if 'voluntary_ctxt_switches' in status and int(status['voluntary_ctxt_switches']) > 1000 or 'nonvoluntary_ctxt_switches' in status and int(status['nonvoluntary_ctxt_switches']) > 1000:
        print("Проблема: Частые переключения контекста обнаружены. Рекомендации: Привяжите процесс к ядрам: taskset -c 0-7 <pid>. Включите автогруппы: echo \"kernel.sched_autogroup_enabled=1\" >> /etc/sysctl.conf && sysctl -p. Проверьте: grep ctxt /proc/<pid>/status.")
    else:
        print("Проблема: Частые переключения контекста не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python context_switch_overhead.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)