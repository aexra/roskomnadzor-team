import process_metrics as pm

def analyze_metrics(metrics):
    status = metrics.get('status', {})
    vm_stk = int(status.get('VmStk', '0k').split()[0]) if 'VmStk' in status else 0
    if vm_stk > 8192:
        print("Проблема: Риск переполнения стека обнаружен. Рекомендации: Увеличьте лимит стека: ulimit -s 16384 или в /etc/security/limits.conf. Проверьте: grep VmStk /proc/<pid>/status. Избегайте глубокой рекурсии в коде.")
    else:
        print("Проблема: Риск переполнения стека не обнаружен.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python stack_overflow_risk.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)