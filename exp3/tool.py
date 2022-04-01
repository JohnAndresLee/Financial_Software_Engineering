import pandas as pd

data = pd.read_excel("save2.xlsx")
Open = list(data['open'].values)
High = list(data['high'].values)
Low = list(data['low'].values)
Close = list(data['close'].values)
Open.reverse()
High.reverse()
Low.reverse()
Close.reverse()
dict = {}
dict['Open'] = Open
dict['Close'] = Close
dict['High'] = High
dict['Low'] = Low
dict = pd.DataFrame(dict)
dict.to_excel("save.xlsx", index=None)