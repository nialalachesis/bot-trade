from datetime import date, datetime, timedelta
import json as js
import pandas as pd
import ta
import requests
import pickle



url = "https://api.binance.com/api/v3/klines"

symbol = "BTCUSDT"
interval = "1d"
startTime = int((datetime.now() - timedelta(50)).timestamp() * 1000)
endTime = int(datetime.now().timestamp() * 1000)




parameter = {"symbol":symbol, "interval":interval, "startTime":startTime}
res = js.loads(requests.get(url,params=parameter).text)
df = pd.DataFrame(res, columns = ['timestamp','open','high','low','close','volume',
    'close_time','quote_av','trades','tb_base_av','tb_quote_av','ignore'])

del (df['quote_av'] ,df['tb_base_av'], df['ignore'],df['close_time'],
df['tb_quote_av'],df['volume'],df['trades'])

df['timestamp'] = pd.to_numeric(df['timestamp'])
df['open'] = pd.to_numeric(df['open'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['close'] = pd.to_numeric(df['close'])

df['timestamp'] = df['timestamp'] # + 7200000 # UTC+2 
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.index = df['timestamp']
del df['timestamp']

#indicator

df['ema1']=ta.trend.ema_indicator(close=df['close'], window=11)
df['ema2']=ta.trend.ema_indicator(close=df['close'], window=35)
df['rsi']=ta.momentum.stochrsi(close=df['close'], window=14)

#wallet

#rec = {"usdt":1000,"coin":0,"position":False,"volume":0,"fee":0.4}

with open("dataUser/wallet", "rb") as file:
    get_record = pickle.Unpickler(file)
    rec = get_record.load()
    print(rec)

usdt = float(rec['usdt'])
coin = float(rec['coin'])
position = float(rec['position'])
vol = int(rec['volume'])
fee = float(rec['fee'])

######################### strat ##########################


    


def strat(coin,usdt,position,vol,fee,df,rec):

    def log(lastindex,vol,df):
        
        with open("dataUser/log.txt", "a") as log:
            log.write(str(vol))
            log.write("  buy at ")
            log.write(str(df['close'][lastindex]))
            log.write(" $ ")
            log.write(" the ")
            log.write(str(lastindex))
            log.write("\n")

    def save(coin,usdt,position,vol):
        rec['usdt'] = usdt
        rec['coin'] = coin
        rec['position'] = position
        rec['volume'] = vol

        with open("dataUser/wallet", "wb") as file:
            record = pickle.Pickler(file)
            record.dump(rec)



    lastindex = df.last_valid_index()

    if (df['ema1'][lastindex] < df['ema2'][lastindex] 
    and usdt > 10 
    and position == False):

        coin = (usdt/df['close'][lastindex])* (1 - (fee/100))
        usdt = 0
        print("buy")
        position = True
        vol = vol + 1
        log(lastindex,vol,df)

    if (df['ema1'][lastindex] > df['ema2'][lastindex] 
    and coin > 0.0001 
    and position == True):

        usdt = (coin * df['close'][lastindex])* (1 - (fee/100))
        coin = 0
        print("sell")
        position = False
        vol = vol + 1
        log(lastindex,vol,df)

    save(coin,usdt,position,vol)
    print("usdt",usdt)
    print("volume",vol)
    print("coin",coin)



strat(coin,usdt,position,vol,fee,df,rec)
