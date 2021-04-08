import matplotlib.pyplot as plt
import numpy as np
from time import time


class Plotter:
  def __init__(self,*labels):
    self.labels = labels
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111)
    self.lines = []
    for _ in self.labels:
      self.lines.append(self.ax.plot([], [])[0])
    plt.legend(labels, bbox_to_anchor=(-0.03, 1.02, 1.06, .102), loc=3,
               ncol=len(labels), mode="expand", borderaxespad=1)
    plt.xlabel('time (s)')
    plt.grid()
    self.t0 = time()
    plt.draw()
    plt.pause(.001)

  def plot(self,*args):
    assert len(args) == len(self.labels),"Got an invalid number of args"
    t = time()-self.t0
    for l,y in zip(self.lines,args):
      l.set_xdata(np.append(l.get_xdata(),t))
      l.set_ydata(np.append(l.get_ydata(),y))
    self.ax.relim() # Update the window
    self.ax.autoscale_view(True, True, True)
    self.fig.canvas.draw() # Update the graph
    self.fig.canvas.flush_events()


if __name__ == "__main__":
  from time import sleep
  p = Plotter('square','cube')
  for i in range(15):
    p.plot((i/10)**2,(i/10)**3)
    sleep(.2)
