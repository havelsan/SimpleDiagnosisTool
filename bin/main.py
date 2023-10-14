import os
import time
import threading
import gi
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk , GLib
GLib.threads_init() # Don' forget!
from WorkerThread import WorkerThread
from MainWindow import MainWindow

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()



