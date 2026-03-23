import yfinance as yf
import pandas_ta as ta
import pandas as pd


class GettingStockData:
    def __init__(self, stock_code):
        self.stock_code = stock_code + ".VN"
        self.df = None

    def get_data(self, start_date, end_date) -> "GettingStockData":
        self.df = yf.download(
            self.stock_code,
            start=start_date,
            end=end_date,
            auto_adjust=False
        )
        self.df.columns = self.df.columns.get_level_values(0)
        self.df = self.df.reset_index()
        self.df['Medium'] = (self.df['High'] + self.df['Low'] + self.df['Close'] + self.df['Open']) / 4
        return self

    def get_rsi(self, length=14) -> "GettingStockData":
        self.df["RSI"] = ta.rsi(self.df["Close"], length=length)
        return self

    def get_choppy(self) -> "GettingStockData":
        self.df["Choppy"] = ta.chop(self.df["High"], self.df["Low"], self.df["Close"])
        return self

    def get_current_data(self) -> pd.Series:
        if self.df is None or self.df.empty:
            raise ValueError("DataFrame is empty. Please call get_data() first.")

        return self.df.iloc[-1]
