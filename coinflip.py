#!/usr/bin/env python

from __future__ import division
import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
from pprint import pprint


xs = np.array([x / 10.0 for x in range(-50, 50)])
pprint(xs)
mean = xs.mean()
std = xs.std()
print('mean: %f' % mean)
print('std: %f' % std)

pt = mean# + std
cdf = norm.cdf(pt, loc=mean)   # gets the probability (percent) that a random var <= pt
ppf = norm.ppf(cdf, loc=mean)  # gets the pt where the probability is the cdf

print('pt: %f' % pt)
print('cdf: %f as (percentage / 100)' % cdf)
print('ppf: %f as pt' % ppf)

print('')
print('-' * 40)
print('')


def norm_approx_to_binomial(n, p):
    '''finds mu and sigma corresponding to a binomial(n, p)'''
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


norm_prob_below = norm.cdf

def norm_prob_above(lo, mu=0, sigma=1):
    return 1 - norm_prob_below(lo, mu, sigma)

def norm_prob_between(lo, hi, mu=0, sigma=1):
    return norm_prob_below(hi, mu, sigma) - norm_prob_below(lo, mu, sigma)

def norm_prob_outside(lo, hi, mu=0, sigma=1):
    return 1 - norm_prob_between(lo, hi, mu, sigma)

def norm_upper_bound(prob, mu=0, sigma=1):
    '''returns the z for which P(Z <= z)'''
    return norm.ppf(prob, mu, sigma)

def norm_lower_bound(prob, mu=0, sigma=1):
    '''returns the z for which P(Z >= z)'''
    return norm.ppf(1 - prob, mu, sigma)

def norm_two_sided_bounds(prob, mu=0, sigma=1):
    '''returns the symmetric bounds (about the mean)
       that contains the probability'''
    tail_prob = (1 - prob) / 2

    # upper bound should have the tail_prob above it
    upper_bound = norm_lower_bound(tail_prob, mu, sigma)
    
    # lower bound should have the tail_prob below it
    lower_bound = norm_upper_bound(tail_prob, mu, sigma)

    return lower_bound, upper_bound


mu_0, sigma_0 = norm_approx_to_binomial(1000, 0.5)
print('samples: %d' % 1000)
print('prob: %f' % 0.5)
print('mu: %f, sigma: %f' % (mu_0, sigma_0))

# decide what is significant -> 5% chance of a false positive
lo, hi = norm_two_sided_bounds(.95, mu_0, sigma_0)
print('.95 around mean: %f, %f' % (lo, hi))

def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is what's less than x
        return 2 * normal_probability_below(x, mu, sigma)
