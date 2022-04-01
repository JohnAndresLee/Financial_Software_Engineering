import matplotlib.pyplot as plt
import pandas as pd
from mplfinance.original_flavor import candlestick2_ochl


def draw_bar(data):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    Open = list(data['Open'].values)  # 当前bar的开始时间价格
    High = list(data['High'].values)
    Low = list(data['Low'].values)
    Close = list(data['Close'].values)
    Open.reverse()
    High.reverse()
    Low.reverse()
    Close.reverse()
    trade = []
    ma10 = [None, None, None, None, None, None, None, None, None, None]
    ma5 = [None, None, None, None, None]
    ma20 = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    for i in range(0, len(Close) - 10):
        ma10.append(sum(Close[i:i + 10]) / 10)
    for i in range(0, len(Close) - 5):
        ma5.append(sum(Close[i:i + 5]) / 5)
    for i in range(0, len(Close) - 20):
        ma20.append(sum(Close[i:i + 20]) / 20)
    candlestick2_ochl(ax, Open, Close, High, Low, width=0.6, colorup='r', colordown='g')
    ax.set_xlabel('Date', fontsize=15)
    ax.set_ylabel('Price', fontsize=15)
    ax.set_title('300750')
    plt.plot(ma5, label='ma5')
    plt.legend()
    plt.plot(ma10, label='ma10')
    plt.legend()
    plt.plot(ma20, label='ma20')
    plt.legend()
    plt.savefig("300750.png")
    plt.show()
    print(ma10)


if __name__ == "__main__":
    df = pd.read_excel("save.xlsx")
    draw_bar(df)
