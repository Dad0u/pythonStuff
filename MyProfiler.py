#coding: utf-8
#Program by Victor Couty (victor@couty.eu)
from __future__ import print_function,division
from time import time

class SerialProfiler:
  """
  A VERY basic profiler using time.time() to query the elapsed time during different stages of a serialized task.
  Does NOT support pausing/restarting or parallel timings on a single instance (self.start() automatically stops the previous step, hence the "serial" profiler)
  Note: it is not meant to be very accurate (time.time() is not precise, especially on Dos systems)
  """
  def __init__(self,name='0'):
    self.tab = [dict(name=name.decode('utf-8'),start=time(),stop=None)]

  def start(self,name=None):
    self.stop()
    if name is None:
      name = str(len(self.time))
    self.tab.append(dict(name=name.decode('utf-8'),start=time(),stop=None))

  def stop(self):
    t = time()
    if self.tab[-1]['stop'] is None:
      self.tab[-1]['stop']=t

  def results(self):
    self.stop()
    #total = (self.tab[-1]['stop']-self.tab[0]['start'])*1000 # Counts time even when no profiler is running
    total = 1000*sum([t['stop']-t['start'] for t in self.tab])
    for i in range(len(self.tab)):
      t = 1000*(self.tab[i]['stop']-self.tab[i]['start'])
      percent = round(t*100/total,2)
      pad = (32-len(self.tab[i]['name']))*'.'+': '
      print(self.tab[i]['name']+pad+str(round(t,3))+" ms ("+str(percent),"%)")
    print("\nTOTAL : "+24*'.'+':',total,"ms.")

class Profile:
  """
  Object representing each timer for ParallelProfiler
  """
  def __init__(self):
    self.running = False
    self.total = 0
    self.t0 = None

  def start(self,stopLast=False):
    if self.running:
      return
    self.running = True
    self.t0 = time()

  def stop(self,t=time()):
    if not self.running:
      return
    self.running = False
    self.total += t-self.t0

class ParallelProfiler:
  """
  A VERY basic profiler using time.time() to query the elapsed time during different stages of a serialized task.
  This version supports pause/restart and parallel timing but may be slightly slower the the serial version
  Note: it is not meant to be very accurate (time.time() is not precise, especially on Dos systems)
  """
  def __init__(self):
    self.dic = dict() # Dict to store id of Profiles by name
    self.tab = [] # list to store the profiles (not using directly the dict because it is not ordered)
    self.n = 0
    self.last = None

  def start(self,name='unnamed',stopLast=False):
    #if StopLast == True, starting this timer will pause the previous one (useful for timing each part of a loop without stopping every timer before starting the next one)
    if stopLast:
      t=time()
      name = name.decode('utf-8')
      try:
        self.tab[self.last].stop(t)
      except TypeError: #If self.last=None
        pass
    try:
      uid = self.dic[name]
      self.tab[uid].start()
    except KeyError:
      self.dic[name] = self.n
      uid = self.n
      self.n += 1
      self.tab.append(Profile())
      self.tab[uid].start()
    self.last = uid

  def stop(self,name='unnamed'):
    t = time()
    self.tab[self.dic[name.decode('utf-8')]].stop(t)

  def results(self):
    t_end = time()
    for p in range(self.n):
      self.tab[p].stop(t_end)
      name = self.__getName(p)
      pad = "."*(30-len(name))+": "
      t = str(round(1000*self.tab[p].total,3))+" ms."
      print(name+pad+t)

  def __getName(self,uid):
    for key,val in self.dic.items():
      if val == uid:
        return key

#Example of usage for Parallel
if __name__ == '__main__':
  from time import sleep
  prof = ParallelProfiler()
  prof.start("Whole loop")
  for i in range(10):
    prof.start("Sleeping .12 seconds")
    sleep(.12)
    prof.start("Looping on 1000000 elements",True) # Stops "Sleeping .12 seconds"
    a = 0
    for i in xrange(1000000):
      a+=i
    prof.stop("Looping on 1000000 elements")
    #Doing unprofiled stuff
    sleep(.05)
    prof.start("Lowering a string 100000 times")
    for i in range(100000):
      a = 'YoLOoLolooLoLLO'.lower()
    prof.stop("Lowering a string 100000 times")
  prof.results() # Automatically stops all running timers (here it stops "Whole loop")

  print("\n############\n")

#Example of usage for Serial
  prof = SerialProfiler("Sleeping .12 seconds") # The profiler starts when instanciated, so it can take the name of the 1st task as argument
  #prof.start("Sleeping .12 seconds")
  sleep(.12)
  prof.start("Looping on 1000000 elements")
  a = 0
  for i in xrange(1000000):
    a+=i
  prof.stop()
  #Doing unprofiled stuff
  sleep(.05)
  prof.start("Lowering a string 100000 times")
  for i in range(100000):
    a = 'YoLOoLolooLoLLO'.lower()
  #prof.stop() #Not necessary
  prof.results()
