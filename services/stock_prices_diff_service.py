import json
from pandas import DataFrame
import yfinance as yf


class StockPriceDiffService:
    def __init__(self, symbol: str, interval='1mo') -> None:
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self.stock_prices = None
        self.interval = interval
        self.cached_historical_prices: DataFrame = None

    def get_historical_price(self) -> DataFrame:
        if self.cached_historical_prices is None:
            self.cached_historical_prices = self.ticker.history(
                interval=self.interval, start='1970-01-01')
        return self.cached_historical_prices.copy()

    def get_stock_prices_diff(self) -> DataFrame:
        df = self.get_historical_price()
        df.dropna(how='all', inplace=True)
        df['price'] = df['Close']
        df['diff'] = (((
            df['Close'].shift(-1) - df['Close']) /
            df['Close']
        ) * 100).round()

        df.index = df.index.strftime('%Y-%m-%d')
        return df[['price', 'diff']].dropna(how='any')

    def get_stock_prices_diff_for_previous_diff(self, previous_diff: int) -> DataFrame:
        df = self.get_stock_prices_diff()
        df.reset_index(inplace=True)
        df.rename(columns={'Date': 'date'}, inplace=True)

        next_record_indices = df[df['diff'] == previous_diff].index + 1
        next_record_indices = next_record_indices[next_record_indices < len(
            df)]

        df = df.iloc[next_record_indices]
        df.set_index('date', inplace=True)
        return df[['price', 'diff']].dropna(how='any')

    def get_stock_prices_diff_for_previous_diff_stats(self, previous_diff: int) -> DataFrame:
        df = self.get_stock_prices_diff_for_previous_diff(previous_diff)[
            'diff'].describe(
        ).rename_axis('unique_values').to_frame('summary')
        return df

    def get_stock_prices_diff_for_previous_diff_histogram(self, previous_diff: int) -> DataFrame:
        df = self.get_stock_prices_diff_for_previous_diff(previous_diff)[
            'diff'].value_counts().rename_axis('unique_values').to_frame('counts')
        df.sort_index(inplace=True)
        return df

    def get_stock_prices_diff_stats(self) -> DataFrame:
        df = self.get_stock_prices_diff()['diff'].describe(
        ).rename_axis('unique_values').to_frame('summary')
        return df

    def get_stock_prices_diff_histogram(self) -> DataFrame:
        df = self.get_stock_prices_diff()['diff'].value_counts(
        ).rename_axis('unique_values').to_frame('counts')
        df.sort_index(inplace=True)
        return df

    def get_stock_prices_diff_2d(self) -> DataFrame:
        return {"counts":  dict((i, json.loads(self.get_stock_prices_diff_for_previous_diff(
            int(i)).to_json())) for i in self.get_stock_prices_diff_histogram().index)}

    def get_stock_prices_diff_stats_2d(self) -> DataFrame:
        return {"counts":  dict((i, json.loads(self.get_stock_prices_diff_for_previous_diff_stats(
            int(i)).to_json())) for i in self.get_stock_prices_diff_histogram().index)}

    def get_stock_prices_diff_histogram_2d(self) -> DataFrame:
        return {"counts":  dict((i, json.loads(self.get_stock_prices_diff_for_previous_diff_histogram(
            int(i)).to_json())) for i in self.get_stock_prices_diff_histogram().index)}
