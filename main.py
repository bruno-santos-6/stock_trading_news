import requests
from dotenv import load_dotenv
import os
from twilio.rest import Client

# -------------------- CONSTANTS --------------------
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# -------- LOADING THE ENVIRONMENT VARIABLES --------
load_dotenv(".env")
STOCK_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API")

TWILIO_ACCOUNT_SID = os.getenv("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")
MY_TWILIO_VERIFIED_NUMBER = os.getenv("TWILIO_VIRTUAL_NUMBER")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
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

difference = yesterday_closing_price - day_before_yesterday_closing_price

up_down = None

if difference > 0:
    up_down = "🔼📈"
else:
    up_down = "🔻📈"

diff_percent = round((difference / yesterday_closing_price) * 100)

if abs(diff_percent) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=MY_TWILIO_VERIFIED_NUMBER
        )