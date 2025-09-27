import process_metrics as pm
from logging import info, warning, error

def analyze_metrics(metrics):
    stat = metrics.get('stat', {})
    if 'signal' in stat and stat['signal'] > 0 or 'sigcatch' in stat and stat['sigcatch'] > 0:
        warning("Проблема: Перегрузка сигналами обнаружена. Рекомендации: Блокируйте ненужные сигналы в коде приложения. Используйте signalfd для обработки сигналов. Проверьте: grep -E 'Sig(Pnd|Blk|Ign|Cgt)' /proc/<pid>/status.")
    else:
        info("Проблема: Перегрузка сигналами не обнаружена.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error("Использование: python signal_overload.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)