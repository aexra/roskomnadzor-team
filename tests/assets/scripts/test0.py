import os, time
pid = os.fork()
if pid == 0:
    os._exit(0)
else:
    time.sleep(60)
