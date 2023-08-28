import numpy as np
import pandas as pd
from datetime import date
import requests
import json
import io
import yfinance as yf
from typing import Optional, Dict, Union, List, Tuple

open_figi_api_key = "paste_open_figi_api_key_here"


def fetch_stock_price_yfinance(stock_ticker_and_exchange: str, date_to_fetch: str) -> Optional[float]:
    """
    Uses the yfinance library to get the closing stock price on the given date.
    :param stock_ticker_and_exchange: stocker ticker and exchange in format VUSA.AS
    :param date_to_fetch: date to fetch in string format
    :return: The closing stock price of that or the nearest day (float) or None
    """
    try:
        # Yfinance does not support querying a single day. The lowest unit it can query is a month.
        # Hence, we will get the whole month and fetch our date of interest, if the date does not exist we pick the
        # closest date.
        start_date = (pd.to_datetime(date_to_fetch) - pd.DateOffset(days=15)).strftime('%Y-%m-%d')
        end_date = (pd.to_datetime(date_to_fetch) + pd.DateOffset(days=15)).strftime('%Y-%m-%d')

        # Query yfinance for the data
        data = yf.download(stock_ticker_and_exchange, start=start_date, end=end_date, progress=False)

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
    """
    Converts to ISIN code from the CSV file to a ticket. It openfigi has an api that can do exactly this
    :param openfigi_apikey: optional, used to bypass rate limits
    :param isin: the isin code from the csv file
    :return: string containing the ticker or none
    """
    url = "https://api.openfigi.com/v2/mapping"
    headers = {'Content-Type': 'text/json', 'openfigi-apikey': openfigi_apikey}
    payload = json.dumps([{'idType': 'ID_ISIN', 'idValue': isin}])
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]['data'][0].get('ticker', None) if 'data' in data[0] else None
    return None


def fetch_yearly_stock_prices(ticker: str, unique_years: list) -> Dict[int, Dict[str, Union[float, None]]]:
    """
    Function that takes in the unique years in which the data for stocks should be collected. It then returns a
    dictionary that has the years as keys and the start and close prices of that stock for the year.
    This function eliminates unnecessary API calls by setting the end date of the previous year as the start date of
    the next.
    :param ticker: ticker + exchange code (VUSA.AS)
    :param unique_years: list containing integers of the years to be fetched
    :return: A dictionary containing a dictionary that returns the open and close prices for a given year
    """
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
    """
    In case transactions do not exist for a stock in a given year the missing years will be added to the list.
    :param stock_df:
    :return: list with the possibly missing years
    """
    unique_years = sorted(list(stock_df['Datum'].dt.year.unique()) + [date.today().year])
    min_year = min(unique_years)
    max_year = max(unique_years)
    all_years = list(range(min_year, max_year + 1))
    return sorted(set(all_years + unique_years))


def calculate_current_worth(stock_df: pd.DataFrame, final_stock_price: float) -> Tuple[float, float, float]:
    """
    Calculates the total gain percentual, total gane value and total  worth of a stock based on the price and
    amount of stock owned
    :param stock_df: CSV file contents for a specific stock in dataframe format
    :param final_stock_price: Stock price at the point we are calculating for
    :return: A list containing the three return values (floats)
    """
    all_stocks_owned_today = stock_df['Aantal'].sum()
    final_worth = final_stock_price * all_stocks_owned_today
    total_invested = stock_df['Waarde'].sum() * -1
    total_gain_value = final_worth - total_invested
    total_gain_percent = ((final_worth / total_invested) - 1) * 100 if total_invested != 0 else 0
    return total_gain_percent, total_gain_value, final_worth


def calculate_yearly_gains(stock_df: pd.DataFrame, yearly_prices: Dict[int, Dict[str, Union[float, None]]],
                           unique_years: List[int]) -> Dict[int, Dict[str, float]]:
    """
    Calculates and returns a dictionary containing the amount of money and percent gained or lost on a stock,
    per year that the stock is held.
    :param stock_df: CSV file contents for a specific stock in dataframe format
    :param yearly_prices: Open and close prices per year dictionary for a given stock
    :param unique_years: Years for which to calculate
    :return: A dictionary contain the unrealized gain in percent and value per year
    """
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


