import subprocess
import os
def StartLogger():
    cPid = os.getpid()
    command_memory ="python memoryLogger.py "+ str(cPid)
    command_cpu ="python cpuLogger.py "+ str(cPid)
    memory_task = ""
    cpu_task = ""
    try:
        memory_task = subprocess.Popen(command_memory, stdout=subprocess.PIPE, shell=True)
        cpu_task = subprocess.Popen(command_cpu, stdout=subprocess.PIPE, shell=True)

    except:
      print("Error while running the logger service")
    
    return memory_task, cpu_task

def EndLogger(memory_task,cpu_task):
    memory_task.kill()
    cpu_task.kill()
