from operator import pos
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
