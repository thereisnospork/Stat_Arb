import sys
import model as md
import time


timing_start = time.time()

from scipy.optimize import differential_evolution

timing_start = time.time()

symbol_string = sys.argv[1]
sym = md.get_time_open(symbol_string, directory='./DJIA_2016/')
arguments = (sym,5,10000,30,60,1)  #trade_algo2 inputs after up_then down : symbol|buy_start|money_init|buy_stop|panic_stop|iter
bnds = ((0, 0.05),(0, 0.05))
res = differential_evolution(md.trade_algo2_profit_only_short, bnds, args=(arguments),disp = True)

print(str(res.x[0]) + str(res.x[1]))
print(res.x)
print(res.fun)
print(res)
print(symbol_string + ' short')
print(str(delta_time) + 'seconds')

