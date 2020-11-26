import pickle


def cachedfunc(savefile):
  # Decorator to save the results of a function
  # Allows the result to be loaded instead of re-computed
  # Only for funcs with hashable arguments !
  # Result mut be picklable
  def deco(f):
    def newf(*args):
      args = tuple(args)
      try:
        with open(savefile,'rb') as sf:
          saved = pickle.load(sf)
      except FileNotFoundError:
        saved = {}
      if args not in saved:
        print(f"[cachedfunc] {f.__name__}{args} not found, adding...")
        saved[args] = f(*args)
        with open(savefile,'wb') as sf:
          pickle.dump(saved,sf)
      else:
        print(f"[cachedfunc] Using cached value for {f.__name__}{args}")
      return saved[args]
    return newf
  return deco


if __name__ == '__main__':
  @cachedfunc("testcache.p")
  def myfunc(*args):
    print(f"Calling func with arg {args}")
    return -sum(args)

  print("f(0)=",myfunc(0))
  print("f(1)=",myfunc(1))
  print("f(0)=",myfunc(0))
  
  print("f(0,0)=",myfunc(0,0))
  print("f(1,0)=",myfunc(1,0))
  print("f(0,0)=",myfunc(0,0))
