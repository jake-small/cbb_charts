import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def make_stackd_area_chart(values):
    # data = pd.DataFrame({'group_A': [1, 4, 6, 8, 9], 'group_B': [
    #                     2, 24, 7, 10, 12], 'group_C': [2, 8, 5, 10, 6], }, index=range(1, 6))
    data = pd.DataFrame(values, index=range(1, 41))

    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)

    # Make the plot
    plt.stackplot(range(1, 6),  data_perc["group_A"],  data_perc["group_B"],
                  data_perc["group_C"], labels=['A', 'B', 'C'])
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.title('100 % stacked area chart')
    plt.show()
