import psutil
import time
import os
import sys
import string

def StartMonitoring(pid):
        process = psutil.Process(int(pid))
        rNumber = int(time.time())
        filename = "/home/maher/Desktop/memory and cpu logs/cpu/logs.txt"
        print("CPU Logger Start\n")
        print("Result File: " + filename)
        
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        for index in range(1,360000):
            f=open(filename, "a+")
            message = str(index) + ", memory_percent: "+ str(process.memory_percent()) + ", cpu_percent: " + str(psutil.cpu_percent(percpu=False))
            f.write(message+"\n")
            time.sleep(1)

if __name__ == '__main__':
    StartMonitoring(sys.argv[1])
