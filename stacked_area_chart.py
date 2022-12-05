import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def make_stackd_area_chart(values):
    data = pd.DataFrame(values, index=range(1, 41))

    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)

    # Make the plot
    plt.stackplot(range(1, 41),  data_perc["home"],  data_perc["away"], labels=[
                  'Home', 'Away'])
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.title('100 % stacked area chart')
    plt.show()
