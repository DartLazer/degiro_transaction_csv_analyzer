# Multi-Year Stock Gain Calculator

This Python script calculates multi-year gains for stocks based on transactions recorded in a CSV file. It uses the
Yahoo Finance API via the yfinance library to fetch stock prices and the OpenFIGI API to convert ISINs to tickers.

The CSV should be the exported CSV from Degiro Transactions in Dutch for now. I will work on English support later.
If it is in English please correct the headers as follows:

`Datum,Tijd,Product,ISIN,Beurs,Uitvoeringsplaats,Aantal,Koers,,Lokale waarde,,Waarde,,Wisselkoers,Transactiekosten
en/of,,Totaal,,Order ID`

## Installation

1. Clone the repository:

   `git clone https://github.com/yourusername/project-name.git`

2. Navigate to the project directory:

3. Install the required dependencies:

   `pip install -r requirements.txt`

4. Obtain an OpenFIGI API key and replace 'paste_open_figi_api_key_here' with your actual API key in
   the `open_figi_api_key` variable in the code.

5. The CSV should be the exported CSV from Degiro Transactions in Dutch for now. I will work on English support later.
If it is in English please correct the headers as follows:

   `Datum,Tijd,Product,ISIN,Beurs,Uitvoeringsplaats,Aantal,Koers,,Lokale waarde,,Waarde,,Wisselkoers,Transactiekosten
en/of,,Totaal,,Order ID`

6. Place the csv in the project directory and call it 'transactions.csv'

## Usage

1. Ensure your transaction data CSV file is correctly formatted.

2. Run the script:

   `python main.py`

3. The script will calculate and display multi-year gains for each stock in the CSV file.

## Author

This script is created by [Rik Beernink](https://github.com/DartLazer) from [Sky-T](https://www.sky-t.nl).

## Contributions

Contributions to this script are welcome! If you'd like to contribute, follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

   `git checkout -b feature-new-feature`

3. Make your changes, commit them, and push to your fork:

   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature-new-feature```

4. Create a pull request on the original repository.

Feel free to enhance and improve the script for better functionality and usability!

Remember to replace 'paste_open_figi_api_key_here' with your actual OpenFIGI API key in the code and ensure that you
have the required CSV file in the specified format for the script to work correctly.

Feel free to reach out if you have any further questions or need assistance with anything else!
