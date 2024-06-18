# custom library
# implements (mostly) painless ways to search for correlated quantitative variables among large lists

import pandas as pd
import matplotlib.pyplot as plt
import sklearn as skl
from sklearn import linear_model
import scipy.stats as scistat

def generateScatterplotGrid(data, vars, dotsize=10, fontsize=6):
    var_count = len(vars)
    
    figure, axes = plt.subplots(var_count, var_count)
    figure.dpi = 350
    for x in range(0, var_count):
        for y in range(0, var_count):
            axes[x, y].scatter(data[vars[y]], data[vars[x]], s=dotsize)
            axes[x, y].set_xlabel(vars[y], fontsize=fontsize)
            axes[x, y].set_ylabel(vars[x], fontsize=fontsize)
            axes[x, y].tick_params(labelsize=fontsize)
            axes[x, y].label_outer()

def gridLinearTest(data, vars, cutoff=0):
    redundancy_count = 0
    for x in vars:
        redundancy_adjusted_vars = vars[:redundancy_count]
        for y in redundancy_adjusted_vars:
            model = skl.linear_model.LinearRegression().fit(data[[x]], data[[y]])
            score = skl.metrics.r2_score(data[[y]], model.predict(data[[x]]))
            if score >= cutoff and score != 1.0: print(x + " / " + y + ": " + str(score))
        redundancy_count += 1

def gridSpearmanTest(data, vars, cutoff=0, significance=0.01):
    redundancy_count = 0
    for x in vars:
        redundancy_adjusted_vars = vars[:redundancy_count]
        for y in redundancy_adjusted_vars:
            coeff, p = scistat.spearmanr(data[[x]], data[[y]])
            if p <= significance and (coeff >= cutoff or coeff <= -cutoff) and coeff != 1.0 and coeff != -1: print(x + " / " + y + ": " + str(coeff) + " p: " + str(p))
        redundancy_count += 1