# custom library
# implements a painless way to generate a rolling-average graph, given a dataframe and some column names

import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy

def plotRollingData(columns: list[str], data: pd.DataFrame, roll_range: int, scales: list[float] = 1, legend = True, spline = 0):
    if scales == 1: scales = [1]*len(columns)
    for i in range(0, len(columns)):
        rolling_avgs = []
        column_name = columns[i]
        column = data[column_name]
        scale = scales[i]
        for j in range(0, len(data)):
            sum, count = 0, 0
            for k in range(max(j - roll_range, 0), min(j + roll_range + 1, len(data))):
                sum += column.iloc[k]*scale
                count += 1
            rolling_avgs.append(sum/count)
        if spline:
            step = 0
            popped_indices = []
            # remove every {spline}nth entry to facilitate smoothing
            # information loss is acceptable because this is a rolling average
            while len(rolling_avgs) - spline - step > 0:
                for i in range(spline):
                    rolling_avgs[step] = (rolling_avgs[step] + rolling_avgs.pop(step + 1))/2
                    popped_indices.append(step * (spline + 1) + i + 1)
                step += 1
            column_index_list = list(column.index)
            popped_indices.reverse()
            for i in popped_indices:
                column_index_list.pop(i)
            spline_index = numpy.linspace(column.index.min(), column.index.max(), 500)
            plt.plot(spline_index, make_interp_spline(column_index_list, rolling_avgs)(spline_index), label=column_name)
        else:
            plt.plot(column.index, rolling_avgs, label=column_name)
    if legend: plt.legend()