def calculate_yearly_worth(stock_df: pd.DataFrame, yearly_prices: Dict[int, Dict[str, float]],
                           unique_years: List[int]) -> Dict[int, int]:
    """
    Calculates the value of the stock held at the end of the year for all the years the stock was in possession.
    :param stock_df: CSV file contents for a specific stock in dataframe format
    :param yearly_prices: Open and close prices per year dictionary for a given stock
    :param unique_years: Years for which to calculate
    :return: Dictionary containing the year as a key and the worth as value
    """
    yearly_worth = {}  # Dictionary to store the worth of stocks at the end of each year
    for year in unique_years:
        end_of_year_stock_price = yearly_prices[year]['end_price']
        all_years_upto_current_df = stock_df[stock_df['Datum'].dt.year <= year]
        total_stocks_at_end_of_year = all_years_upto_current_df['Aantal'].sum()
        end_of_year_worth = total_stocks_at_end_of_year * end_of_year_stock_price
        yearly_worth[year] = int(end_of_year_worth)
    return yearly_worth


def calculate_multi_year_gain(csv_file) -> dict:
    csv_data = csv_file.read().decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_data))
    df['Datum'] = pd.to_datetime(df['Datum'], format='%d-%m-%Y')
    unique_stocks = df['Product'].unique()

    exchange_codes = ['AS', 'DE', 'XC', 'L', 'AQ']

    results = []  # List to store results for each stock
    total_worth_all_stocks = 0
    total_gain_all_stocks = 0
    total_invested_all_stocks = 0

    for stock in unique_stocks:
        stock_result = {}  # Dictionary to store results for the current stock

        stock_df = df[df['Product'] == stock]
        isin = stock_df['ISIN'].iloc[0]
        ticker = isin_to_ticker(open_figi_api_key, isin)

        if ticker is None:
            stock_result['stock_name'] = stock
            stock_result['error'] = f"Unable to find data for {isin}"
            results.append(stock_result)
            continue

        unique_years = populate_unique_years(stock_df)
        yearly_prices = {}
        for exchange_code in exchange_codes:
            complete_ticker = f"{ticker}.{exchange_code}"
            yearly_prices = fetch_yearly_stock_prices(complete_ticker, unique_years)
            if yearly_prices:
                break

        if not yearly_prices:
            continue

        final_stock_price = yearly_prices[unique_years[-1]]['end_price']

        total_gain_percent, total_gain_value, final_worth = calculate_current_worth(stock_df, final_stock_price)

        total_worth_all_stocks += final_worth
        total_gain_all_stocks += total_gain_value

        yearly_gains = calculate_yearly_gains(stock_df, yearly_prices, unique_years)

        all_stocks_owned_today = stock_df['Aantal'].sum()
        total_invested = stock_df['Waarde'].sum() * -1

        total_invested_all_stocks += total_invested

        stock_result['stock_name'] = stock
        stock_result['total_gain_percent'] = total_gain_percent
        stock_result['total_gain_value'] = total_gain_value
        stock_result['total_invested'] = total_invested
        stock_result['final_worth'] = final_worth
        stock_result['stocks_in_possession'] = all_stocks_owned_today
        stock_result['yearly_gains'] = yearly_gains
        stock_result['yearly_worth'] = calculate_yearly_worth(stock_df, yearly_prices, unique_years)

        results.append(stock_result)

    summary = {
        'total_worth': round(total_worth_all_stocks, 2),
        'total_gain': round(total_gain_all_stocks, 2),
        'total_gain_percentage': round((total_worth_all_stocks / total_invested_all_stocks  - 1) * 100, 2)
    }

    return {'results': results, 'summary': summary}
