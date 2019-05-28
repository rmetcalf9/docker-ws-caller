
import os
import time
import subprocess
import signal

import threading

class subThread(threading.Thread):
  jobCmd = None
  timeout = None
  retVal = None
  def __init__(self, jobCmd, timeout):
    self.jobCmd = jobCmd
    self.timeout = timeout
    self.retVal = None
    super(subThread, self).__init__()
    
  def run(self):
    self.retVal = executeCommandINTERNAL(self.jobCmd, self.timeout)

def executeCommand(jobCmd, timeout):
  st = subThread(jobCmd, timeout)
  st.start()
  st.join()
  return st.retVal

def preexecfn():
  os.setsid() #prevent killing process from killing server

#Function to execute the command. Passed the shell string and outputs the executed result
def executeCommandINTERNAL(jobCmd, timeout):
  # https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess

  job_env = dict()
  job_env = os.environ.copy()
  ##job_env["DOCKJOB_JOB_GUID"] = jobExecutionObj.jobGUID

  start_time = time.time()
  proc = subprocess.Popen(
    jobCmd, 
    stdin=None, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT, 
    shell=True, 
    cwd=None, 
    preexec_fn=preexecfn, #self.getDemoteFunction(), 
    env=job_env
  )
  returncode = None
  while (returncode == None):
    time.sleep(0.2)

    returncode = proc.poll()
    #print("Timeout Check:", (time.time() - start_time))
    if (time.time() - start_time) > timeout:
      os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
      ###proc.terminate()
      
'''
The above gives this error
........................Exception in thread Thread-47:
Traceback (most recent call last):
  File "/usr/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/home/robert/otherGIT/docker-ws-caller/test/executor.py", line 20, in run
    self.retVal = executeCommandINTERNAL(self.jobCmd, self.timeout)
  File "/home/robert/otherGIT/docker-ws-caller/test/executor.py", line 57, in executeCommandINTERNAL
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
ProcessLookupError: [Errno 3] No such process
'''
      
      #valid return codes are between 0-255. I have hijacked -1 for timeout
      returncode = -1
  stdout = None
  stderr = None
  if returncode != -1:
    stdout, stderr = proc.communicate()
  completed = subprocess.CompletedProcess(
    args=jobCmd,
    returncode=returncode,
    stdout=stdout,
    stderr=stderr,
  )
  return completed
