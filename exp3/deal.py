import re
import pandas as pd

data = pd.read_excel("deal.xlsx", header=None)
data = data[0].values
order = []
open_price = []
open_datetime = []
volume = []
for i in data:
    o = int(re.findall(r'\'order(\d*)\'', i)[0])-4
    p = re.findall(r'_price\': (\d*\.\d*)\,', i)[0]
    date = re.findall(r'_datetime\': \'(.*)\',', i)[0]
    v = re.findall(r'volume\': (\d*)', i)[0]
    open_price.append(p)
    order.append(o)
    open_datetime.append(date)
    volume.append(v)
d = {}
d['order'] = order
d['open_price'] = open_price
d['open_datetime'] = open_datetime
d['volume'] = volume
d = pd.DataFrame(d)
d.to_excel("deal.xlsx", index=None)
print("ok")
