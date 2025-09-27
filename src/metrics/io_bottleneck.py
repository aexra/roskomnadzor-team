import process_metrics as pm

def analyze_metrics(metrics):
    io_data = {k: v for k, v in metrics.items() if k in ['rchar', 'wchar', 'read_bytes', 'write_bytes']}
    if 'read_bytes' in io_data and 'write_bytes' in io_data:
        io_read_gb = io_data['read_bytes'] / (1024**3)
        io_write_gb = io_data['write_bytes'] / (1024**3)
        if io_read_gb > 1 or io_write_gb > 1:
            print("Проблема: Bottleneck ввода-вывода обнаружен. Рекомендации: Установите быстрый планировщик диска: echo mq-deadline > /sys/block/<disk>/queue/scheduler. Увеличьте буфер чтения: blockdev --setra 8192 /dev/<disk>. Оптимизируйте запись на диск: echo \"vm.dirty_ratio=20\" >> /etc/sysctl.conf && sysctl -p. Используйте SSD; следите с iostat или iotop.")
        else:
            print("Проблема: Bottleneck ввода-вывода не обнаружен.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python io_bottleneck.py <PID или имя процесса>")
        sys.exit(1)
    input_arg = sys.argv[1]
    pid = input_arg if input_arg.isdigit() else pm.find_pid_by_name(input_arg)[0]
    metrics = pm.get_process_metrics(pid)
    analyze_metrics(metrics)