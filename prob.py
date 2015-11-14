#!/usr/bin/env python

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm

plot_pdf = True
plot_cdf = True
plot_ppf = True  # inverse cdf - percent point function

# x = std dev
# y = prob
# sigma = 1 -> ~ 68% prob of a random var falling w/i this range
if plot_pdf:
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [norm.pdf(x, scale=1) for x in xs], '-', label='mu=0,sigma=1')
    plt.plot(xs, [norm.pdf(x, scale=2) for x in xs], '--', label='mu=0,sigma=2')
    plt.plot(xs, [norm.pdf(x, scale=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
    plt.plot(xs, [norm.pdf(x, loc=-1) for x in xs], '-.', label='mu=-1,sigma=1')

    plt.legend()
    plt.title('Various Normal pdfs')
    plt.show()

# prob of a random var <= a reference pt
if plot_cdf:
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [norm.cdf(x, scale=1) for x in xs], '-', label='mu=0,sigma=1')
    plt.plot(xs, [norm.cdf(x, scale=2) for x in xs], '--', label='mu=0,sigma=2')
    plt.plot(xs, [norm.cdf(x, scale=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
    plt.plot(xs, [norm.cdf(x, loc=-1) for x in xs], '-.', label='mu=-1,sigma=1')

    plt.legend(loc=4)  # bottom right
    plt.title('Various Normal cdfs')
    plt.show()

if plot_ppf:
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [norm.ppf(x, scale=1) for x in xs], '-', label='mu=0,sigma=1')
    plt.plot(xs, [norm.ppf(x, scale=2) for x in xs], '--', label='mu=0,sigma=2')
    plt.plot(xs, [norm.ppf(x, scale=0.5) for x in xs], ':', label='mu=0,sigma=0.5')
    plt.plot(xs, [norm.ppf(x, loc=-1) for x in xs], '-.', label='mu=-1,sigma=1')

    plt.legend(loc=4)  # bottom right
    plt.title('Various Normal ppfs')
    plt.show()
