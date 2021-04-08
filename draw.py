import numpy as np


def circle(a,coord,r,value=1):
  cy,cx = coord
  h,w = a.shape
  for y in range(int(np.round(cy-r)),int(np.round(cy+r))+1):
    if y < 0 or y >= h:
      continue
    l = (r*r-(cy-y)**2)**.5
    img[y,max(0,int(np.round(cx-l))):min(w,int(np.round(cx+l)))] = value


if __name__ == '__main__':
  import matplotlib.pyplot as plt
  Y,X = 480,640
  img = np.zeros((Y,X))
  for i in range(5):
    circle(img,
        (np.random.rand()*Y,np.random.rand()*X),
        np.random.rand()*min(Y,X)/4)
  plt.imshow(img)
  plt.show()
