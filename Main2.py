import talib
import yfinance as yf
from nselib import capital_market
from yahooquery import Ticker

# ----------------FULL EQUIT LIST-----------------------
Full_equity_list = capital_market.equity_list()
Full_equity_list["SYMBOL"] = Full_equity_list["SYMBOL"]+".NS"
Full_stock_list = Full_equity_list["SYMBOL"].to_list()
# ________________________________________________________
# ------------------NIFTY_50 LIST---------------------------

Fno_List = capital_market.fno_equity_list()
Fno_List["symbol"] = Fno_List["symbol"]+".NS"
Fno_Stock_list = Fno_List["symbol"].to_list()
# ____________________________________________________________
# list1 = Fno_Stock_list
list1 = Full_stock_list
count = 1
for stock in list1:
    print(count) 
    print(stock)
    count = count+1
    try:
        data2 = yf.Ticker(stock)
        market_cap = data2.info["marketCap"]/10000000
        if(market_cap < 5000):
            continue
    except:
        print("exception occured!")

    try:
        data = yf.download(stock,start = "2024-01-01" , end = "2024-09-16")
        data['rsi'] = talib.RSI(data["Close"],14)
        data['ema_21'] = talib.EMA(data["Close"],21)
        data['ema_50'] = talib.EMA(data["Close"],50)
        data['ema_150'] = talib.EMA(data["Close"],150)
        data['s_rsi_5'] = talib.EMA(data['rsi'],5)
        data['s_rsi_9'] = talib.EMA(data['rsi'],9)
        data['s_rsi_21'] = talib.EMA(data['rsi'],21)
        index = Fno_List.loc[Fno_List['symbol'] == stock].index[0]

        data["cross"] = "NO"
        # checking if stock is in MOMENTUM AND UPTREND
        if  data.iloc[-1]['s_rsi_9'] > data.iloc[-1]['s_rsi_21'] and data.iloc[-1]['s_rsi_5'] > data.iloc[-1]['s_rsi_9'] and data.iloc[-1]['ema_21'] > data.iloc[-1]['ema_50'] and data.iloc[-1]['ema_50'] > data.iloc[-1]['ema_150'] and (market_cap >= 5000) :
            Fno_List.loc[index,'Cross'] = 'YES'
        else:
            Fno_List.loc[index,'Cross'] = 'NO'
    except:
        print("exception occured!")
# FINALLIST OF STOCK WITH UPTREND MOMENTUM
finallist = Fno_List.loc[Fno_List["Cross"]=="YES"]["symbol"].to_list()

print(finallist)
print(len(finallist))

