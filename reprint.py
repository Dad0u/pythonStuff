#coding: utf-8

last_len = None


def reprint(*args):
  global last_len
  s = " ".join([str(i) for i in args])
  s = s.split("\n")[0]
  l = len(s)
  if last_len is not None:
    s+=" "*(last_len-l)
  last_len = l
  print(s,end='\r',flush=True)


if __name__ == "__main__":
  from time import sleep
  for i in range(10):
    sleep(.2)
    reprint(i,"X"*(1+i%3))
  print("\n")
