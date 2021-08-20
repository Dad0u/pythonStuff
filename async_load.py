from multiprocessing import Process, Queue
from time import sleep


class Async_iter(Process):
  """
  Can be used to iterate over a list of objects and apply
  asynchronously a function (like an async map)

  For example to load images to be processed in an other process

  namelist: List of keys

  load: function to call on each key

  length: The number of element to load in advance

  sleep_delay: How long will the process sleep if there no elements are needed
  """
  def __init__(self, namelist, load, length=3, sleep_delay=.1):
    super().__init__()
    self.namelist = namelist
    self.load = load
    self.q = Queue()
    self.length = length
    self.sleep_delay = sleep_delay

  def __iter__(self):
    self.start()
    return self

  def run(self):
    for name in self.namelist:
      while self.q.qsize() >= self.length:
        sleep(self.sleep_delay)
      self.q.put(self.load(name))

  def __next__(self):
    while self.q.qsize() == 0 and self.is_alive():
      sleep(self.sleep_delay)
    if self.q.qsize() > 0:
      return self.q.get()
    raise StopIteration


class Worker(Process):
  """
  Super basic worker, takes data from qin,
  applies func and puts the result in qout

  Will stop if None is received
  """
  def __init__(self, func, qin, qout):
    super().__init__()
    self.func = func
    self.qin = qin
    self.qout = qout

  def run(self):
    while (i := self.qin.get()) is not None:
      self.qout.put(self.func(i))


class Async_iter_parallel(Async_iter):
  """
  Same idea as Async_iter, but this time using multiple loading processes
  in parrallel.

  This is only relevent if the loading times
  are longer than the processing times
  """
  def __init__(self, namelist, load, processes=3, length=3, sleep_delay=.1):
    super().__init__(namelist, load, length, sleep_delay)
    self.np = processes
    self.feed = Queue()

  def run(self):
    self.plist = [Worker(self.load, self.feed, self.q) for _ in range(self.np)]
    for p in self.plist:
      p.start()
    for name in self.namelist:
      while self.q.qsize() >= self.length:
        sleep(self.sleep_delay)
      self.feed.put(name)
    for _ in range(self.np):
      self.feed.put(None)


if __name__ == '__main__':
  from time import time
  """
  Quick demo
  """
  def load_f(name):
    print("Loading", name)
    sleep(2)
    print("finished loading", name)
    return name

  #l = Async_iter(list(range(5)), load_f)
  l = Async_iter_parallel(list(range(5)), load_f)

  t0 = time()
  for i in l:
    print(f"[{time()-t0:.2f}] GOT", i)
    sleep(1.1)
