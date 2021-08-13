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


if __name__ == '__main__':
  """
  Quick demo
  """
  def load_f(name):
    print("Loading", name)
    sleep(.2)
    print("finished loading", name)
    return name

  l = Async_iter(list(range(5)), load_f)

  for i in l:
    print("GOT", i)
    sleep(1)
