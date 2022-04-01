import matplotlib.pyplot as plt
import pandas as pd
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


# def demo():
#     x = [1, 2, 3, 4]
#     y = [4, 5, 6, 7]
#     plt.xlabel("日期")
#     plt.ylabel("价格")
#     plt.title("图表")
#     plt.figure(num='vae', figsize=(10, 3), dpi=75, facecolor='#FFFFFF', edgecolor='#0000FF')
#     plt.xlim(0, 10)
#     plt.ylim(0, 10)
#     plt.legend()
#     plt.plot(x, y)
#     plt.show()
#
#
# if __name__ == '__main__':
#     demo()


def read_data(path):
    data = []
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        # 筛选你想要的数据
        data.append([row['tradeDate'], row['closePrice']])
    return data


def read_volume_data(path):
    data = []
    df = pd.read_csv(path)
    for index, row in df.iterrows():
        # 筛选你想要的数据
        data.append([row['tradeDate'], row['turnoverVol'], row['openPrice'], row['closePrice']])
    return data


def draw_price():
    data = read_data("./600036_half_year.csv")
    time = [line[0] for line in data]
    price = [line[1] for line in data]
    # 画布属性设置，分辨率参数-dpi，画布大小参数-figsize
    plt.figure(dpi=80, figsize=(20, 10))
    # 定义title, x y轴
    plt.title('Price Line')
    plt.xlabel('Time')
    # 设置x轴每隔15隔显示坐标
    plt.xticks(range(0, len(time), 15))
    plt.ylabel('Price')
    # 分别设置x, y轴数据
    plt.plot(time, price, 'k-')
    plt.show()


def draw_volume():
    data = read_volume_data("./600036_half_year.csv")
    time = [line[0] for line in data]
    volume = [line[1] for line in data]
    openprice = [line[2] for line in data]
    closeprice = [line[3] for line in data]
    plt.figure(dpi=80, figsize=(20, 10))
    # 定义title, x y轴
    plt.xlabel('Time')
    # 设置x轴每隔15隔显示坐标
    plt.ylabel('Volume')
    plt.bar(np.arange(0, len(time)), volume,
            color=['g' if openprice[x] > closeprice[x] else 'r' for x in
                   range(0, len(time))])
    plt.xticks(np.arange(0, len(time), 15), time)
    plt.savefig("test.png")
    plt.show()


# def draw2():
#     x = np.arange(1, 100, 1)
#     fig = plt.figure()
#     ax1 = fig.add_subplot(121)
#     ax1.plot(x, x)
#     ax2 = fig.add_subplot(122)
#     ax2.plot(x, x ** 2)
#     plt.savefig("test2.png")
#     plt.show()


if __name__ == '__main__':
    pass
