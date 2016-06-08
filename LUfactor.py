#coding: utf-8
from __future__ import print_function,division

import numpy as np
import scipy.linalg as lalg

"""
A program to understand system resolution by LU factorization. It does not permute anything, so it cannot solve every solvable system, it is only for understanding (and it is waaay slower than numpy)
"""


#Takes a matrix M, decomposes it in a product LU of a lower triangular matrix and an upper triangular matrix
def LU(M):
  L = np.identity(size)
  U = M

  for i in range(size):
    for j in range(i+1,size):
      L[j,i] = M[j,i]/M[i,i]
      U[j] = M[j]-L[j,i]*U[i]

  return L,U

# Given the LU decomposition of a matrix, solves (LU)x=b
def LUsolve(L,U,b):
#Solving Lp = b
  p = np.zeros(size)
  for k in range(size):
    r = sum([L[i,k]*p[i] for i in range(k)])
    p[k] = (b[k]-r)/L[k,k]

# And now, Ux = p (equivalent to LUx=b)
  x = np.zeros(size)
  for k in [size-i-1 for i in range(size)]:
    r = sum([U[k,i]*x[i] for i in range(k,size)])
    x[k] = (p[k]-r)/U[k,k]
  return x

def solve(M,b):
  L,U = LU(M)
  return LUsolve(L,U,b)


if __name__ == "__main__":
  size = 50
  M = np.random.rand(size,size)
  print("M:\n",M,"\n\n")
  b = np.random.rand(size)

  x = solve(M,b)
  print("My solution:\n",x,"\n\n")

  x2 = np.linalg.solve(M,b)
  print("Numpy solution:\n",x2)

  print("Success:",np.allclose(x,x2))
