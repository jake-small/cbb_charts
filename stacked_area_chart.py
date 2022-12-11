import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

BLUE_COLORS = ['#397F64', '#3EAEB2',
               '#39B4E5', '#0C88FC', '#0A47CC', '#081DA5']
RED_COLORS = ['#7F6339', '#B2743E',
              '#E57B39', '#FC540C', '#CC300A', '#A50808']
C_COLORS = ['#7F6339', '#B2743E',
            '#E57B39', '#FC540C']


def make_stacked_area_chart(values):
    data = pd.DataFrame(values, index=range(1, 41))
    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)
    # Make the plot
    # plt.stackplot(range(1, 41),  data_perc["home"],  data_perc["away"], labels=[
    #               'Home', 'Away'])
    data_2d_aray = []
    labels = []
    for col in data.columns:
        data_2d_aray.append(data_perc[col])
        labels.append(col)
    colors = BLUE_COLORS.append(RED_COLORS)
    plt.stackplot(range(1, 41),  data_2d_aray, labels=labels, colors=C_COLORS)
    plt.figlegend(loc='upper left')
    plt.margins(0, 0)
    plt.title('100 % stacked area chart')
    plt.show()
