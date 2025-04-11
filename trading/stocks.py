import os
import logging
from datetime import datetime, timedelta
import akshare as ak
import ta  # 导入 ta 库
import time
import pandas as pd  # 添加 pandas 库

# 全局缓存变量
_cache = {
    "all_stock_info": None,
    "last_fetch_time": 0
}

def get_stocks_from_codes(stock_codes):
    logging.info(f"Fetching stock data for: {stock_codes}")

    stock_data = []
    try:
        # 检查缓存是否过期（60秒）
        current_time = time.time()
        if _cache["all_stock_info"] is None or current_time - _cache["last_fetch_time"] > 60:
            logging.info("Fetching fresh data from ak.stock_zh_a_spot_em")
            _cache["all_stock_info"] = ak.stock_zh_a_spot_em()
            _cache["last_fetch_time"] = current_time
        else:
            logging.info("Using cached data for ak.stock_zh_a_spot_em")

        all_stock_info = _cache["all_stock_info"]
    except Exception as e:
        logging.warning(f"Error fetching all stock data: {e}")
        return stock_data

    for code in stock_codes:
        try:
            # 从获取的所有股票数据中筛选目标股票
            stock_row = all_stock_info[all_stock_info['代码'] == code]
            if not stock_row.empty:
                stock_data.append({
                    "code": code,
                    "name": stock_row.iloc[0]['名称'],
                    "price": stock_row.iloc[0]['最新价'] if not pd.isna(stock_row.iloc[0]['最新价']) else 0,  # 处理 NaN
                    "change": stock_row.iloc[0]['涨跌幅'] if not pd.isna(stock_row.iloc[0]['涨跌幅']) else 0  # 处理 NaN
                })
            else:
                logging.warning(f"Stock code {code} not found in all_stock_info")
        except Exception as e:
            logging.warning(f"Error processing data for {code}: {e}")

    return stock_data

def get_stock_analysis(symbol):
    logging.info(f"Fetching data for {symbol}")  # 添加日志记录

    # 动态计算开始日期和结束日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y%m%d')

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

    # 计算 RSI 指标，使用周期 6
    rsi = ta.momentum.RSIIndicator(hist['收盘'], window=6)
    hist['RSI'] = rsi.rsi()

    # 将 NaN 替换为 0
    hist['RSI'].fillna(0, inplace=True)

    analysis_data = {
        "symbol": symbol,
        "kline": [{"date": row["日期"], "value": row["收盘"]} for index, row in hist.iterrows()],
        "macd": [], 
        "volume": [{"date": row["日期"], "value": row["成交量"]} for index, row in hist.iterrows()],
        "rsi": [{"date": row["日期"], "value": row["RSI"]} for index, row in hist.iterrows()],
        "signals": []  # 这里可以添加买入卖出信号逻辑
    }
    return analysis_data

def get_stock_strategy(symbol):
    logging.info(f"Calculating strategy for {symbol}")

    # 动态计算开始日期和结束日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y%m%d')

    try:
        # 使用 akshare 获取股票数据
        hist = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, end_date=end_date, adjust="")
    except Exception as e:
        logging.warning(f"Error fetching data for {symbol}: {e}")
        return None

    if hist.empty:
        logging.warning(f"No data found for {symbol}")
        return None

    # 计算 RSI 指标
    rsi = ta.momentum.RSIIndicator(hist['收盘'], window=6)
    hist['RSI'] = rsi.rsi()
    hist['RSI'].fillna(0, inplace=True)

    # 策略计算
    results = []
    positions = []  # 当前持仓列表，每个持仓为一个字典

    for i, row in hist.iterrows():
        date = row["日期"]
        price = row["收盘"]
        rsi_value = row["RSI"]

        # 检查是否满足买入条件
        if rsi_value > 0 and rsi_value < 20:  # RSI 为 0 时不买入
            positions.append({"buy_date": date, "buy_price": price})

        # 检查每个持仓是否满足卖出条件
        for position in positions[:]:  # 遍历当前持仓
            if price <= position["buy_price"] * 0.9:  # 止损卖出
                results.append({
                    "buy_date": position["buy_date"],
                    "buy_price": position["buy_price"],
                    "sell_date": date,
                    "sell_price": price,
                    "profit": (price - position["buy_price"]) / position["buy_price"] * 100
                })
                positions.remove(position)  # 移除已卖出的持仓
            elif rsi_value > 80:  # RSI 大于 80 卖出
                results.append({
                    "buy_date": position["buy_date"],
                    "buy_price": position["buy_price"],
                    "sell_date": date,
                    "sell_price": price,
                    "profit": (price - position["buy_price"]) / position["buy_price"] * 100
                })
                positions.remove(position)  # 移除已卖出的持仓

    # 将未卖出的持仓添加到结果中
    for position in positions:
        results.append({
            "buy_date": position["buy_date"],
            "buy_price": position["buy_price"],
            "sell_date": None,
            "sell_price": None,
            "profit": None
        })

    return {"symbol": symbol, "strategy_results": results}



def get_stock_add(symbol):
    return

def get_stock_delete(symbol):
    return






# 测试其他股票代码和日期范围
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(get_stock_analysis("000001"))
    print(get_stock_analysis("600941"))

    # 动态计算开始日期和结束日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y%m%d')

    # 使用 akshare 获取股票数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date=start_date, end_date=end_date, adjust="")
    print(stock_zh_a_hist_df)

