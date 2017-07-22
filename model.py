#####VERSION 7 ########
#


#TO DO: successfully seperate out get_time_open from algo eval ####

import time
import numpy as np
#import scipy as sp
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
# import tensorflow as tf
import os
import csv
import matplotlib as plt


###Data Handling###

# folders = os.listdir('./DJIA_minute') #list of dirs
# folders.sort() #sorted old -> new
#blah blah blah blah testing synch blah blah blah



def get_time_open(SYM, directory='./DJIA_2016/', start=900, stop=1400):  ##date as sequential integer
    """pulls time (native formate HHMM and open price for symbol. date is sequential integer input"""
    folders = os.listdir(directory)  # list of data dirs in selected dir
    folders.sort()  # sorted by date, old -> new
    list_by_date = list()
    for folder in folders:
        symbol_data = np.genfromtxt(directory + folder + '/table_' + SYM + '.csv', delimiter=',', usecols=(1, 2))
        early_mask = symbol_data[:, 0] > start  # start of day
        late_mask = symbol_data[:, 0] < stop  # end of day HHMM
        mask = early_mask * late_mask  # mask combination
        #  print(mask)
        extract = symbol_data[mask]  ##applies the mask down the column(s) and appends the masked to the list of np.arrays
        length = delta_minutes(start, stop) + 1

        if len(extract[:, 1]) < stop - start:
            extract.resize((length,2))  #####debug me resize ro start - stop mod 60 (etc)
        list_by_date.append(extract[:,1])
    full_data = np.concatenate(list_by_date, axis = 0) #sticks all data extracted for symbol into 1 numpy array
    full_data.resize(len(list_by_date),length)#  resize into shape, each row 1 day access as ARRAY[col#]_

    return full_data  # full_data

def delta_minutes(t1, t2):  # only deals with whole minutes, forces to int
    """ Calculates delta minutes from HHMM formate 24hr time delta_min +1 then
    equals number of rows in that time interval @ 1min interval """
    hr_1 = t1 // 100  ##### HHMM formate / divide no remainder for Hours then subtract hrs to get min
    hr_2 = t2 // 100  ##### DEBUG MR
    min_1 = (t1 - hr_1 * 100)
    min_2 = (t2 - hr_2 * 100)
    # print(hr_1,hr_2,min_1,min_2)
    min_1 = hr_1 * 60 + min_1
    min_2 = hr_2 * 60 + min_2
    delta = min_2 - min_1
    # print(delta)
    return delta

### Alogorythm (s) ###

def trade_algo1(up_then_down, symbol, buy_start = 5, money_init = 10000, buy_stop = 30, panic_stop = 30):#, dates):
    """"algorithm implementation.  inputs +/- bounds, symbol(s)  returns a list of profit of each trading day. up / down input as decimal percent
        upthendown: 2 unit list

    """
    #data_array = get_time_open(symbol)   ####generate data array within vs outside function
    up = up_then_down[0]
    down = up_then_down[1]  ###for array input into optimize function
    data_array = symbol
    profit = list()
    for row in data_array:  ###nditer to go row wise over data_array #### trivially parallel at this for loop
        buy_time = np.random.random_integers(buy_start, buy_stop)
        price = row[buy_time]
        shares = money_init//price
        paid = shares * price   ###END BUY LOGIC ###
        ###START SELL Logic###
        for tick in row[buy_time + 1:-1]:    #### check slicing, starting from minute_tick after buy_time
            if tick > price + price * up:
                sold = tick * shares
                profit.append(sold - paid)
                break
            if tick < price - price * down and tick != 0:
                sold = tick * shares
                profit.append(sold - paid)  ##adds
                break
            if tick == row[-panic_stop] and tick != 0:#-panic_stop]: ##did not meet exit condition, sell default 30 minutes before end of day.  Possible issues if panic stop exceeds number of trailing zeros in row
                sold = tick * shares
                profit.append(sold - paid)
                #print(str(tick) +' tick ' + str(shares) + ' shares ' + str(price) +' price')
                #print('timeout, sold ' + str(sold) +', paid ' + str(paid))
                break
            #print(str(profit) +'profit')
  #  print(sum(profit) +' sum profit')
    return -1 * sum(profit)    #inverted output for benefit of minimize function (scipy)

def trade_algo1_iter(up_then_down, symbol, buy_start = 5, n=20, money_init = 10000, buy_stop = 30, panic_stop = 30):
    """Averages x interations"""
    data = np.zeros(n)
    symbol_data = get_time_open(symbol)
    for i in range(n):
        datum = trade_algo1(up_then_down, symbol_data, buy_start, money_init, buy_stop, panic_stop)
        data[i] = datum
    result = np.mean(data)
    return result

