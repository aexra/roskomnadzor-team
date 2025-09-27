import process_metrics as pm

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'state' in stat and stat['state'] == 'Z':
        print("Проблема: Зомби-процессы обнаружены. Рекомендации: Исправьте код приложения, чтобы вызывать waitpid() для дочерних процессов. Убейте родителя: kill -9 <ppid>. Проверьте: ps aux | grep Z.")
    else:
        print("Проблема: Зомби-процессы не обнаружены.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python zombie_processes.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)