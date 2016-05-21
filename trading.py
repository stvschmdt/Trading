# -*- coding: utf-8 -*-
"""
Spyder Editor

author: steve schmidt
title: algorithmic trading functions
todo: separate functions to classes
started: 5.13.16

todo:
1. read baseline dates spy from yahoo
2. read list of /tech/ stocks in from csv
3. read in /tech/ stocks data into storage unit
4. join on dates, adj close into one dataframe formatted as such:
date as idx, spy, stock1, stock2, stock3...stockn as adjclose
5. format missing values in dataframe
6. write dataframe out to storage for easier future reading
7. write out ancillary data from dateframes to files for each stock
8. implement a timing function
"""

import pandas as pd
import numpy as np
from yahoo_finance import Share
import matplotlib.pyplot as plt
import time
import math

def main():
    #always time to improve
    start = time.clock()   
    #user fields -> single stock
    ndays = 20
    sdate = '2013-01-01'
    edate = '2016-05-20'
    sym = 'nvda'
    #for data filtering
    feature = 'MarketCap'
    tol = 2000000000
    bank = 10000  
    #init data for single share
    df_sym = df_initShareData(sym, sdate, edate)
    
    if len(df_sym) == 0:
        print "ending"
        return -1
    #get statistics for tech analysis      
    df_sym = df_initShareFrame(df_sym,sym)
    if len(df_sym) == 0:
        print "ending"
        return -1
    #first get daily results and cum results
    df_sharpe = df_dailyReturns(df_sym)
    sharpe = sharpeRatio(df_sharpe, len(df_sym))
    df_sym = df_statBuilder(df_sym, ndays)
    if len(df_sym) == 0:
        print "ending"
        return -1
    #FS = Full Single Stock for writing out
    df_writeCsv(df_sym, "/Users/steveschmidt/trading/FS_{}.csv".format(sym))
    #simulation ---> assumes zero shares held to start
    profit = singleSimulation(df_sym, bank)
    reportSingleSimulation(profit, bank)
    
    print "[cum var]\t{}".format(cumulativeReturns(df_sym[sym]))
    print "[sharpe]\t{}".format(sharpe[sym])
    end = time.clock()
    print "-----------------------------------------"
    print "[run time]\t{}".format(end-start)
    

    #filename = "/Users/steveschmidt/trading/shortlist.csv"
    #filename = "/Users/steveschmidt/trading/mediumlist.csv"
    filename = "/Users/steveschmidt/trading/companylist.csv"
    #let's get the right days & baseline reference using SPY
    #df_pfolio = df_shareToAdjClose('goog',start_date,end_date)
    #df_spy = df_pfolio.copy()
    #this is a df of tech sector stocks
    df_Tech = df_readCsv(filename)
    df_Tech = df_filterCompanies(df_Tech, feature, tol)
    df_Tech = df_filterCompanies(df_Tech, 'IPOyear', '2013',1)
    #todo -> add check for ipo before 2016, and market cap over X amount
    #print "[creating data for:] {}".format([x for x in df_Tech['Symbol']])
    #read in the list of stocks from csv, column symbol has the string to use
    l_stocks = []
    for i in df_Tech['Symbol']:
        l_stocks.append(i)
    
    #this line should only be run when new data is needed in mass --> comment out
    #fetchDataToCsv(l_stocks, sdate, edate)
        
#        df_tech = df_shareToAdjClose(i, start_date, end_date)
#        df_pfolio = df_joinDataFrames(df_pfolio, df_tech)
        #df_pfolio = df_normalize(df_pfolio)
    #print df_pfolio
#    df_writeCsv(df_pfolio, "/Users/steveschmidt/trading/prices.csv")
#    df_pfolio = df_normalize(df_pfolio)
#    df_writeCsv(df_pfolio, "/Users/steveschmidt/trading/normprices.csv")
    #single stock analysis testing
#    df_smaSpy = df_rollingAve(df_spy, 20)
#    df_stdSpy = df_rollingStd(df_spy, 20)
#    upper_bollinger, lower_bollinger = df_bollingerBands(df_smaSpy, df_stdSpy)
#    df_bs = df_spy.join(upper_bollinger, lsuffix="_price",rsuffix='_upper')
#    df_bs = df_bs.join(lower_bollinger)
#    l_labels = ['SPY','Rolling Mean', 'Upper Bollinger', 'Lower Bollinger']
    #plot bollinger bands with simple moving average
