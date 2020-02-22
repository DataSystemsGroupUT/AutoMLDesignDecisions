from memory_profiler import memory_usage
import time
import os
import sys
import string


if __name__ == '__main__':

	#cPid = os.getpid() Use this command to get process ID
	#print(cPid)
	
	rNumber = int(time.time())
	
	filename = "/home/maher/Desktop/memory and cpu logs/memory/logs.txt" #directory of log file
	print("Memory Logger Start\n")
	print("Result File: " + filename)
		
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	
	f = open(filename, "a")
	print(os.getpid())
	mem_usage = memory_usage(int(sys.argv[1]), interval=1, timeout=360000, retval=False, stream=f)
