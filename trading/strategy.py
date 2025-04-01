import pandas as pd
import numpy as np

def execute_strategy(data):
    # 将传入的数据转换为DataFrame
    df = pd.DataFrame(data)
    
    # 示例策略：简单移动平均线策略
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    
    # 生成交易信号
    df['signal'] = 0
    df['signal'][10:] = np.where(df['SMA_10'][10:] > df['SMA_50'][10:], 1, 0)
    df['position'] = df['signal'].diff()
    
    return df.to_dict(orient='records')