#    plot_singleSymbol(df_spy, [df_smaSpy, upper_bollinger, lower_bollinger], l_labels)
    #print df_spy
#    ret= 0
#    hold = 0 
#    print df_bs
##    for index,row in df_bs.iterrows():
#        if hold == 0 and row['goog'] > row['goog_price']:
#            price = buy(row['goog_price'])
#            print "[buy:] {} stock".format(index)
#            hold = 1
#        if hold != 0 and row['goog_upper'] < row['goog_price']:
#            print "[sell:] {} stock".format(index)
#            ret += sell(row['goog_price'],price )
#            hold = 0
#        
#    print "[return for period: ] {}".format(ret)
#    end = time.clock()
#    df_pfolio.plot(title="Trends", fontsize=2)
#    plt.show()
#    print "\n[run time:] {}".format(end-start)

def df_initShareData(sym, sdate, edate):
    try:
        s = Share(sym)
        l_s = s.get_historical(sdate, edate)
        df_s = pd.DataFrame(l_s)
        return df_s
    except:
        print "[error] receiving data from host..please try again or load from csv"
        df = pd.DataFrame()
        return df
        
def df_initShareFrame(df,symbol):
    df = df.copy()
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Adj_Close'] = pd.to_numeric(df['Adj_Close'])
        #do this first to print full data for future
        #df_writeCsv(df, "/Users/steveschmidt/trading/F_{}.csv".format(symbol))
        df = df[['Date','Adj_Close']]
        #dont use original dataframe label ---->
        df = df.rename(columns={'Adj_Close':'{}'.format(symbol)})
        df = df.set_index('Date').sort_index()
        return df
    except:
        print "[error] dataframe formatting\n", df
        df = pd.DataFrame()
        return df
        
def df_statBuilder(df,days):
    try:    
        #these are all dataframes
        rm = df.rolling(days).mean() 
        std = df.rolling(days).std()
        bolu = rm + 2*std
        boll = rm - 2*std
        rm = rm.rename(columns={'{}'.format(list(df)[0]) : 'rolling_mean'})
        bolu = bolu.rename(columns={'{}'.format(list(df)[0]) : 'upper_band'})
        boll = boll.rename(columns={'{}'.format(list(df)[0]) : 'lower_band'})
        #add these all onto df
        df = df.join(rm)
        df = df.join(bolu)
        df = df.join(boll)
        return df
    except:
        print "[error] stat builder fail\n", df, rm, std, bolu, boll
        df = pd.DataFrame()
        return df

#daily returns, n-(n-1) so day zero will be zero, account for this    
def df_dailyReturns(df):
    df1 = df.copy()
    df1 = (df1[1:] / df1[:-1].values) - 1
    df1.ix[0,:] = 0
    return df1
        
#assumes zero shares held to start
def singleSimulation(df, money):
    sym = list(df)[0]
    h = list(df)[2]
    l = list(df)[3]
    hold = 0
    ret = 0
    price = 0
    shares = 0
    for idx, row in df.iterrows():
        if hold == 0 and row[l] > row[sym]:
            hold = 1
            price = row[sym]
            shares = int(money/price)
            money = money - shares*price
            print '[buy]\t{}\t{}\t{}\t{}'.format(sym,shares,price,money)
        if hold == 1 and row[h] < row[sym] and row[sym] > price:
            hold = 0
            ret += shares * (row[sym]-price)
            money += shares * row[sym]
            print '[sell]\t{}\t{}\t{}\t{}'.format(sym,shares,row[sym],money)
            shares = 0
    if hold == 1:
        print "-----------------------------------------"
        print "[long] \t{}\t{}\t{}\t{}".format(sym,shares,df[sym][-1],money)
    df.plot()
    return ret
    
#sum of all dailyReturns()/n days
def meanDailyReturns(df):
    m = df.mean()
    return m
   
def reportSingleSimulation(prof, init):
    print "-----------------------------------------"
    print "[cum ret]\t{}".format(prof)
    print "-----------------------------------------"
    print "[prc ret]\t{}".format(prof/init)
    print "-----------------------------------------"

#read in a csv, return a pandas dataframe
def df_readCsv(filename):
    df = pd.read_csv(filename)
    return df
    #print df['Symbol']
    
