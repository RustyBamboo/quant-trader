#!python3

"""
    This bot obtains the average price that you bought a stock multiplied by the quantity.
    It then compares the price of the stock at a given moment with the initial bought value
    If it's lower than some threshold, it will automatically sell 
"""

import sys, time

sys.path.append('./pyrh')
from pyrh import Robinhood

from dotenv import load_dotenv
load_dotenv()
import os
USERNAME = os.getenv("RH_USERNAME")
PASSWORD = os.getenv("RH_PASSWORD")

rh = Robinhood(username=USERNAME, password=PASSWORD)
rh.login()

# Set how much you're willing to loss
PRICE_DIFF_LIMIT = -100

# How many seconds to wait before polling
REFRESH_TIME = 1800

def fetch_json_by_url(rh, url):
    return rh.session.get(url).json()

def get_current_positions(rh):
    positions = rh.positions()

    return [pos for pos in positions["results"] if float(pos["quantity"]) > 0]

# Get how much stock was bought for the first time
def obtain_bought(rh):
    bought = {}
    current_positions = get_current_positions(rh)
    for pos in current_positions:
        instrument = fetch_json_by_url(rh, pos["instrument"])

        avg_bought_price = float(pos["average_buy_price"]) * float(pos["quantity"])

        info = {"symbol": instrument["symbol"], "price": avg_bought_price, "quantity": float(pos["quantity"])}
        bought[instrument["url"]] = info
    return bought

# Get the price of stocks at this moment
def get_current_price(rh):
    current_price = {}
    current_positions = get_current_positions(rh)
    for pos in current_positions:
        instrument = fetch_json_by_url(rh, pos["instrument"])
        avg_price = rh.ask_price(instrument["symbol"])[0][0] # weird API return ask_price
        avg_price = float(avg_price) * float(pos["quantity"])
        info = {"symbol": instrument["symbol"], "price": avg_price, "quantity": float(pos["quantity"])}

        current_price[instrument["url"]] = info
    
    return current_price

bought = obtain_bought(rh)

while 1:
    current_price = get_current_price(rh)

    for instrument_url, info in current_price.items():
        if instrument_url in bought:
            bought_info = bought[instrument_url]
            # Compute percentage
            if bought_info["price"] > 1e-8:
                percent = (info["price"]/bought_info["price"]) - 1
                print(info["symbol"], percent)
                #TODO: could sell based of percentage

            # Compute price difference is below threshold, then sell the stock 
            price_diff = info["price"] - bought_info["price"]

            # If the diff
            if price_diff < PRICE_DIFF_LIMIT:
                print("Selling {} shares of {}".format(info["quantity"], info["symbol"]))
                instrument = {"url": instrument_url, "symbol": info["symbol"]}
                rh.place_sell_order(instrument, info["quantity"])

                # refresh bought list
                bought = obtain_bought(rh)

        # Detected a new entry, so refresh bought list
        else:
            bought = obtain_bought(rh)

    # Refresh every hour
    time.sleep(REFRESH_TIME)