# custom library
# implements a painless way to generate a rolling-average graph, given a dataframe and some column names

import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy

def plotRollingData(columns: list[str], data: pd.DataFrame, roll_range: int, scales: list[float] = 1, direction = "left", legend = True, spline = 0):
    if scales == 1: scales = [1]*len(columns)
    if direction == "center":
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
                while len(rolling_avgs) - spline - step - 1 > 0:
                    for i in range(spline):
                        rolling_avgs.pop(step + 1)
                        popped_indices.append(step * (spline + 1) + i + 1)
                    step += 1
                for i in range(len(rolling_avgs) - step - 2):
                    rolling_avgs.pop(step + 1)
                    popped_indices.append(step * (spline + 1) + i + 1)
                column_index_list = list(column.index)
                popped_indices.reverse()
                for i in popped_indices:
                    column_index_list.pop(i)
                spline_index = numpy.linspace(column.index[0], column.index.max(), 500)
                plt.plot(spline_index, make_interp_spline(column_index_list, rolling_avgs)(spline_index), label=column_name)
            else:
                plt.plot(column.index, rolling_avgs, label=column_name)
    elif direction == "backward" or direction == "left":
        for i in range(0, len(columns)):
            rolling_avgs = [0]*roll_range
            column_name = columns[i]
            column = data[column_name]
            scale = scales[i]
            for j in range(roll_range, len(data)):
                sum, count = 0, 0
                for k in range(max(j - roll_range, 0), j+1):
                    sum += column.iloc[k]*scale
                    count += 1
                rolling_avgs.append(sum/count)
            if spline:
                step = 0
                popped_indices = []
                while len(rolling_avgs) - roll_range - spline - step - 1 > 0:
                    for i in range(spline):
                        rolling_avgs.pop(roll_range + step + 1)
                        popped_indices.append(roll_range + step * (spline + 1) + i + 1)
                    step += 1
                for i in range(len(rolling_avgs) - roll_range - step - 2):
                    rolling_avgs.pop(roll_range + step + 1)
                    popped_indices.append(roll_range + step * (spline + 1) + i + 1)
                column_index_list = list(column.index)
                popped_indices.reverse()
                for i in popped_indices:
                    column_index_list.pop(i)
                spline_index = numpy.linspace(column.index[roll_range], column.index.max(), 500)
                plt.plot(spline_index, make_interp_spline(column_index_list[roll_range:], rolling_avgs[roll_range:])(spline_index), label=column_name)
            else:
                plt.plot(column.index[roll_range:], rolling_avgs[roll_range:], label=column_name)
    else: raise Exception("Invalid range type.")

    if legend: plt.legend()