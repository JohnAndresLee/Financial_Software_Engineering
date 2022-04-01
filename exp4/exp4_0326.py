import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


def read_data():
    df = pd.read_csv("600036_half_year.csv")
    data = []
    for index, row in df.iterrows():
        data.append([row['tradeDate'], row['highestPrice'], row['lowestPrice'], row['openPrice'], row['closePrice'],
                     row['turnoverVol']])
    return data


def draw_candle_volume():
    data = read_data()
    time = np.array([line[0] for line in data])
    highestprice = np.array([line[1] for line in data])
    lowestprice = np.array([line[2] for line in data])
    openprice = np.array([line[3] for line in data])
    closeprice = np.array([line[4] for line in data])
    volume = np.array([line[5] for line in data])

    colors_bool = closeprice > openprice
    bar_colors = np.zeros(colors_bool.size, dtype="U5")
    bar_colors[:] = "g"
    bar_colors[colors_bool] = "w"

    edge_colors = np.zeros(colors_bool.size, dtype="U1")
    edge_colors[:] = "g"
    edge_colors[colors_bool] = "r"

    fig = plt.figure(dpi=200, figsize=(20, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    ax1 = plt.subplot(gs[0])
    plt.title("600036 招商银行 K线图", fontsize=20)

    ax1.set_ylabel("价格", fontsize=20)

    ax1.vlines(time, lowestprice, highestprice, colors=edge_colors)
    ax1.bar(time, (closeprice - openprice), bottom=openprice, color=bar_colors,
            edgecolor=edge_colors, zorder=3)

    ax1.tick_params(axis='x', rotation=30, labelsize=12)
    ax1.grid(linestyle=":")
    ax1.tick_params(axis='y', labelsize=12)
    ax1.set_xticks(np.arange(0, len(time), 15))
    fig.subplots_adjust(hspace=0)

    ma10 = [None, None, None, None, None, None, None, None, None, None]
    ma5 = [None, None, None, None, None]
    ma20 = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None]
    for i in range(10, len(closeprice)):
        ma10.append(sum(closeprice[i - 10:i]) / 10)
    for i in range(5, len(closeprice)):
        ma5.append(sum(closeprice[i - 5:i]) / 5)
    for i in range(20, len(closeprice)):
        ma20.append(sum(closeprice[i - 20:i]) / 20)
    ax1.plot(time, ma5, label='ma5')
    ax1.plot(time, ma10, label='ma10')
    ax1.plot(time, ma20, label='ma20')
    ax1.legend(fontsize=18)

    # ax2 = fig.add_subplot(212)
    ax2 = plt.subplot(gs[1])
    # 定义title, x y轴
    ax2.set_xlabel('日期', fontsize=20)
    # 设置x轴每隔15隔显示坐标
    ax2.set_ylabel('成交量', fontsize=20)
    ax2.bar(time, volume,
            color=['g' if openprice[x] > closeprice[x] else 'r' for x in
                   range(0, len(time))])
    ax2.tick_params(axis='x', rotation=30, labelsize=12)
    ax2.set_xticks(np.arange(0, len(time), 15))
    ax2.grid(linestyle=":")
    plt.savefig("exp4.png")
    plt.show()


if __name__ == '__main__':
    draw_candle_volume()
    print("ok")
