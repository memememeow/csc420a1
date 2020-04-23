import numpy as np
import scipy.linalg as sp
import cv2 as cv


# Q5
def isSeparableFilter(mask):
    u, s, v = np.linalg.svd(mask)

    for i in range(1, s.shape[0]):
        if s[i] > np.finfo(np.float32).eps:
            return False
    print u[:, 0] * np.sqrt(s[0])
    print v[0, :] * np.sqrt(s[0])

    # Check that the product of the vector is equal to the original filter
    print np.multiply(u[:, 0].reshape(3, 1) * np.sqrt(s[0]), v[0, :].reshape(1, 3) * np.sqrt(s[0]))
    return True


if __name__ == '__main__':
    # Test for Q5
    # Separable
    filter1 = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]).astype(np.float)
    filter2 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]).astype(np.float) * (1 / 16.0)
    filter4 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]).astype(np.float) * (1 / 9.0)

    # Not separable
    filter3 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).astype(np.float)

    print filter1
    print isSeparableFilter(filter1)

    print filter2
    print isSeparableFilter(filter2)

    print filter3
    print isSeparableFilter(filter3)

    print filter4
    print isSeparableFilter(filter4)
