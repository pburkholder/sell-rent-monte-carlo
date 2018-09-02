#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 21:13:50 2018

@author: peterburkholder
"""


import pandas as pd
# workaround until 0.7.0 of pandas_datareader is released.
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

start = dt.datetime(2017,1,3)
end = dt.datetime(2017,11,20)

# datareader returns a class of pand.core.series, so `std` etc. are included
prices = web.DataReader('AAPL', 'iex', start, end)['close']
returns = prices.pct_change()

last_price = prices[-1]

num_simulations = 1000
num_days = 252
simulation_df = pd.DataFrame()

for x in range(num_simulations):
    count = 0  # each simulation starts at zero
    daily_volatility = returns.std()
    
    # for each simulation, a new series
    price_series = []
    
    # compute a price for day 0 based on the last price
    price = last_price * (1 + np.random.normal(0, daily_volatility))
    
    # append it as item 0 in price series
    price_series.append(price)
    
    for y in range(num_days):
        if count == 251:
            break
        # compute a new prices based on the last one, and append.
        price = price_series[count] * (1 + np.random.normal(0, daily_volatility))
        price_series.append(price)
        count += 1
    
    simulation_df[x] = price_series
    
fig = plt.figure()
fig.suptitle('MC simulation AAPL')
plt.plot(simulation_df)
plt.axhline(y= last_price, color = 'r', linestyle = '-')
plt.xlabel('day')
plt.ylabel('price')
plt.show

aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
np.random.choice(aa_milne_arr, 20, p=[0.8, 0.1, 0.05, 0.05])
np.random.choice(aa_milne_arr, 20)