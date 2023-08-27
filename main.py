import numpy as np
import pandas as pd
from datetime import date
import requests
import json
import yfinance as yf
from typing import Optional, Dict, Union, List, Tuple

open_figi_api_key = "paste_open_figi_api_key_here"


def fetch_stock_price_yfinance(stock: str, date_to_fetch: str) -> Optional[float]:
    try:
        start_date = (pd.to_datetime(date_to_fetch) - pd.DateOffset(days=15)).strftime('%Y-%m-%d')
        end_date = (pd.to_datetime(date_to_fetch) + pd.DateOffset(days=15)).strftime('%Y-%m-%d')
        data = yf.download(stock, start=start_date, end=end_date, progress=False)

        if data.empty:
            return None

        specific_date = pd.to_datetime(date_to_fetch)

        if specific_date in data.index:
            return data.at[specific_date, 'Adj Close']

        # If the specific date doesn't exist in the data, find the closest date
        closest_date_idx = np.argmin(np.abs(data.index - specific_date))
        closest_date = data.index[closest_date_idx]
        return data.at[closest_date, 'Adj Close']

    except Exception:
        return None


def isin_to_ticker(openfigi_apikey: str, isin: str) -> Optional[str]:
    url = "https://api.openfigi.com/v2/mapping"
    headers = {'Content-Type': 'text/json', 'openfigi-apikey': openfigi_apikey}
    payload = json.dumps([{'idType': 'ID_ISIN', 'idValue': isin}])
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]['data'][0].get('ticker', None) if 'data' in data[0] else None
    return None


def fetch_yearly_stock_prices(ticker: str, unique_years: list) -> Dict[int, Dict[str, Union[float, None]]]:
    yearly_prices = {}
    prev_end_price = None  # To store the end price of the previous year

    for year in unique_years:
        end_date = f"{year}-12-31"

        # Check if the date exceeds the current date
        if pd.to_datetime(end_date) > pd.to_datetime(date.today()):
            end_date = date.today().strftime('%Y-%m-%d')

        end_price = fetch_stock_price_yfinance(ticker, end_date)

        # If there's no previous end price, fetch the start price
        if prev_end_price is None:
            start_date = f"{year}-01-01"
            start_price = fetch_stock_price_yfinance(ticker, start_date)
        else:
            start_price = prev_end_price

        if end_price:
            yearly_prices[year] = {
                'start_price': start_price,
                'end_price': end_price
            }
            prev_end_price = end_price  # Update for the next iteration

    return yearly_prices


def populate_unique_years(stock_df: pd.DataFrame) -> List[int]:
    unique_years = sorted(list(stock_df['Datum'].dt.year.unique()) + [date.today().year])
    min_year = min(unique_years)
    max_year = max(unique_years)
    all_years = list(range(min_year, max_year + 1))
    return sorted(set(all_years + unique_years))


def calculate_current_worth(stock_df: pd.DataFrame, final_stock_price: float) -> Tuple[float, float, float]:
    all_stocks_owned_today = stock_df['Aantal'].sum()
    final_worth = final_stock_price * all_stocks_owned_today
    total_invested = stock_df['Waarde'].sum() * -1
    total_gain_value = final_worth - total_invested
    total_gain_percent = ((final_worth / total_invested) - 1) * 100 if total_invested != 0 else 0
    return total_gain_percent, total_gain_value, final_worth


def calculate_yearly_gains(stock_df: pd.DataFrame, yearly_prices: Dict[int, Dict[str, Union[float, None]]],
                           unique_years: List[int]) -> Dict[int, Dict[str, float]]:
    yearly_gains = {}
    for year in unique_years:
        start_of_year_value = yearly_prices[year]['start_price']
        end_of_year_stock_price = yearly_prices[year]['end_price']

        # Filter the DataFrame for records up to the end of the previous year
        previous_year_df = stock_df[stock_df['Datum'].dt.year < year]

        # Calculate the total number of stocks owned up to the end of the previous year
        total_stocks_previous_year = previous_year_df['Aantal'].sum()
        start_of_year_worth = total_stocks_previous_year * start_of_year_value

        # Filter the DataFrame for records only for the current year
        current_year_df = stock_df[stock_df['Datum'].dt.year == year]

        # Calculate the total purchase price for the current year
        total_purchase_price_this_year = current_year_df['Waarde'].sum() * -1

        all_years_upto_current_df = stock_df[stock_df['Datum'].dt.year <= year]
        total_stocks_at_end_of_year = all_years_upto_current_df['Aantal'].sum()
        # Calculate the worth of stocks at the end of the year
        end_of_year_worth = total_stocks_at_end_of_year * end_of_year_stock_price

        # Calculate the virtual gain value
        virtual_gain_value = end_of_year_worth - start_of_year_worth - total_purchase_price_this_year
        # Calculate the virtual gain percentage compared to total invested
        if start_of_year_worth + total_purchase_price_this_year != 0:
            virtual_gain_percentage = (virtual_gain_value / (
                    start_of_year_worth + total_purchase_price_this_year)) * 100
        else:
            virtual_gain_percentage = 0

        yearly_gains[year] = {'virtual_gain_value': virtual_gain_value,
                              'virtual_gain_percentage': virtual_gain_percentage}
    return yearly_gains


def calculate_multi_year_gain() -> None:
    filename = "transactions.csv"
    df = pd.read_csv(filename)
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d-%m-%Y')
    unique_stocks = df['Product'].unique()

    for stock in unique_stocks:
        print(f"{'=' * 50}\nCalculating for {stock}\n{'=' * 50}")

        stock_df = df[df['Product'] == stock]
        isin = stock_df['ISIN'].iloc[0]
        ticker = isin_to_ticker(open_figi_api_key, isin)

        if ticker is None:
            print(f"Unable to find data for {isin}")
            continue

        complete_ticker = f"{ticker}.AS"

        unique_years = populate_unique_years(stock_df)

        yearly_prices = fetch_yearly_stock_prices(complete_ticker, unique_years)
        final_stock_price = yearly_prices[unique_years[-1]]['end_price']

        total_gain_percent, total_gain_value, final_worth = calculate_current_worth(stock_df, final_stock_price)

        yearly_gains = calculate_yearly_gains(stock_df, yearly_prices, unique_years)

        all_stocks_owned_today = stock_df['Aantal'].sum()
        total_invested = stock_df['Waarde'].sum() * -1

        print(f"Total Gain: {total_gain_percent:.2f}% (€{total_gain_value:.2f})")
        print(f"Total Invested: €{total_invested:.2f}")
        print(f"Current Worth: €{final_worth:.2f}")
        print(f'Stocks in possession today: {all_stocks_owned_today}')

        for year, data in yearly_gains.items():
            print(f"Year {year}:")
            print(f"  Virtual Gain {data['virtual_gain_percentage']:.2f}.% (: €{data['virtual_gain_value']:.2f})")


if __name__ == "__main__":
    calculate_multi_year_gain()
