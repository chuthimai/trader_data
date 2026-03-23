from datetime import datetime, timedelta
import requests
import os
from getting_data.getting_stock_data import GettingStockData


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def get_current_data(stock_code: str):
    # ngày hôm nay
    END_DATE = datetime.today().strftime("%Y-%m-%d")

    # ngày trước hôm nay 150 ngày ~ 6 tháng
    START_DATE = (datetime.today() - timedelta(days=150)).strftime("%Y-%m-%d")

    stock_data = GettingStockData(stock_code).get_data(
        start_date=START_DATE,
        end_date=END_DATE,
    ).get_rsi(length=14).get_choppy().get_current_data()

    return stock_data


def format_stock(stock_code, data):
    low = data["Low"]
    high = data["High"]
    rsi = data["RSI"]
    choppy = data["Choppy"]

    # xác định lệnh
    command = None

    if choppy < 40:
        if rsi > 40:
            command = "SELL"
        elif rsi < 40:
            command = "BUY"

    if command is None:
        return None

    return f"{stock_code} | {low:.0f} | {high:.0f} | {rsi:.2f} | {choppy:.2f} | {command}"


if __name__ == '__main__':
    stock_codes = ["E1VFVN30", "FUEVFVND", "FUEMAV30", "FUESSV30", "FUEKIV30"]

    results = []
    for stock_code in stock_codes:
        data = get_current_data(stock_code)
        row = format_stock(stock_code, data)
        if row is None:
            continue
        results.append(row)

    if results:
        message = "CODE | LOW | HIGH | RSI | CHOPPY | SIGNAL\n"
        message += "\n".join(results)
        send_message(message)

