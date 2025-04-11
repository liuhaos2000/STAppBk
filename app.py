from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from trading.strategy import execute_strategy
from trading.stocks import get_stocks_from_codes, get_stock_analysis, get_stock_strategy
from trading.rsi_search import get_stocks_with_low_rsi  # 导入 RSI 搜索逻辑
from auth import requires_auth
from config import Config
import logging

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求
app.config.from_object(Config)

# 设置日志记录
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    logging.info("Home route accessed")
    return "Welcome to Quant Trading App"

@app.route('/api/execute_strategy', methods=['POST'])
@requires_auth
def execute_trading_strategy():
    logging.info("Executing trading strategy")
    try:
        # 获取请求中的 JSON 数据
        data = request.json
        # 执行交易策略
        result = execute_strategy(data)
        # 返回 JSON 响应
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error executing trading strategy: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks', methods=['POST'])
def stocks():
    try:
        # 从请求体中获取股票代码列表
        stock_codes = request.json.get("codes", [])
        if not stock_codes:
            # 如果没有提供股票代码，返回空数据
            return jsonify({"success": True, "data": []})

        # 调用 get_stocks_from_codes 方法获取股票信息
        stock_data = get_stocks_from_codes(stock_codes)
        return jsonify({"success": True, "data": stock_data})
    except Exception as e:
        logging.error(f"Error fetching stocks: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks/<symbol>', methods=['GET'])
def stock_detail(symbol):
    try:
        stock = get_stock_detail(symbol)
        if stock:
            return jsonify(stock)
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching stock detail for {symbol}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks/<symbol>/analysis', methods=['GET'])
def stock_analysis(symbol):
    try:
        analysis = get_stock_analysis(symbol)
        if analysis:
            return jsonify(analysis)
        else:
            return jsonify({"error": "Stock analysis not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching stock analysis for {symbol}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks/<symbol>/strategy', methods=['GET'])
def stock_strategy(symbol):
    try:
        strategy = get_stock_strategy(symbol)
        if strategy:
            return jsonify(strategy)
        else:
            return jsonify({"error": "Stock strategy not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching stock strategy for {symbol}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks/<symbol>/chart', methods=['GET'])
def stock_chart(symbol):
    try:
        logging.info(f"Generating stock chart for {symbol}")
        chart_path = generate_stock_chart(symbol)
        if chart_path:
            return send_file(chart_path, mimetype='image/png')
        else:
            return jsonify({"error": "Stock chart not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching stock chart for {symbol}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/stocks/search-rsi', methods=['GET'])
def search_rsi():
    try:
        # 调用 RSI 搜索逻辑
        stocks = get_stocks_with_low_rsi()
        return jsonify({"success": True, "data": stocks})
    except Exception as e:
        logging.error(f"Error searching RSI: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# 全局错误处理
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # 启动 Flask 应用，启用调试模式
    app.run(debug=True)