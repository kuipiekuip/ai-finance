
from yahoo_fin.stock_info import get_data

from yahoo_fin import stock_info as si

import yfinance as yf
from yahooquery import search

company_name = "ABN AMRO"
result = search(company_name)

# Print the first result's ticker symbol
ticker_name = result["quotes"][0]["symbol"]

comp = yf.Ticker(ticker_name)
comp_historical = comp.history(start="2020-06-02", end="2020-06-07", interval="1d")
print(comp_historical)

specific_date = "2020-06-03"
volume = comp_historical.loc[specific_date, "Volume"]
print(f"Volume on {specific_date}: {volume}")