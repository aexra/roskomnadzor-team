import os
import sys
import pprint

def get_process_metrics(pid):
    proc_dir = f"/proc/{pid}"
    if not os.path.exists(proc_dir):
        raise ValueError(f"Процесс с PID {pid} не найден или /proc недоступен.")

    metrics = {
        'pid': pid,
        'available_files': os.listdir(proc_dir)  # Все файлы/директории в /proc/<pid>/
    }

    # Парсинг /proc/<pid>/stat (основные статусы процесса)
    try:
        with open(f"{proc_dir}/stat", 'r') as f:
            stat_data = f.read().strip().split()
            metrics['stat'] = {
                'comm': stat_data[1][1:-1],  # Имя команды (без скобок)
                'state': stat_data[2],
                'ppid': int(stat_data[3]),
                'pgrp': int(stat_data[4]),
                'session': int(stat_data[5]),
                'tty_nr': int(stat_data[6]),
                'tpgid': int(stat_data[7]),
                'flags': int(stat_data[8]),
                'minflt': int(stat_data[9]),
                'cminflt': int(stat_data[10]),
                'majflt': int(stat_data[11]),
                'cmajflt': int(stat_data[12]),
                'utime': int(stat_data[13]),
                'stime': int(stat_data[14]),
                'cutime': int(stat_data[15]),
                'cstime': int(stat_data[16]),
                'priority': int(stat_data[17]),
                'nice': int(stat_data[18]),
                'num_threads': int(stat_data[19]),
                'itrealvalue': int(stat_data[20]),
                'starttime': int(stat_data[21]),
                'vsize': int(stat_data[22]),
                'rss': int(stat_data[23]),
                'rsslim': int(stat_data[24]),
                'startcode': int(stat_data[25]),
                'endcode': int(stat_data[26]),
                'startstack': int(stat_data[27]),
                'kstkesp': int(stat_data[28]),
                'kstkeip': int(stat_data[29]),
                'signal': int(stat_data[30]),
                'blocked': int(stat_data[31]),
                'sigignore': int(stat_data[32]),
                'sigcatch': int(stat_data[33]),
                'wchan': int(stat_data[34]),
                'nswap': int(stat_data[35]),
                'cnswap': int(stat_data[36]),
                'exit_signal': int(stat_data[37]),
                'processor': int(stat_data[38]),
                'rt_priority': int(stat_data[39]),
                'policy': int(stat_data[40]),
                'delayacct_blkio_ticks': int(stat_data[41]),
                'guest_time': int(stat_data[42]),
                'cguest_time': int(stat_data[43]),
                # Дополнительные поля, если есть (зависит от версии ядра)
            }
    except FileNotFoundError:
        pass

    # Парсинг /proc/<pid>/status (детальный статус, память, группы и т.д.)
    try:
        with open(f"{proc_dir}/status", 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metrics[key.strip()] = value.strip()
    except FileNotFoundError:
        pass

    # Парсинг /proc/<pid>/statm (статистика памяти)
    try:
        with open(f"{proc_dir}/statm", 'r') as f:
            statm_data = f.read().strip().split()
            metrics['statm'] = {
                'size': int(statm_data[0]),      # Общий размер в страницах
                'resident': int(statm_data[1]),  # Резидентная память
                'share': int(statm_data[2]),     # Общая память
                'trs': int(statm_data[3]),       # Text (code)
                'drs': int(statm_data[4]),       # Data + stack
                'lrs': int(statm_data[5]),       # Lib
                'dt': int(statm_data[6]),        # Dirty pages
            }
    except FileNotFoundError:
        pass

    # Парсинг /proc/<pid>/io (I/O статистика)
    try:
        with open(f"{proc_dir}/io", 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metrics[key.strip()] = int(value.strip())
    except FileNotFoundError:
        pass

    # Парсинг /proc/<pid>/limits (лимит ресурсов)
    try:
        with open(f"{proc_dir}/limits", 'r') as f:
            limits = {}
            next(f)  # Пропуск заголовка
            for line in f:
                parts = line.split()
                limit_name = ' '.join(parts[:-3])  # Название лимита
                soft = parts[-3]
                hard = parts[-2]
                units = parts[-1] if len(parts) > 3 else ''
                limits[limit_name] = {'soft': soft, 'hard': hard, 'units': units}
            metrics['limits'] = limits
    except FileNotFoundError:
        pass

    # Дополнительные простые метрики
    try:
        metrics['cmdline'] = open(f"{proc_dir}/cmdline", 'r').read().strip().split('\x00')[:-1]
    except FileNotFoundError:
        pass

    try:
        metrics['num_fds'] = len(os.listdir(f"{proc_dir}/fd"))  # Количество открытых файловых дескрипторов
    except FileNotFoundError:
        pass

    try:
        metrics['num_tasks'] = len(os.listdir(f"{proc_dir}/task"))  # Количество потоков/тасков
    except FileNotFoundError:
        pass

    return metrics

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python process_metrics.py <PID>")
        sys.exit(1)
    
    pid = sys.argv[1]
    try:
        metrics = get_process_metrics(pid)
        pprint.pprint(metrics)
    except Exception as e:
        print(f"Ошибка: {e}")