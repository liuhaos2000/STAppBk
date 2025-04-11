import pandas as pd
from trading.stocks import get_stock_analysis  # 修正导入路径

def get_stocks_with_low_rsi():
    return get_a50_stocks_with_low_rsi()





# 定义中国A50股票代码列表
A50_STOCKS = [
    "600519", "601318", "300750", "600036", "000858", "000333", "600276", "600030", "601888", "601012",
    "600900", "000001", "600887", "601398", "601628", "600309", "000651", "601899", "600585", "600048",
    "601288", "601601", "601688", "601166", "601988", "600028", "601857", "601818", "601319", "600104",
    "601668", "601390", "601766", "600029", "601633", "600745", "600436", "600196", "600276", "600570",
    "601888", "601012", "600900", "000001", "600887", "601398", "601628", "600309", "000651", "601899"
]

def get_a50_stocks_with_low_rsi():
    """
    获取 A50 股票中 RSI 小于 20 的股票
    """
    low_rsi_stocks = []

    for stock_code in A50_STOCKS:
        analysis_data = get_stock_analysis(stock_code)
        if analysis_data and analysis_data["rsi"]:
            # 获取 RSI 数据中最后一个值
            last_rsi = round(analysis_data["rsi"][-1]["value"])  # 对 RSI 值进行四舍五入
            if last_rsi < 20:
                low_rsi_stocks.append({
                    "code": stock_code,
                    "rsi": last_rsi
                })

    return low_rsi_stocks

if __name__ == "__main__":
    # 打印 A50 中 RSI 小于 20 的股票
    low_rsi_stocks = get_a50_stocks_with_low_rsi()
    print("A50 中 RSI 小于 20 的股票:")
    for stock in low_rsi_stocks:
        print(stock)
