from flask import Blueprint, request
from services.stock_prices_diff_service import StockPriceDiffService


stocks_controller = Blueprint('stocks_controller', __name__)


def get_interval():
    interval = request.args.get('interval')
    return '1mo' if interval is None else interval


@stocks_controller.route('/stock-prices-diff/<symbol>')
def stock_prices_diff(symbol):
    return StockPriceDiffService(symbol, get_interval()).get_stock_prices_diff().to_json()


@stocks_controller.route('/stock-prices-diff-histogram/<symbol>')
def stock_prices_diff_histogram(symbol):
    return StockPriceDiffService(symbol, get_interval()).get_stock_prices_diff_histogram().to_json()


@stocks_controller.route('/stock-prices-diff-stats/<symbol>')
def stock_prices_diff_stats(symbol):
    return StockPriceDiffService(symbol, get_interval()).get_stock_prices_diff_stats().to_json()
