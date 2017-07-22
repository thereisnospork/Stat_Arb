import model as md
import time
import pandas as pd
#import numpy as np #imports as dependency from model



timing_start = time.time()
#def trade_algo1_iter(up_then_down, symbol, buy_start = 5, n=20, money_init = 10000, buy_stop = 30, panic_stop = 30):

asdf = md.trade_algo1_iter([0.07,.007],'gt',n=500,data_folder = './/DJIA_minute//')

print(type(asdf))

timing_end = time.time()
timing = timing_end-timing_start
print(timing)
print(timing/500)
