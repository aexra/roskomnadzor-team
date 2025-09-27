import process_metrics as pm

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'nice' in stat and stat['nice'] > 10:
        print("Проблема: Инверсия приоритетов обнаружена. Рекомендации: Повысьте приоритет: renice -n -10 -p <pid> или chrt -f 50 <pid> для реального времени. Проверьте: ps -o pri,ni -p <pid>.")
    else:
        print("Проблема: Инверсия приоритетов не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python priority_inversion.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)