def opti_all(symbols, output_file):
    '''Optimizes all symbols based on trade_aldo_1_iter using scipy.differential evolution  Prints to CSV outputfile'''
    results = list()
    for symbol in symbols:
        res2 = differential_evolution(trade_algo1_iter, bnds, args=(symbol,))
        results.append(res2.x)
        print(res2.x)
        print(symbol)
    np.genfromtxt(output_file,results)


    return (asdf)

def print_results(list_of_results):
    """takes list (up,down,symbol_as_string)"""
    for result in list_of_results:
        profit = trade_algo1_iter(result[0],result[1])
        print(str(profit)+ ' ' + result[1])


# ^^^^^^^^^^^^^^^^^^^^DEBUG ME^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
##EXECUTE##
timing_start = time.time()

#inputs = np.array([high, low])
# x0 = (.005,.01)
# bnds = ((0,.1),(0,.1)) #bound the inputs 0,10pct
# symbols = ('aapl','aig','axp','ba','bac','c','cat','csco','cvx','dd','dis',
#            'ge','gs','gt','hd','hon','hpq','ibm','intc','ip','jnj','jpm','ko',
#            'mcd','mmm','mo','mrk','msft','nke','pfe','pg','trv','unk','utx','vz',
#            'wmt','xom')
#
# opti_all(symbols, 'all_optimized.csv')

short = [[[0.00557528,0.00185379],'aapl'],
[[0.07281943,0.00568387],'aig'],
[[0.07022998,0.00360369],'axp'],
[[0.0503437,0.00518098],'ba'],
[[0.00280995,0.04761158],'bac'],
[[0.01406295,0.03561052],'c'],
[[0.06762976,0.00587916],'cat'],
[[0.00860325,0.00811569],'csco'],
[[0.00849136,0.00288248],'cvx'],
[[0.05161093,0.00519237],'dd'],
[[0.07089521,0.00494719],'dis'],
[[0.00058142,0.00044623],'ge'],
[[0.05027102,0.0032439],'gs'],
[[0.07082985,0.01007958],'gt'],
[[0.05740773,0.00495989],'hd'],
[[0.03605639,0.00463496],'hon'],
[[0.03958526,0.00436299],'hpq'],
[[0.06253051,0.00424721],'ibm'],
[[0.00600533,0.0195076],'intc'],
[[0.06890256,0.00743289],'ip'],
[[0.06826672,0.00198224],'jnj'],
[[0.01185559,0.00019781],'ibm'],
[[0.01860628,0.0055825],'mcd'],
[[0.05250509,0.00286221],'mmm'],
[[0.02590775,0.00316596],'mo'],
[[0.03953711,0.00501394],'mrk'],
[[0.00253434,0.03322771],'msft'],
[[0.01572529,0.01369308],'nke'],
[[0.0607296,0.02311622],'pfe'],
[[0.04879832,0.00134363],'pg'],
[[0.05470664,0.0047023],'trv']]

long = [[[0.04851386,0.00563457],'aapl'],
[[0.00381956,0.05354488],'aig'],
[[0.00637289,0.04302866],'axp'],
[[0.0040113,0.01915204],'ba'],
[[0.04152606,0.00599932],'bac'],
[[0.00772714,0.00872866],'c'],
[[0.01884494,0.07000933],'cat'],
[[0.01641655,0.00265472],'csco'],
[[0.0402106,0.01610199],'cvx'],
[[0.00679118,0.08803495],'dd'],
[[0.01517777,0.09775599],'dis'],
[[0.02708419,0.00516124],'ge'],
[[0.01686101,0.09382813],'gs'],
[[0.00648983,0.06773664],'gt'],
[[0.00463562,0.09878199],'hd'],
[[0.00411023,0.09256679],'hon'],
[[0.00896651,0.04610689],'hpq'],
[[0.02597515,0.07220315],'ibm'],
[[0.01875173,0.0085123],'intc'],
[[0.00573747,0.03284219],'ip'],
[[0.00749818,0.06137275],'jnj'],
[[0.03763235,0.00817235],'jpm'],
[[0.00370947,0.03574267],'mcd'],
[[0.00275564,0.05624655],'mmm'],
[[0.00552901,0.06228388],'mo'],
[[0.00714736,0.05544184],'mrk'],
[[0.01918663,0.00654561],'msft'],
[[0.00028612,0.06999424],'nke'],
[[0.01679991,0.0003181],'pfe'],
[[0.00319645,0.02215017],'pg'],
[[0.00334016,0.0720133],'trv']]

print_results(long)
print('End Long Res')
print_results(short)
print('end Short Res')

#res = trade_algo1_iter(x0,xom)


# res = minimize(trade_algo1_iter,x0, args = (xom), method='TNC', bounds = bnds, options={'eps':1})#inputs)
# print(res)
# print(type(res))

# res2 = differential_evolution(trade_algo1_iter, bnds,args = (xom,))
# print(res2)




timing_end = time.time()
print(str(timing_end-timing_start) + 'seconds elapsed')





