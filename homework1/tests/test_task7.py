import numpy as np
import pytest
from src.task7 import matrix_mul

#Default value test
def test_matrix_mul_default():
    result = matrix_mul()

    expected = np.array([[7, 10],
                         [15, 22]])

    assert np.array_equal(result, expected)

#Both matrices are custom   
def test_matrix_mul_custom():
    A = np.array([[2, 0],
                  [1, 2]])

    B = np.array([[1, 3],
                  [4, 0]])

    result = matrix_mul(A, B)

    expected = np.array([[2, 6],
                         [9, 3]])

    assert np.array_equal(result, expected)

#One matrix is default    
def test_matrix_mul_one_default():
    A = np.array([[1, 0],
                  [0, 1]])

    result = matrix_mul(A)

    expected = np.matmul(A, np.array([[1, 2], [3, 4]]))

    assert np.array_equal(result, expected)

#Matrices are incompatible for matrix multiplication
def test_matrix_mul_incompatible_shapes():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])      

    B = np.array([[1, 2],
                  [3, 4]])         

    # 2x3 * 2x2 is invalid 
    with pytest.raises(ValueError):
        matrix_mul(A, B)