from typing import Optional

import yfinance as yf
import app_config as cfg
import time
import os

# valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
# TICKER_PERIOD = '1mo'
TICKER_START = '2021-01-09'
TICKER_END = '2021-01-17'
# valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
TICKER_INTERVALS = ['15m', '30m', '60m']
STOCK_DATA_DIRECTORY = '../json/stock'

def main():
    company_keys = cfg.example_sp500_companies.keys()
    # company_keys = ['TSLA']
    for company_key in company_keys:
        print(f'company key: {company_key}')
        company_ticker = yf.Ticker(company_key)
        print(f'company ticker info:\n{company_ticker.info}')

        for ticker_interval in TICKER_INTERVALS:
            stock_history = company_ticker.history(start=TICKER_START, end=TICKER_END, interval=ticker_interval)
            print(f'stock history for {company_key}:\n[start: {TICKER_START}, end: {TICKER_END}, '
                  f'interval:{ticker_interval}]\n{stock_history}')
            json_stock_history = stock_history.to_json(orient='table', date_format='iso')
            print(f'json history for {company_key}:\n[start: {TICKER_START}, end: {TICKER_END}, '
                  f'interval:{ticker_interval}]\n{json_stock_history}')

            milliseconds = int(round(time.time() * 1000))
            file_name = f'{STOCK_DATA_DIRECTORY}/stock_yfinance_{company_key}_{TICKER_START}-{TICKER_END}_' \
                        f'ti{ticker_interval}_{milliseconds}.json'
            with open(file_name, "w") as write_file:
                write_file.write(json_stock_history)
                print(f'File saved as: {os.path.realpath(write_file.name)}')


if __name__ == '__main__':
    main()
