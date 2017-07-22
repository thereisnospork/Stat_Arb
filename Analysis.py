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


##EXECUTE##
timing_start = time.time()




timing_end = time.time()
print(str(timing_end-timing_start) + 'seconds elapsed')