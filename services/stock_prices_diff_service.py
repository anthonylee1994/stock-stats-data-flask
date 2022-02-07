from pandas import DataFrame
import yfinance as yf


class StockPriceDiffService:
    def __init__(self, symbol: str, interval='1mo') -> None:
        self.symbol = symbol
        self.ticker = yf.Ticker(self.symbol)
        self.stock_prices = None
        self.interval = interval

    def get_stock_prices_diff(self) -> DataFrame:
        df = self.ticker.history(interval=self.interval, start='1970-01-01')
        df.dropna(how='all', inplace=True)
        df['price'] = df['Close']
        df['diff'] = (((
            df['Close'].shift(-1) - df['Close']) /
            df['Close']
        ) * 100).round()

        df.index = df.index.strftime('%Y-%m-%d')
        return df[['price', 'diff']].dropna(how='any')

    def get_stock_prices_diff_stats(self) -> DataFrame:
        df = self.get_stock_prices_diff()['diff'].describe(
        ).rename_axis('unique_values').to_frame('summary')
        return df

    def get_stock_prices_diff_histogram(self) -> DataFrame:
        df = self.get_stock_prices_diff()['diff'].value_counts(
        ).rename_axis('unique_values').to_frame('counts')
        df.sort_index(inplace=True)
        return df
