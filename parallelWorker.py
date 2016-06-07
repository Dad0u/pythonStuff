#coding: utf-8
from __future__ import print_function

from multiprocessing import Process,Queue
from Queue import Empty as QE
from threading import Thread

class QueueClearer(Thread):
  """
  Class to empty the worker queue and store it in a list (queues can lock the program when full)
  Allows to get the return values on demand
  """
  def __init__(self, q):
    Thread.__init__(self)
    self.l = []
    self.go = True
    self.q = q

  def run(self):
    while self.go:
      try:
        val = self.q.get(True,1)
        self.l.append(val)
      except QE:
        pass

  def getList(self):
    l = len(self.l)
    ret = []
    for i in range(l):
      ret.append(self.l.pop(0))
    return ret

  def stop(self):
    self.go = False
    


class Worker:
  """
    This class creates multiple processes to execute of fonction asynchronously on large ammount of data. Once started, it waits for data (given with feed(data)), executes the fonction and stores the return value. It can then be recovered with .getRes()
    /!\ For now, order is not necessarily respected in the output !
  """
  def __init__(self,**kwargs):
    self.reslist = []
    self.f = kwargs.get("target",lambda x:x)
    self.N = kwargs.get("N",8)
    self.qOut = Queue()
    self.qIn = Queue()
    self.p = []

    def queuedF(qIn,qOut,f):
      val = 0
      while True:
        try:
          val = qIn.get(True,1)
          if val is None:
            break
          qOut.put(f(val))
        except QE:
          pass
      
    for i in range(self.N):
      self.p.append(Process(target=queuedF,args=(self.qIn,self.qOut,self.f)))

    self.qc = QueueClearer(self.qOut)

  def start(self):
    for i in range(self.N):
      self.p[i].start()
    self.qc.start()

  def feed(self,data):
    self.qIn.put(data)

  def stop(self):
    for i in range(self.N):
      self.qIn.put(None)
    for i in range(self.N):
      self.p[i].join()

    self.qc.stop()
    self.qc.join()
    print("Ended properly :)")
    #print(self.qIn.qsize(),self.qOut.qsize())

  def getRes(self):
    return self.qc.getList()
    


# ============= Example ============

if __name__ == "__main__":

  from time import sleep
  import numpy as np

  def doStuff(arr):
    for i in range(500):
      arr+=.002
      arr-=.002
      arr *= 1.5
      arr /= 1.5
    return arr+148


  w = Worker(target=doStuff)

  for i in range(500):
    w.feed(np.random.random((100,100))) # It is possible to "pre-feed" before starting

  w.start()

  for i in range(500):
    w.feed(np.random.random((100,100)))

  l = w.getRes()
  print(len(l))
  sleep(.5)
  l.extend(w.getRes())
  print(len(l))

  w.stop()
  l.extend(w.getRes())
  print(len(l))
  print(l[0])
