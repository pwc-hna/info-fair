import sys
from subprocess import Popen, PIPE

def hello(text=None):
    print ("Executing script with input param = "+str(text))
    proc = Popen(["C:\Python36-32\python.exe", "C:\\Work\\python-info-fair-wrapper\\robot\\robotProcess\\ml_named_entity_recognition.py", text], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.wait()
    output, err = proc.communicate()
    rc = proc.returncode
    return str(rc)

