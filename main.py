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
NEWS_API_KEY = os.getenv("NEWS_API")

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

if diff_percent > 0:

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    print(three_articles)

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
