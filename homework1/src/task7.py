import numpy as np 

#Function for matrix multiplication. 
def matrix_mul(matA=None, matB=None):
    if matA is None:
        matA=np.array([[1, 2], [3, 4]])
    if matB is None:
        matB = np.array([[1, 2], [3, 4]])
    return np.matmul(matA, matB)