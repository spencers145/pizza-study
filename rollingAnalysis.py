# custom library
# implements a painless way to generate a rolling-average graph, given a dataframe and some column names

import matplotlib.pyplot as plt
import pandas as pd

def plotRollingData(columns: list[str], data: pd.DataFrame, roll_range: int, direction: str = "center", scales: list[float] = 1, legend = True):
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
            plt.plot(column.index[roll_range:], rolling_avgs[roll_range:], label=column_name)
    else: raise Exception("Invalid range type.")
    if legend: plt.legend()