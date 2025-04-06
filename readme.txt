
1，后端
Flask==3.1.0
pandas==2.2.3
numpy==2.2.3

启动虚拟环境
cd /Users/lh01/10_App/STAppBk
python3 -m venv venv
source venv/bin/activate

安装
pip install -r requirements.txt

启动
python app.py





2，前端
cd /Users/lh01/10_App/STApp
npx react-native run-ios



现在我想修改这个股票列表画面MainScreen.js。 和它的后台程序，stocks.py的get_stocks方法。

我希望对股票列表的代码进行持久化，持久化在前端做。 当股票列表画面显示时候，画面去获取持久化的股票代码一览，然后传给后台程序，后台程序通过akshear接口，获取最新的股票信息返回给前端。前端页面把信息显示到画面上。

另外，我希望在股票列表画面的最上方，添加一个输入框和一个按钮，用户可以在输入框输入股票代码，然后点击按钮来来更新持久化列表，然后刷新页面获取最新数据。

画面显示的列表要求，显示股票代码，股票名称，当前价格，涨跌幅。 然后是现在的详情按钮不变。另外在详情按钮边上加个删除按钮，点击删除的时候可以从持久化的列表删除，然后刷新页面。

请你帮我修改后端get_stocks的方法。 和前端代码以及相关其他代码。