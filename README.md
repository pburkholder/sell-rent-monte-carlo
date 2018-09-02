# Some thoughts on statistical computing, Monte Carlo, and sell/rent

## Context

Our family may be making some decisions down the line, one of them being:
If move, do we rent our current residence or sell it? There's a fairly useful spreadsheet for doing the modelling at:
https://www.journalofaccountancy.com/issues/2005/jun/sellit.html 
by Witmer and Kelley from 2005 Journal of Accountacy.

One of the things that occurred to me as I started to work with that model, though, is that you have to make fairly broad assumptions about: CPI inflation, market performance, rental market trends, real estate performance and so on. How do I prevent wishful thinking from coloring what numbers I use?

For fun, I started at the least useful part, but most interesting working with Monte Carlo simulations.

## Tooling

I did some Googling to determine whether I should work in this R, Julia or Python. I've worked with R, which has me interested in Julia, but in the end I found that a good starting point was to work with Python, thanks to guidance like [Simple Monte Carlo Simulation of Stock Prices with Python](https://www.youtube.com/watch?v=_T0l015ecK4) from [Programming4Finance](https://www.youtube.com/channel/UCwjqNW1QutYpEToYSAlqeDQ) to work. 

Getting Spyder installed on MacOS was a pain. This came in useful: http://engineeringterminal.com/computer-science/tutorials/scipy-setup-macos.html



There are no vim bindings that work for me, and panda_datareader was failing with `cannot import name 'is_list_like' from 'pandas.core.common'`, so I have to import it like this:

```python
import pandas as pd
# workaround until 0.7.0 of pandas_datareader is released.
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
```

so in the end I was able to get the example from Programming4Finance on YouTube to work.

## Neat tricks:

Import Case-Schiller Home Index from FREd:

```python
import datetime as dt
import numpy as np
start = dt.datetime(1987,1,1)
end = dt.datetime(2018,6,1)

homes = web.DataReader('CSUSHPISA', 'fred', start, end)
```

Some notes on DataFrames vs Series:

DataFrame can have multiple keys, and is what's returned by DataReader, even if there's only one key:

```python
homes = web.DataReader('CSUSHPISA', 'fred', start, end) # dataframe
```

Most stats are down on a series, so we can get the singular key with:

```python
homes = web.DataReader('CSUSHPISA', 'fred', start, end)['CSUSHPISA'] # series
```

If we're only interested in the month-over-month percent returns:

```python
homes = web.DataReader(
          'CSUSHPISA', 'fred', start, end
        )['CSUSHPISA'].pct_change() # series of Δs
```

The first element will be a NaN, so we should trim that:
```python
homes = web.DataReader(
          'CSUSHPISA', 'fred', start, end
        )['CSUSHPISA'].pct_change()[1:] # series of Δs, less the first
```

### for this work

The example from Programming4Finance is unrealistic for homes/rents because it uses random values each day, and stock data are nearly random, but home prices are strongly autocorrelated:

```python
homes = web.DataReader(
          'CSUSHPISA', 'fred', start, end
        )['CSUSHPISA'].pct_change()[1:] # series of Δs, less the first
homes_ac=homes.autocorr(1)
```

We see that the autocorrelation is 0.93. Also fun to play with are `lag_plots` and `autocorrelation_plot`:

```
from pandas.plotting import autocorrelation_plot
from pandas.plotting import lag_plot
plt.figure()

data = pd.Series(0.7 * np.random.rand(1000) +  0.3 * np.sin(np.linspace(-9 * np.pi, 9 * np.pi, num=1000)))
plt.plot(data)
autocorrelation_plot(data)
lag_plot(data)
autocorrelation_plot(homes)
lag_plot(homes)
```

## Meaning

What matters for a sell/rent decision is:
- YoY rents: I'd only change rents once/year, so month to month variations don't matter.
- Home prices: I should compute the array of 10-year results across the last 30, and use the lowest 3% or 5% for my conservative estimate.