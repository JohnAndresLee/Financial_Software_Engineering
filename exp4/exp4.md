# 金融软件工程实验四

<font size=5>**201870119 李锵**</font>

## 实验内容简述

本次实验的**主要内容**为：

1. 根据数据集中的半年数据，以天为单位用plt.vlines和plt.bars函数绘制“招商银行”的**K线图**;
2. 在上述K线图中叠加**MA线**；
3. 绘制对应的**量能图**。

本次实验使用到的**库**：

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec
from pylab import *
```



## 一、绘图前期准备工作

### matplotlib中文显示的问题

通过对matplotlib中的字体格式与编码转换进行设置，我们能够在绘图中正常使用中文：

```python
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
```

### 读取文件中的数据

```python
def read_data():
    df = pd.read_csv("600036_half_year.csv")
    data = []
    for index, row in df.iterrows():
        data.append([row['tradeDate'], row['highestPrice'], row['lowestPrice'], row['openPrice'], row['closePrice'], row['turnoverVol']])
    return data

# 函数中调用的格式
def draw_candle_volume():
    data = read_data()
    time = np.array([line[0] for line in data])
    highestprice = np.array([line[1] for line in data])
    lowestprice = np.array([line[2] for line in data])
    openprice = np.array([line[3] for line in data])
    closeprice = np.array([line[4] for line in data])
    volume = np.array([line[5] for line in data])
```

### 批量设置绘图颜色

利用Numpy库高效设置bar以及edge的颜色：
```python
	# 快速比较两个数列间同位置数字的大小关系
    colors_bool = closeprice > openprice
    bar_colors = np.zeros(colors_bool.size, dtype="U5")
    bar_colors[:] = "g"
    bar_colors[colors_bool] = "w"

    edge_colors = np.zeros(colors_bool.size, dtype="U1")
    edge_colors[:] = "g"
    edge_colors[colors_bool] = "r"
```



## 二、K线图的绘制

通过查阅相关资料，设定相关参数让绘制图片与我们预期一致

```python
    ax1.vlines(time, lowestprice, highestprice, colors=edge_colors)
    ax1.bar(time, (closeprice - openprice), bottom=openprice, color=bar_colors,
            edgecolor=edge_colors, zorder=3)
```

绘图的具体参数设置

```python
    ax1.set_ylabel("价格", fontsize=20)
    ax1.tick_params(axis='x', rotation=30, labelsize=12)
    ax1.grid(linestyle=":")
    ax1.tick_params(axis='y', labelsize=12)
    ax1.set_xticks(np.arange(0, len(time), 15))
```

![exp4(2)](G:\lq201870119\exp4\exp4(2).png)




## 三、K线图中叠加MA线

因为MA线涉及到数据量的偏移，先设置了前面若干个空值

```python
	ma5 = [None, None, None, None, None]
    ma10 = [None, None, None, None, None, None, None, None, None, None]
    ma20 = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
```

通过对均线价格的计算，我们得到了MA5, MA10, MA20三条均线的时间序列

```python
    for i in range(10, len(closeprice)):
        ma10.append(sum(closeprice[i - 10:i]) / 10)
    for i in range(5, len(closeprice)):
        ma5.append(sum(closeprice[i - 5:i]) / 5)
    for i in range(20, len(closeprice)):
        ma20.append(sum(closeprice[i - 20:i]) / 20)
    ax1.plot(time, ma5, label='ma5')
    ax1.plot(time, ma10, label='ma10')
    ax1.plot(time, ma20, label='ma20')
```

设置显示样例的大小

```python
    ax1.legend(fontsize=18)
```

![exp4(1)](G:\lq201870119\exp4\exp4(1).png)

## 四、量能图的绘制

此处采用了另外一种等价的方法设置量能图中的不同颜色

```python
    ax2.bar(time, volume,
            color=['g' if openprice[x] > closeprice[x] else 'r' for x in
                   range(0, len(time))])
```

量能图的参数设置：

```python
    ax2.set_xlabel('日期', fontsize=20)
    ax2.set_ylabel('成交量', fontsize=20)
    ax2.tick_params(axis='x', rotation=30, labelsize=12)
    ax2.set_xticks(np.arange(0, len(time), 15))
    ax2.grid(linestyle=":")
```

![test](G:\lq201870119\exp4\test.png)



## 五、子图样式设置

为了更便捷的对子图格式进行设置，我没有选择add_subplots()函数，而是通过gridspec.GridSpec()函数对子图的格式/位置进行设置。其中height_ratios设置了上下子图的高度比例。

```python
 	fig = plt.figure(dpi=200, figsize=(20, 10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    plt.title("600036 招商银行 K线图", fontsize=20)
```

![exp4(0)](G:\lq201870119\exp4\exp4(0).png)

**如果仅仅按照上面进行子图设置，我们将发现上子图的x轴显示在两图中间，这与我们常见的K线—量能图并不一致。如果简单粗暴的对x轴刻度进行不显示或者隐藏显示，则或多或少会影响到图片中grid的划分或者上下图间的美观，因此我使用subplots_adjust()调整了子图的行距，解决了上述问题。**

```python
fig.subplots_adjust(hspace=0)
```



## 六、实验结果

```python
	plt.savefig("exp4.png")
    plt.show()
```

![exp4](G:\lq201870119\exp4\exp4.png)



-------------

*2022-03-27*
