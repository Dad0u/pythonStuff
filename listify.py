#coding: utf-8
from __future__ import print_function

def listify(f):
  """
  Decorator to allow a function to take its args as a list
  """
  def new_f(*args,**kwargs):
    if args and all([isinstance(arg,list) for arg in args]):
      assert len(set([len(arg) for arg in args])) == 1,\
          "[listify decorator] Lists must have the same len"
      r = []
      for a in zip(*args):
        r.append(f(*a,**kwargs))
      return r
    return f(*args,**kwargs)
  return new_f

if __name__ == "__main__":
  @listify
  def afficher(a,b):
    print("["+str(a)+"]",b)

  afficher("header","message")
  afficher(["header1","header2"],["message1","message2"])
