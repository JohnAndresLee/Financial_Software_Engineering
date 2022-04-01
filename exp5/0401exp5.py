import pandas as pd

data = []
df = pd.read_csv("./600036_half_year.csv")
for index, row in df.iterrows():
    # 筛选你想要的数据
    data.append(row)

OrderTime = data[0]['tradeDate']  # 下单时间记录
OrderPrice = data[0]['openPrice']  # 下单价格记录
CoverTime = data[-1]['tradeDate']  # 卖出时间记录
CoverPrice = data[-1]['closePrice']  # 卖出价格记录
print("Buy OrderTime:", OrderTime, " OrderPrice:", OrderPrice,)
print("SaleTime:", CoverTime, " SalePrice:", CoverPrice, " Profit:", CoverPrice-OrderPrice)