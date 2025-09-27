# test_fd_leak.py
import os
files = []
for i in range(2000):
    try:
        f = open(f"/tmp/test_{i}.txt", "w")
        files.append(f)
    except:
        break
input("Press Enter to close files...")