def df_writeCsv(df,path):
    df.to_csv(path)
    
#risk adjusted return
#mean daily returns / std daily returns
#approximate to zero or use shortcut
#divided by k=root(number of days per year ie 252)
def sharpeRatio(df, k=252):
    k = math.sqrt(k)
    sr = k * (df.mean() / df.std())
    return sr

def df_filterCompanies(df, key, val, lt=0):
    if lt == 0:
        df1 = df.loc[df[key] > val]
    elif lt == 1:
        df1 = df.loc[df[key] < val]
    else:
        df1 = df.loc[df[key] == val]
    print "[filter]\t{}\t{}\t{}\t{}".format(key,val,len(df), len(df1))
    return df1
#input: string name of stock, start/end dates
#output: dataframe with index dates, one column named the stock name, data is adj close prices
#option: write the entire Share object to file
#figure out the index TODO
def df_shareToAdjClose(symbol, start_date, end_date):
    try:
        s_symbol = Share(symbol)
        l_symbol = s_symbol.get_historical(start_date, end_date)
        df_symbol = pd.DataFrame(l_symbol)
        df_symbol = df_symbol[['Date','Adj_Close']]
        df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])
        df_symbol['Adj_Close'] = pd.to_numeric(df_symbol['Adj_Close'])
        df_symbol = df_symbol.rename(columns={'Adj_Close':'{}'.format(symbol)})
        df_symbol = df_symbol.set_index('Date').sort_index()
        return df_symbol
    except:
        print "[data collection error:] {}".format(symbol)
        
    
#for each asset, over the time period, what are all the returns each day + -
def cumulativeReturns(series):
    ret = (series[-1]/series[0]) - 1
    return ret
    
#std of daily returns
def stdDailyReturns(df):
    s = df.std()
    return s

def plot_singleSymbol(df_symbol, l_toplot, l_labels):
    ax = df_symbol.plot(title="Bollinger Bands", label="{}".format(l_labels[0]))
    for i in range(0,len(l_toplot)):
        l_toplot[i].plot(label="{}".format(l_labels[i]), ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.legend(l_labels)
    plt.show()
   
   
def df_joinDataFrames(df1, df2, key=None):
    if key == None:
        try:
            df1 = df1.join(df2)
            #df1 = df1.dropna()
            return df1
        except:
            print "[bad dataframe]\n{}".format(df2)
            return df1
    else:
        #todo
        return df1
        
    
#divide pandas dataframe by first row
def df_normalize(df1):
    try:
        df1 = df1 / df1.ix[0,:]
    except:
        print "[bad division error]"
    return df1

    
def df_bollingerBands(df_rMean, df_rStd):
    upper = df_rMean + df_rStd*2
    lower = df_rMean - df_rStd*2
    return upper, lower
    
def plt_plot():
    
    return 0
    
def l_linReg(l_prices):
    return 0
    
def type_formatData(data, type='nparray'):
    return 0
    
def df_rollingAve(df_symbol, ndays):
    df_sma = df_symbol.rolling(window=ndays).mean()
    return df_sma
    
def df_rollingStd(df_symbol, ndays):
    df_std = df_symbol.rolling(window=ndays).std()
    return df_std
    
#todo later
def l_perturb(l_prices):
    return 0
    
def l_dailyPortfolioBalance():
    return 0
    
def fetchDataToCsv(l_stocks, start_date, end_date):
    try:
        for symbol in l_stocks:
            s_symbol = Share(symbol)
            l_symbol = s_symbol.get_historical(start_date, end_date)
            df_symbol = pd.DataFrame(l_symbol)
            df_symbol['Date'] = pd.to_datetime(df_symbol['Date'])
            df_symbol['Adj_Close'] = pd.to_numeric(df_symbol['Adj_Close'])
            df_symbol = df_symbol.rename(columns={'Adj_Close':'{}'.format(symbol)})
            df_symbol = df_symbol.set_index('Date').sort_index() 
            df_writeCsv(df_symbol, "/Users/steveschmidt/trading/data/2013_2015/F_{}.csv".format(symbol))
            print "[fetch]\t{}".format(symbol)
        return 0
    except:
        print "[error] data fetch error - check offline files"
        return -1

def l_readCsv():
    return 0

main()