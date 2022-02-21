import os
from binance import Client
import pandas as pd

current_directory = os.getcwd()
print(current_directory)
# api keys
api_key = os.environ.get("BINANCE_API_KEY")
api_secret = os.environ.get("BINANCE_SECRET_KEY")

client = Client(api_key, api_secret)

# read csv
position_frame = pd.read_csv("position")


def change_position(current, buy=True):
    if buy:
        position_frame.loc[position_frame.Currency == current, "position"] = 1
    else:
        position_frame.loc[position_frame.Currency == current, "position"] = 0
    position_frame.to_csv("position", index=False)


def gethourlydata(symbol):
    frame = pd.DataFrame(client.get_historical_klines(
        symbol, "1h", "25 hours ago UTC"))
    frame = frame.iloc[:, :5]
    frame.columns = ["Time", "Open", "High", "Low", "Close"]
    frame[["Open", "High", "Low", "Close"]] = frame[[
        "Open", "High", "Low", "Close"]].astype(float)
    frame.Time = pd.to_datetime(frame.Time, unit="ms")
    return frame


df = gethourlydata("BTCUSDT")


def applytechnicals(df):
    df["FastSMA"] = df.Close.rolling(7).mean()
    df["SlowSMA"] = df.Close.rolling(25).mean()


def trader(curr):
    # how much buy or sell
    qty = position_frame[position_frame.Currency == curr].quantity.values[0]
    # get data
    df = gethourlydata(curr)
    applytechnicals(df)
    lastrow = df.iloc[-1]

    if not position_frame[position_frame.Currency == curr].quantity.values[0]:
        if lastrow.FastSMA > lastrow.SlowSMA:
            # order = client.create_order(symbol=curr,side="BUY",type="MARKET",quantity=qty)
            # print (order)
            change_position(curr, buy=True)
        else:
            print(f"Not in position{curr} but Condition not fulfilled")
    else:
        print(f"Already in {curr} position")
        if lastrow.SlowSMA > lastrow.FastSMA:
            # order = client.create_order(symbol=curr,side="SELL",type="MARKET",quantity=qty)
            # print (order)
            change_position(curr, buy=False)
        else:
            print(f"Not in position{curr} but Condition not fulfilled")
