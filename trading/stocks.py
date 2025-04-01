import os
import logging
from datetime import datetime, timedelta
import akshare as ak
import ta  # 导入 ta 库

def get_stocks():
    # 模拟股票数据
    stocks = [
        {"symbol": "000001", "price": 150},
        {"symbol": "600941", "price": 3400},
    ]
    return stocks

def get_stock_analysis(symbol):
    logging.info(f"Fetching data for {symbol}")  # 添加日志记录

    # 动态计算开始日期和结束日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=60)).strftime('%Y%m%d')

    try:
        # 使用 akshare 获取股票数据
        hist = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="")

    except Exception as e:
        logging.warning(f"Error fetching data for {symbol}: {e}")
        return None

    if hist.empty:
        logging.warning(f"No data found for {symbol}")  # 添加警告日志
        return None

    logging.info(f"Fetched data for {symbol}: {hist.head()}")  # 添加日志记录

    # 计算 MACD 指标
    macd = ta.trend.MACD(hist['收盘'])
    hist['MACD'] = macd.macd()
    hist['MACD_signal'] = macd.macd_signal()
    hist['MACD_diff'] = macd.macd_diff()

    analysis_data = {
        "symbol": symbol,
        "kline": [{"date": row["日期"], "value": row["收盘"]} for index, row in hist.iterrows()],
        "macd": [], 
        "volume": [{"date": row["日期"], "value": row["成交量"]} for index, row in hist.iterrows()],
        "rsi": [],  # 这里可以添加 RSI 计算逻辑
        "signals": []  # 这里可以添加买入卖出信号逻辑
    }
    return analysis_data

# 测试其他股票代码和日期范围
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(get_stock_analysis("000001.SZ"))
    print(get_stock_analysis("600941.SH"))

    # 动态计算开始日期和结束日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y%m%d')

    # 使用 akshare 获取股票数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001.SZ", period="daily", start_date=start_date, end_date=end_date, adjust="")
    print(stock_zh_a_hist_df)

