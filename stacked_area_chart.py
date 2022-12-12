import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

BLUE_COLORS_DIAG = ['#397F64', '#3EAEB2',
                    '#39B4E5', '#0C88FC', '#0A47CC', '#081DA5']
RED_COLORS_DIAG = ['#7F6339', '#B2743E',
                   '#E57B39', '#FC540C', '#CC300A', '#A50808']
BLUE_COLORS_ALT = ['#397D7F', '#3E91B2',
                   '#39DFE5', '#0CB8FC', '#0AC5CC', '#0879A5']
RED_COLORS_ALT = ['#7F6339', '#B2743E',
                  '#E57B39', '#FC540C', '#CC300A', '#A50808']


def make_stacked_area_chart(values):
    data = pd.DataFrame(values, index=range(1, 41))
    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)
    # Make the plot
    data_2d_aray = []
    labels = []
    for col in data.columns:
        data_2d_aray.append(data_perc[col])
        labels.append(col)
    BLUE_COLORS_DIAG.reverse()
    colors = BLUE_COLORS_DIAG + RED_COLORS_DIAG
    plt.stackplot(range(1, 41),  data_2d_aray, labels=labels, colors=colors)
    plt.figlegend(loc='upper left')
    plt.margins(0, 0)
    plt.title('UNC vs IU @ Assembly Hall 11/30/2022') # TODO make this dynamically
    plt.show()
