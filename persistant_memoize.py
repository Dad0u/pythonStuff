import pickle


class Memo:
  """
  Allows to save the results of a func to disk

  getter must be deterministic. The file will only be saved after adding
  writecache elements.
  Note that if not using as a context manager, save must be called at
  the end to flush the last cached values
  """
  def __init__(self, savefile, getter, writecache=10):
    self.savefile = savefile
    self.getter = getter
    self.writecache = writecache
    self.cached = 0
    try:
      with open(savefile, 'rb') as f:
        self.d = pickle.load(f)
    except FileNotFoundError:
      self.d = {}

  def get(self, elt):
    if elt not in self.d:
      self.d[elt] = self.getter(elt)
      self.cached += 1
    if self.cached >= self.writecache:
      self.save()
    return self.d[elt]

  def save(self):
    with open(self.savefile, 'wb') as f:
      pickle.dump(self.d, f)
    self.cached = 0

  def __enter__(self):
    return self

  def __exit__(self, etype, evalue, etb):
    self.save()


if __name__ == '__main__':
  def get(i):
    print("Getting", i)
    return 'g'+str(i)

  """
  m = Memo('save.p', get)
  for i in range(15):
    print(m.get(i))
  m.save()
  """

  with Memo('save.p', get) as m:
    for i in range(15):
      print(m.get(i))
