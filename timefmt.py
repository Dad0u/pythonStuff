#!/bin/python
#coding: utf-8


def format_time(t):
  i = int(t)
  s = i%60
  i //= 60
  m = i%60
  i //= 60
  h = i%24
  d = i//24
  if d:
    return "{} days {:02d}:{:02d}:{:02d}".format(d,h,m,s)
  elif h:
    return "{:02d}:{:02d}:{:02d}".format(h,m,s)
  elif m:
    return "{:02d}:{:02d}".format(m,s)
  else:
    frac = "{:.3f}".format(t-i)[2:]
    return "{:02d}.{}s".format(s,frac)
