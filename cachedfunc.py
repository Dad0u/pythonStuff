import pickle


def cachedfunc(savefile):
  # Decorator to save the results of a function
  # Allows the result to be loaded instead of re-computed
  # Only for funcs with a single hashable argument
  # Result mut be picklable
  def deco(f):
    def newf(arg):
      try:
        with open(savefile,'rb') as sf:
          saved = pickle.load(sf)
      except FileNotFoundError:
        saved = {}
      if arg not in saved:
        saved[arg] = f(arg)
        with open(savefile,'wb') as sf:
          pickle.dump(saved,sf)
      return saved[arg]
    return newf
  return deco


if __name__ == '__main__':
  @cachedfunc("testcache.p")
  def myfunc(arg):
    print(f"Calling func with arg {arg}")
    return -arg

  print("f(0)=",myfunc(0))
  print("f(1)=",myfunc(1))
  print("f(0)=",myfunc(0))
