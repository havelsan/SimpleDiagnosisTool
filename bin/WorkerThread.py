import os
import time
import threading
import gi
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk , GLib
GLib.threads_init() # Don' forget!


class WorkerThread(threading.Thread):
    def __init__(self, callback,diagnose):
        threading.Thread.__init__(self)
        self.diagnostic_tool_home=os.getenv("DIAGNOSTIC_TOOL_HOME")
        self.callback = callback
        self.diagnose = diagnose
        self.exit_code=1
        self.msg=""
        self.daemon = True

    def run(self):
        # Simulate a long process, do your actual work here
        process=subprocess.Popen([self.diagnostic_tool_home+"/lib/"+self.diagnose+"/run.sh"],stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.exit_code = process.wait()
        #outputOfTheProcess=p.stdout.read().strip().decode('ascii')
        self.msg=stdout.strip().decode('utf-8')
        # The callback runs a GUI task, so wrap it!
        print(self.msg, self.exit_code)
        GLib.idle_add(self.callback,self.diagnose,self.exit_code,self.msg)



