import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

data = pd.read_csv(r"./GBPCHF_Ticks_10.08.2020-10.08.2020.csv")

data.columns = ["Date", "open", "close", "Ask_vol", "Bid_vol"]

data.Date = pd.to_datetime(data.Date)

data = data.set_index(data.Date)

data = data[["open", "close", "Ask_vol", "Bid_vol"]]

data = data.drop_duplicates(keep=False)

price = data.close.iloc[:10000]

previous_index = np.array([])
cleared = np.array([])

for i in range(0, len(price)):

    max_idx = list(argrelextrema(price.values[:i], np.greater, order=10)[0])
    min_idx = list(argrelextrema(price.values[:i], np.less, order=10)[0])

    idx = max_idx + min_idx + [len(price.values[:i]) - 1]

    idx.sort()

    if len(idx) >= 5:

        current_idx = idx[-5:] # gets 5th from last to last extrema x values as such in idx
        #print(current_idx)
        #print("\n")

        start = min(current_idx)
        end = max(current_idx)

        current_pat = price.values[current_idx] # the corresponding prices values of the extrema

        XA = current_pat[1] - current_pat[0]
        AB = current_pat[2] - current_pat[1]
        BC = current_pat[3] - current_pat[2]
        CD = current_pat[4] - current_pat[3]

        if XA > 0 and AB < 0 and BC > 0 and CD < 0:

            err = 0.1
            ABr = np.array([0.618 - err, 0.618 + err]) * abs(XA)
            BCr = np.array([0.382 - err, 0.886 + err]) * abs(AB)
            CDr = np.array([1.27 - err, 1.618 + err]) * abs(BC)

            if ABr[0] < abs(AB) < ABr[1] and BCr[0] < abs(BC) < BCr[1] and CDr[0] < abs(CD) < CDr[1]:

                plt.plot(np.arange(start, end+100), price.values[start:end+100])
                plt.plot(current_idx, current_pat, c="r")
                plt.show()

