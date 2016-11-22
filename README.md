# trade_sim

created by steve schmidt 2016

python 2.7+

pandas 0.17+

-- data loading and storage for share symbol information using yahoo_finance import

-- single share analysis (static and predictive)

-- portfolio analysis and optimization

-- simulations

-- overall science

Various technicals and ML algorithms will be implemented and tested to determine optimal trading strategies for simulation

Dev Plan

(drivers for entire platform)
Controller -> Loader
User Interface -> Loader
(get and set data - various formatting and storage)
Loader -> Symbol(s)
Loader -> File_IO
Loader -> DataFrame
Loader/DataFrame -> Lab
(computational work)
Lab -> Technical Analysis
Lab -> ML Analysis
Technical Analysis -> Lab
ML Analysis -> Lab
(experimentation and decision making - Brain)
Lab -> Simulator
(tracking and testing)
Simulator -> Account_Balances
Simulator -> Trading_Simulator
