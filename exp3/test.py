import sys
import requests
from datetime import datetime, time
from dateutil.parser import parse
from time import sleep
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

f = open('a.log', 'a+')
sys.stdout = f
sys.stderr = f		# redirect std err, if necessary
print("test")
print("test2")

def getTick():
    """获取最新股票价格"""
    headers = {"Referer": "https://finance.sina.com.cn"}
    response = requests.get(url="https://hq.sinajs.cn/?format=text&list=sz300750", headers=headers)
    stock_info = response.text.strip().split(",")
    last = float(stock_info[3])
    trade_datetime = stock_info[30] + " " + stock_info[31]
    trade_datetime = parse(trade_datetime)  # 将时间字符串转为datetime对象
    tick = (trade_datetime, last)
    return tick


class AstockTrading:
    def __init__(self, strategy_name):
        self.strategy_name = strategy_name
        self.Dt = None
        self.Open = None
        self.High = None
        self.Low = None
        self.Close = None
        self.ma10 = None

        self.money = 100000000
        self.isNewBar = False
        self.current_orders = {}
        self.history_orders = {}
        self.order_number = 0

        # 订单存储格式
        # self.current_orders = {
        #     'order1': {'open_price': 1,
        #                'open_datetime': '2022-03-03 9:30',
        #                'volume': 100,
        #                'close_price': 2,  # 这个是在卖出时才添加的信息，买入时不需要
        #                'close_datetime': 'xxxx'}  # 这个也是
        # }

    def get_history_data_from_local(self):
        # 下面是全局变量，用于存放及构建bar，里面已经填充了一些数据，模拟之前的交易日中的数据，以后我们会正式从文件中读取前面交易日的数据
        self.Dt = [datetime(2022, 3, 2, 14, 59),  # 最前面的位置是当前bar的开始时间
                   datetime(2022, 3, 2, 14, 58),  # 前一个bar的开始时间
                   datetime(2022, 3, 2, 14, 57),
                   datetime(2022, 3, 2, 14, 56),
                   datetime(2022, 3, 2, 14, 55)]
        self.Open = [513.64, 513.64, 513.66, 513.63, 513.70]  # 当前bar的开始时间价格
        self.High = [513.84, 513.64, 513.66, 513.69, 513.70]
        self.Low = [513.64, 513.64, 513.64, 513.48, 513.59]
        self.Close = [513.84, 513.64, 513.64, 513.64, 513.59]  # 当前bar的结束时间价格

    def bar_generate(self, tick):
        """
        根据最新的tick，更新当前bar或者生成一个新的bar
        :param tick: getTick()函数返回的一个元组，(trade_datetime, last)
        :param Dt: List[], [datatime(...), ...]
        :param Open: List[float], [45.79, 45.66, 45.72]
        :param High: List[float], 每个bar的最高价格
        :param Low: List[float], 每个bar的最低价格
        :param Close: List[float], 每个bar的最后价格
        :return: Dt, Open, High, Low, Close
        """

        # 每读取到一个tick，就要把tick[0]-时间存放到Dt的0位置,
        # tick[1]-价格插入Open, High, Low, Close
        # 每1分钟产生一个新的bar,如果每5分钟产生一个新bar，该怎么判断？
        if tick[0].minute != self.Dt[0].minute:
            print("===============Create a new bar!===============")
            print("Bar_ID:", len(self.Dt) + 1)
            # 创建一个新的bar
            self.isNewBar = True
            self.Open.insert(0, tick[1])
            self.High.insert(0, tick[1])
            self.Low.insert(0, tick[1])
            self.Close.insert(0, tick[1])
            self.Dt.insert(0, tick[0])
        else:
            # 更新bar的high/low/close
            self.isNewBar = False
            self.High[0] = max(self.High[0], tick[1])
            self.Low[0] = min(self.Low[0], tick[1])
            self.Close[0] = tick[1]
            self.Dt[0] = tick[0]
        return self.Dt, self.Open, self.High, self.Low, self.Close

    def buy(self):
        order = {}
        if self.money > self.Close[0] * 100:
            order = self.establish_order(0)
            self.current_orders.update(order)
            self.money = self.money - self.Close[0] * 100
            print(order)
        else:
            print("Insufficient Capital!")
        return

    def sell(self):
        order = {}
        if self.current_orders:
            order = self.establish_order(1)
            self.history_orders.update(self.current_orders)
            self.history_orders.update(order)
            self.current_orders = {}
            self.money = self.money + self.Close[0] * len(self.current_orders)
        print(order)
        return

    def establish_order(self, t):
        number = "order"+str(self.order_number)
        d = {}
        subdict = {}
        if t == 0:
            subdict['open_price'] = self.Close[0]
            subdict['open_datetime'] = self.Dt[0]
            subdict['volume'] = 100
        else:
            subdict['close_price'] = self.Close[0]
            subdict['close_datetime'] = self.Dt[0]
            subdict['volume'] = 100*len(self.current_orders)
        d[number] = subdict
        self.order_number += 1
        return d

    def strategy(self):
        """
        根据策略决定是否买入/卖出股票
        :param Close: List[float], 存放每个bar的最后价格，第一个元素代表当前bar的最新价格
        :return: None
        """
        # 朴素策略：最新价格<均价*0.998时买入，>均价*1.002时卖出
        # 根据历史数据，计算出均价(ma10)
        if (not self.isNewBar) | (len(self.Close) < 10):  # TODO: 如果没有10个bar，无法计算ma10，直接return
            return
        # TODO：只有新bar被创建，才需要计算ma10，不用每次都重新计算。且听下回分解
        ma10 = sum(self.Close[1:11]) / 10  # 除了当前正在更新的bar以外，计算之前10个已经生成的bar的均值（20*5分钟）
        if self.Close[0] < 0.998 * ma10:  # Close[0]是最新价格
            print("===============进行买入操作===============")
            self.buy()
        elif self.Close[0] > ma10 * 1.002:
            if 1:  # TODO: 如果之前买过，有long信号，才能卖，没买过是不能卖的。且听下回分解
                print("===============进行卖出操作===============")
                self.sell()
        else:  # 如果在均线5%附近波动，什么也不操作
            pass
        return

    # def draw_bar(self):
    #     fig = plt.figure(figsize=(12, 8))
    #     ax = fig.add_subplot(111)
    #     # 加载数据
    #     df_ma = pd.DataFrame()
    #     original_data = pd.read_csv(r'C:\Users\飘逸\Desktop\600837.csv')
    #     print(original_data)
    #     # 设置显示的交易日数
    #     days = 150
    #     # 生成开盘价、收盘价、最高价、最低价
    #     opens = original_data['Open'][0:days]
    #     closes = original_data['Close'][0:days]
    #     highs = original_data['High'][0:days]
    #     lows = original_data['Low'][0:days]
    #     # 生成时间序列
    #     data_index = original_data['Date'][0:days]
    #     # 使用zip()生成数据列表
    #     ohlc = list(zip(np.arange(0, len(opens)), opens, closes, highs, lows))
    #     # 绘制k线图
    #     mpf.candlestick2_ochl(ax, opens, closes, highs, lows, width=0.6, colorup='r', colordown='g')
    #     # 设置x轴的范围
    #     ax.set_xlim(0, days)
    #     # x轴刻度设置
    #     ax.set_xticks(np.arange(0, days, 20))
    #     # 标签设置为日期
    #     ax.set_xticklabels([data_index[index] for index in ax.get_xticks()])
    #     # 设置轴标签
    #     ax.set_xlabel('Date', fontsize=15)
    #     ax.set_ylabel('Price', fontsize=15)
    #     ax.set_title('600837')
    #     plt.show()


if __name__ == "__main__":
    cur_time = datetime.now()  # datetime库的用法：https://blog.csdn.net/cmzsteven/article/details/64906245
    trade = AstockTrading("mystrategy")
    trade.get_history_data_from_local()
    while time(9, 30) < cur_time.time() < time(15):
        last_tick = getTick()  # 获取最新的股票数据，一般是每3秒更新一次
        # 获得一个最新价格后就去更新bar
        trade.bar_generate(last_tick)
        print(trade.Dt[0], "HIGH:", trade.High[0], "LOW:", trade.Low[0], "CLOSE:", trade.Close[0])
        trade.strategy()
        # 暂停三秒钟
        sleep(3)

