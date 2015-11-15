#!/usr/bin/env python

from __future__ import division
import math
import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
from pprint import pprint
from collections import Counter
from utils import correlation


def bucketize(point, bucket_size):
    '''floor the point into a bucket'''
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points, bucket_size):
    return Counter(bucketize(point, bucket_size) for point in points)


def plot_histogram(points, bucket_size, title=''):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()


def plot1d():
    random.seed(0)
    
    # uniform between -100 and 100
    uniform = [200 * random.random() - 100 for _ in range(10000)]
    
    # normal distribution with mean 0, standard deviation 57
    normal = [57 * norm.ppf(random.random())
              for _ in range(10000)]
    
    plot_histogram(uniform, 10, "Uniform Histogram")
    plot_histogram(normal, 10, "Normal Histogram")


def random_normal():
    '''returns a random draw from a standard normal distribution'''
    return norm.ppf(random.random())


def plot2d():
    xs = [random_normal() for _ in range(1000)]
    ys1 = [x + random_normal() / 2 for x in xs]
    ys2 = [-x + random_normal() / 2 for x in xs]
    
    print(correlation(xs, ys1))
    print(correlation(xs, ys2))
    
    plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
    plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    plt.title('Very Different Joint Distributions')
    plt.show()


def correlation_matrix(data):
    '''returns the num_columns x num_columns matrix whose (i, j)th entry
    is the correlation between columns i and j of data'''
    
    _, num_columns = data.shape()
    
    def matrix_entry(i, j):
        return correlation(data[:,i], data[:,j])
    
    return make_matrix(num_columns, num_columns, matrix_entry)


def plot_correlation_matrix():
    num_points = 100
    
    def random_row():
        row = [None, None, None, None]
        row[0] = random_normal()
        row[1] = -5 * row[0] + random_normal()
        row[2] = row[0] + row[1] + 5 * random_normal()
        row[3] = 6 if row[2] > -2 else 0
        return row
    
    random.seed(0)
    data = np.matrix([random_row() for _ in range(num_points)])
    _, num_columns = data.shape
    fig, ax = plt.subplots(num_columns, num_columns)
    
    for i in range(num_columns):
        for j in range(num_columns):
            
            # scatter column_j on the x-axis vs column_i on the y-axis
            if i != j: ax[i][j].scatter(data[:,j], data[:,i])
            
            # unless i == j, in which case show the series name
            else: ax[i][j].annotate('series ' + str(i), (0.5, 0.5),
                                    xycoords='axes fraction',
                                    ha='center', va='center')
            
            # then hide axis labels except left and bottom charts
            if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
            if j > 0: ax[i][j].yaxis.set_visible(False)
    
    # fix the bottom right and top left axis labels, which are wrong because
    # their charts only have text in them 
    ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    ax[0][0].set_ylim(ax[0][1].get_ylim())
    
    plt.show()
    
    
if __name__ == '__main__':
    #plot1d()
    #plot2d()
    plot_correlation_matrix()