from datetime import date
import io
from typing import Optional, Dict, Union, List, IO
import requests
import json
import pandas as pd
import yfinance as yf
open_figi_api_key = "paste_open_figi_api_key_here"





def check_and_convert_csv_headers(csv_file: IO[str]) -> pd.DataFrame:
    """
    The degiro app may export the headers in a different language that may break this script depending on app lanuage.
    This functions checks if the headers are correct (Dutch) If they are not they convert the headers to Dutch if the
    length of the headers is the same.

    Raises a ValueError if the CSV file headers are neither matching nor have
    the same column count as the expected headers.

    Args:
        csv_file (IO[str]): The input CSV file.

    Returns:
        pd.DataFrame: A DataFrame with standardized headers.
    """

    csv_data = csv_file.read().decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_data))

    expected_headers = ("Datum,Tijd,Product,ISIN,Beurs,Uitvoeringsplaats,Aantal,Koers,,Lokale waarde,,Waarde,,"
                        "Wisselkoers,Transactiekosten en/of,,Totaal,,Order ID")
    expected_headers_list = expected_headers.split(',')

    if ','.join(df.columns) == expected_headers:
        return df
    elif len(df.columns) == len(expected_headers_list):
        df.columns = expected_headers_list
        return df
    else:
        raise ValueError(
            "The CSV file headers are not as expected and their count does not match the expected headers.")


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


def fetch_yearly_stock_prices(ticker: str, unique_years: List[int]) -> Dict[int, Dict[str, Union[float, None]]]:
    """
    Function that takes in the unique years in which the data for stocks should be collected.
    It then returns a dictionary that has the years as keys and the start, mid, Q1 end, Q3 end, and close prices
    of that stock for the year.
    :param ticker: ticker + exchange code (VUSA.AS)
    :param unique_years: list containing integers of the years to be fetched
    :return: A dictionary containing a dictionary that returns the open, mid, Q1 end, Q3 end, and
    close prices for a given year
    """
    yearly_prices = {}
    start_date = f"{min(unique_years)}-01-01"
    end_date = f"{max(unique_years)}-12-31"

    if pd.to_datetime(end_date) > pd.to_datetime(date.today()):
        end_date = date.today().strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start_date, end=end_date, threads=True)

    if data.empty:
        return yearly_prices

    for year in unique_years:
        year_data = data.loc[f"{year}-01-01":f"{year}-12-31"]

        if not year_data.empty:
            start_price = year_data.iloc[0]['Close']

            mid_price = year_data.loc[f"{year}-06-30":f"{year}-06-30"]['Close']
            mid_price = mid_price.iloc[0] if not mid_price.empty else None

            q1_end_price = year_data.loc[f"{year}-03-01":f"{year}-03-01"]['Close']
            q1_end_price = q1_end_price.iloc[0] if not q1_end_price.empty else None

            q3_end_price = year_data.loc[f"{year}-10-01":f"{year}-10-01"]['Close']
            q3_end_price = q3_end_price.iloc[0] if not q3_end_price.empty else None

            end_price = year_data.iloc[-1]['Close']

            yearly_prices[year] = {
                'start_price': start_price,
                'mid_price': mid_price,
                'Q1_end': q1_end_price,
                'Q3_end': q3_end_price,
                'end_price': end_price
            }

    return yearly_prices
