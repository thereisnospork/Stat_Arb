import model as md
import time
from scipy.optimize import differential_evolution

from ggplot import *
import pandas as pd
#import numpy as np #imports as dependency from model



timing_start = time.time()

sym = md.get_time_open('ibm',directory='.//DJIA_2016//')
arguments = (sym,5,10000,30,60,300)  #trade_algo2 inputs after up_then down : symbol|buy_start|money_init|buy_stop|panic_stop|iter
bnds = ((0, 0.05),(0, 0.05))
res = differential_evolution(md.trade_algo2_profit_only_short, bnds, args=(arguments))
print(res)
print(res.x)
print(res.fun)
print('gt_long')

#to do:
#get daily data to plot
#calculate max draw down / Sharpe Ratio

##EXecute single version of optimized ##;s

#arguments = (sym,5,10000,30,60,30)  #trade_algo2 inputs after up_then down : symbol|buy_start|money_init|buy_stop|panic_stop|iter
# bnds = ((0, 0.05),(0, 0.05))
# sym = md.get_time_open('gt',directory='.//DJIA_2016//')
# res = md.trade_algo2_profit_only_short(([ 0.03333181,  0.04332638]),sym,5,10000,30,90,2000)
# print(res)







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
