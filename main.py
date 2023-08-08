import requests
from dotenv import load_dotenv
import os


# -------------------- CONSTANTS --------------------
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# -------- LOADING THE ENVIRONMENT VARIABLES --------
load_dotenv(".env")
STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()

alpha_data = response.json()
time_series = alpha_data["Time Series (Daily)"]

closing_stock_price = [value for (key, value) in time_series.items()]
yesterday_data = closing_stock_price[0]
yesterday_closing_price = yesterday_data["4. close"]
yesterday_closing_price = float(yesterday_closing_price)

day_before_yesterday = closing_stock_price[1]
day_before_yesterday_closing_price = float(day_before_yesterday["4. close"])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)

diff_percent = (difference / yesterday_closing_price) * 100
print(diff_percent)

if diff_percent > 0:
    print("Get News")

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

