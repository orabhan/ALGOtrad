from universal.algo import Algo
import numpy as np


class ReversalTrend(Algo):
    PRICE_TYPE = 'log'

    # if true, replace missing values by last values
    REPLACE_MISSING = True

    def __init__(self, m=12, n=26):

        if n <= m:
            raise ValueError('n parameter must be > m')
        # n,m length of exponential moving average
        self.m = m
        self.n = n
        super(ReversalTrend, self).__init__(min_history=n)

    def init_weights(self, columns):
        return pd.Series(np.ones(len(columns)) / len(columns), columns)

    def weights(self, S):
        # Building exponential moving average m on Stock S
        def EMA(m, S):
            S_ewm = S.ewm(span=m, adjust=False).mean()
            return S_ewm

        # calculate exponential moving average m
        ema_m = EMA(self.m, S)

        # calculate exponential moving average n
        ema_n = EMA(self.n, S)

        # calculate exponential moving average (n+m)/2
        ema_mean = EMA(int((self.m + self.n) / 2), S)

        delta_1 = S - ema_n
        delta_2 = S - ema_m

        sum_delta = delta_1 + delta_2

        # Smoothing signal   around th threshold of 0 to detect the beginning of bullishness when stock prices
        # are going accross the zero
        plus = sum_delta.where(sum_delta >= 0, 0)
        moins = sum_delta.where(sum_delta < 0, 0)

        # find the max when all assets are downcreasing and find it by putting 1 and 0 for the rest of dataframe moins
        m = moins.eq(moins.where(moins != 0).max(1), axis=0).astype(int)

        moins = m * moins

        # construct sgn with the the modified moins

        sgn = moins + plus

        # retrieve positive sign corresponding to bullishness of prices or put 1  when all prices are downcreasing for one is downcreasing softly
        w = sgn.apply(np.sign).replace(-1, 0)

        # Compute log_return
        log_return = np.log(S / S.shift(1)).fillna(method='ffill')

        # Calculate the moving standard deviation on asset logreturn with window=mean short term & long term of EMA
        # vol is and indicatrice which determines if all assets are not flat, vol of all assets >1 and we compute the number of  assets concerned by this condition
        vol = (((log_return.rolling(window=int((self.m + self.n) / 2), min_periods=1).std()) > 0.6) * 1).sum(axis=1)

        # if vol of all element < 1 so we retrieve the data of signs of w and of sum_delta above else if we do compute in order to actualize weights
        # disactivate calculus of weights if the vol of all assets at t < to the mean of median of each asset, retrieve line of datas at t-1 and put it on t
        for index, row in zip(range(len(w) - 1), w.iterrows()):
            if vol[index + 1] == 0:
                w.iloc[index + 1,] = w.iloc[index,]
                sgn.iloc[index + 1,] = sgn.iloc[index,]

        # Multiply t by sum_delta to evaluate the strength of the spread with stock price and different moving average in order to quantify the trend an so to quantify the weight
        w = w * sgn

        # normalize so that they sum to 1
        w = w.div(w.sum(axis=1), axis=0).fillna(0)  # Na's if downcreasing trend for all underlying assets

        return w

