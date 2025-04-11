import pandas as pd

def get_stocks_with_low_rsi():
    """
    模拟获取 RSI 指标小于 20 的股票列表
    """
    # 模拟股票数据
    stocks = [
        {"code": "000001", "name": "平安银行", "rsi": 18},
        {"code": "000002", "name": "万科A", "rsi": 25},
        {"code": "000003", "name": "国农科技", "rsi": 15},
        {"code": "000004", "name": "招商银行", "rsi": 10},
    ]

    # 筛选 RSI 小于 20 的股票
    low_rsi_stocks = [stock for stock in stocks if stock["rsi"] < 20]
    return low_rsi_stocks
