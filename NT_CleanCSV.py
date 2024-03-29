import pandas as pd
df = pd.read_csv('NinjaTrader.csv') #retrieve our raw data file

get_ipython().run_line_magic('run', 'NTTimeCalc.ipynb')
import import_ipynb
from NTTimeCalc import ticks_to_DT #import functions to clean up timestamp data

#check for duplicate data
df.duplicated().any()
#check for any null values
df.isnull().any()

def LS (binInput): #convert the binary 'MarketPosition' column into 'Buy'/'Sell' strings
    if binInput == 0: 
        return 'Buy'
    else:
        return 'Sell'

df['OrderType'] = df['MarketPosition'].apply(LS)


#create TradeID based on 'Position' resets (0)
lastPos = None
lastID = 0

def trade_ID(row):
    global lastPos, lastID

    if lastPos is None or abs(lastPos) > 0:
        lastPos = row['Position']
        return lastID
    elif lastPos == 0:
        lastID += 1
        lastPos = row['Position']
        return lastID

df['TradeID'] = df.apply(trade_ID, axis=1)


#create grouped trades by 'TradeID'
gTrades = df.groupby('TradeID').apply(lambda x: x.index.tolist(), include_groups=False)

PL = []
contractQ = []

for idValue, row_num in gTrades.items(): #iterate through ID groups to calculate profit per trade
    entryPrice = float(df.iloc[row_num[0]]['Price'])
    contractQ.append(df.iloc[row_num[0]]['Quantity']) #number of contracts by initial trade
    b_s = df.iloc[row_num[0]]['OrderType'] #buy/sell signal 

    prices_List = []

    
    for row in row_num:
        curPrice = df.iloc[row]['Price']
        
        if row > 0:
            prices_List.append(curPrice)
    
    for index, p in enumerate(prices_List):
        if p == 0:
            contractQ.append(df.iloc[row_num[index]]['Quantity'])       #collect number of contracts for this trade 
        if p > 0:
            prices_List[index] -= entryPrice
        if index == len(prices_List) - 1: #determine absolute profit/loss depending on 'OrderType'
            if b_s == "Buy":
                PL_total = sum(prices_List)
                PL.append(PL_total)
            elif b_s == "Sell":
                PL_total = sum(prices_List) * -1
                PL.append(PL_total)



#establish new dataframe using calculated TradeIDs, contracts, and P/L
tradedf = pd.DataFrame(columns=['TradeID', 'Order Type', 'Contracts', 'Profit/Loss', 'Time'])

tradedf['TradeID'] = df['TradeID'].drop_duplicates()
tradedf['Order Type'] = df['OrderType']
tradedf['Contracts'] = contractQ
tradedf['Profit/Loss'] = PL
tradedf['Time'] = df['Time']


#export updated dataframes to csv files
df.to_csv('MasterData.csv', index=False)
tradedf.to_csv('TradeLog.csv', index=False)

