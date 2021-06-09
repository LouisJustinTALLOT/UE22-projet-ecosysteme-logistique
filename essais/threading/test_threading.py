#!/usr/bin/python

import threading
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   threading._start_new_thread( print_time, ("Thread-1", 2, ) )
   threading._start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print("Error: unable to start thread")

for i in range(100_000_000):
   pass