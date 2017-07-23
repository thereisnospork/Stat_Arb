import model as md
import time
from ggplot import *
import pandas as pd
#import numpy as np #imports as dependency from model



timing_start = time.time()



def opti_all(symbols, output_file):
    '''Optimizes all symbols based on trade_aldo_1_iter using scipy.differential evolution  Prints to CSV outputfile'''
    results = list()
    for symbol in symbols:
        res2 = differential_evolution(trade_algo2, args=(symbol,))
        results.append(res2.x)
        print(res2.x)
        print(symbol)
    np.genfromtxt(output_file,results)
















#def trade_algo1_iter(up_then_down, symbol, buy_start = 5, n=20, money_init = 10000, buy_stop = 30, panic_stop = 30):

#asdf = md.trade_algo1_iter((0.07,.007),'gt',n=500,data_folder = './/DJIA_minute//')

# sym = md.get_time_open('aapl',directory='.//DJIA_2016//')
# asdf = md.trade_algo2((7,1),sym)
#
# asdf.to_csv('out.csv')
#
# print(type(asdf))
#
# plot = ggplot(aes(x = 'day', y = 'money'),asdf) + geom_point()
# plot
# #print(asdf)


timing_end = time.time()
timing = timing_end-timing_start
print(str(timing)+ ' ' +'seconds')
