#!/usr/bin/env python

from __future__ import division

import math
import numpy as np
from pprint import pprint
from collections import Counter


# sum of squares: v1 * v1 + ... + vn * vn
def sum_of_squares(v):
    return np.dot(v, v)

# magniture
def magnitude(v):
    return math.sqrt(sum_of_squares(v))

# distance
def distance(v, w):
    return magnitude(np.subtract(v, w))


# create a matrix
def make_matrix(rows, cols, fn):
    '''returns a rows x cols matrix | entry (i, j) = fn(i, j)'''
    return np.matrix([[fn(i, j)               # create an entry value
                       for j in range(cols)]  # for each col
                       for i in range(rows)]) # create a list for each row

def is_diagonal(i, j):
    '''1's on the diagonal'''
    return 1 if i == j else 0

# variance - how a variable deviates from it's mean
# the avg of the squared difference from the mean -> shows how spread out the data is
def de_mean(x):
    '''translate x's mean to 0'''
    x_bar = x.mean()
    return [x_i - x_bar for x_i in x]

# divide by n for the whole population
# divide by n-1 for a sample of the population,
# to account for a 'correction' -> shows it more spread out
def variance(x):
    '''assumes x has at least 2 elements'''
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

# standard deviation, 68% lies within +- std of the mean
def standard_deviation(x):
    return math.sqrt(variance(x))

# interquartile_range
def interquartile_range(x):
    return np.percentile(x, 75) - np.percentile(x, 25)

# covariance - how two variables vary in tandem from their means
# a larger covariance indicates better correlation (neg * neg, and pos * pos)
# ~ how much each entry pair contributed?
def covariance(x, y):
    n = len(x)
    return np.dot(de_mean(x), de_mean(y)) / (n - 1)

# correlation, ranges from -1 (anti_correlation) to 1 (perfect correlation)
def correlation(x,y):
    #std_x = x.std()
    #std_y = y.std()
    cov = np.cov(x, y)
    std_x = math.sqrt(cov[0, 0])
    std_y = math.sqrt(cov[1, 1])
    if std_x > 0 and std_y > 0:
        #return np.cov(x, y)[0, 1] / std_x / std_y
        return cov[0, 1] / std_x/ std_y
    else: return 0


if __name__ == '__main__':
        # defs
    v = np.array([1, 2, 3])
    w = np.array([4, 5, 6])
    print('v: %s' % v)
    print('w: %s' % w)
    
    # vector add
    print('v + w: %s' % np.add(v, w))
    
    # vector subtract
    print('v - w: %s' % np.subtract(w, v))
    
    # vector sum
    print('sum (v): %s' % np.sum(v))
    
    # scalar multiply
    print('3v: %s' % np.dot(3, v))
    
    # mean, median
    print('mean (v, w): %s' % np.mean([v, w]))
    print('median (v): %s' % np.median(v))
    
    # dot
    print('dot (v, w): %s' % np.dot(v, w))
    
    print('sum of squares (v): %f' % sum_of_squares(v))
    
    print('magnitude (v): %f' % magnitude(v))

    print('distance (v, w): %f' % distance(v, w))
    print('np distance (v, w): %f' % np.linalg.norm(v-w))
    
    print('-' * 40)
    
    # percentile
    print('percentile (v, 50): %f' % np.percentile(v, 50))
    
    # mode (most common values)
    # from scipy import stats
    # print('mode (v):')
    # pprint(stats.mode(v))
    
    # matrices
    A = np.matrix([[1, 2, 3],
                   [4, 5, 6]])
    
    B = np.matrix([[1, 2],
                   [3, 4],
                   [5, 6]])
    print('A:')
    pprint(A)
    print('B:')
    pprint(B)
    
    # shape
    print('shape (A): %s' % (A.shape,))
    
    # get row, col
    print('row (A, 0): %s' % A[0])
    print('col (A, 0):')
    pprint(A[:,0])

    identity_matrix = make_matrix(5, 5, is_diagonal)
    print('identity matrix:')
    pprint(identity_matrix)
    
    print('np identity matrix:')
    pprint(np.identity(5))
    
    print('-' * 40)
    
    # statistics
    v = np.array([100, 25, 
                  20, 18, 17, 17,
                  5, 5, 5, 4, 4, 4, 4, 4,
                  3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1])
    print('v: %s' % v)
    
    # range
    print('range (v): %s' % v.ptp(axis=0))
    print('range (A, 0): %s' % A.ptp(axis=0))
    print('range (A, 1):')
    pprint(A.ptp(axis=1))

    print('variance (v): %f' % variance(v))
    print('np variance (v): %f' % v.var())
    print('np standard deviation (v): %f' % v.std())

    print('interquartile range (v): %f' % interquartile_range(v))

    print('-' * 40)
    
    # correlation
    num_friends = np.array([10, 7, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1])
    daily_minutes = np.array([35, 21, 15, 17, 14, 12, 11, 9, 10, 8, 8, 7, 6, 6, 5, 5, 2])
    print('num_friends: %s' % num_friends)
    print('daily_minutes: %s' % daily_minutes)

    print('covariance: %f' % covariance(num_friends, daily_minutes))
    print('mean (num_friends): %f' % num_friends.mean())
    print('variance (num_friends): %f' % num_friends.var())
    print('stdev (num_friends): %f' % num_friends.std())
    print('mean (daily_minutes): %f' % daily_minutes.mean())
    print('variance (daily_minutes): %f' % daily_minutes.var())
    print('stdev (daily_minutes): %f' % daily_minutes.std())
    print('np covariance:')
    pprint(np.cov(num_friends, daily_minutes))

    print('correlation: %f' % correlation(num_friends, daily_minutes))
